#!/usr/bin/env python
import sys
import botocore
import boto3
import click
from halo import Halo

print("\n")
ecs = boto3.client('ecs')
waiter = ecs.get_waiter('services_stable')
spinner = Halo()

def pull_task_template(task_template):    
    spinner.start(text="Pulling service task template...\n")
    try:
        response = ecs.describe_task_definition(taskDefinition = task_template)        
    except botocore.exceptions.ClientError as error:
        spinner.fail(f"ERROR: {error.response['Error']['Code']}: {error.response['Error']['Message']}\n")
        print("\nFailed to retrieve task template. Exiting script.")
        sys.exit(1)
    except Exception:
        spinner.fail("\nFailed to retrieve task template. Exiting script.")
        raise
        sys.exit(1)
    else:
        spinner.succeed(f"Task template found! Basing new task on \033[1m{response['taskDefinition']['family']}.\033[0m\n")
        return response["taskDefinition"]


def register_new_task(task_def, image):
    spinner.start(text=f"Registering new task definition with provided container image...\n")
    task_def["containerDefinitions"][0]["image"] = image
    try:
        response = ecs.register_task_definition(
            family=task_def["family"].removesuffix("-template"),
            taskRoleArn=task_def["taskRoleArn"],
            executionRoleArn=task_def["executionRoleArn"],
            networkMode=task_def["networkMode"],
            volumes=task_def["volumes"],
            containerDefinitions=task_def["containerDefinitions"],
            requiresCompatibilities=task_def["requiresCompatibilities"],
            cpu=task_def["cpu"],
            memory=task_def["memory"]
        )
    except botocore.exceptions.ClientError as error:
        spinner.fail(f"ERROR: {error.response['Error']['Code']}: {error.response['Error']['Message']}\n")
        print("\nFailed to register new task definition. Exiting script.")
        sys.exit(1)
    else:
        spinner.succeed(f"New task successfully registered.\n")
        return response["taskDefinition"]["taskDefinitionArn"]
    

def update_service(new_task, project):
    spinner.start(text="Updating service with new task...\n")
    try:
        response = ecs.update_service(
            cluster=project + "-cluster",
            service=project + "-service",
            taskDefinition=new_task,
            forceNewDeployment=True
        )
    except botocore.exceptions.ClientError as error:
        spinner.fail(f"ERROR: {error.response['Error']['Code']}: {error.response['Error']['Message']}\n")
        print("\n New task registered, but failed to update service. Exiting script.")
        sys.exit(1)
    else:
        spinner.succeed(f"Service updated with new task definition.\n")
        return { "service": response["service"]["serviceArn"], "cluster": response["service"]["clusterArn"]}

def monitor_rollout(arns):
    spinner.start("Launching new tasks...\n")
    try:
        waiter.wait(
            cluster=arns["cluster"],
            services=[arns["service"]],
            # WaiterConfig={
            #     "Delay": 10,
            #     "MaxAttempts":25
            # }
        )
    except botocore.exceptions.WaiterError as error:
        spinner.fail(f"Tasks registered, but failing health checks. ERROR: {error}")
        print("Exiting script.")
        sys.exit(1)
    else:
        spinner.succeed("New tasks active!")
        print("\n")
        sys.exit(0)
        


@click.command()
@click.option("--image", required=True, help="Full URL of image to deploy.")
@click.option("--project", required=True, help="Name of the project; used as a prefix for all resources.")
def deploy_ecs(image, project):
    template = pull_task_template(f"{project}-task-template")
    new_task_def = register_new_task(template, image)
    arns = update_service(new_task_def, project)
    monitor_rollout(arns)

deploy_ecs()