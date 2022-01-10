version: 2.1
workflows:
  test_build_push:
    jobs:
      - test:
          context: personal_testing
      - build_and_push:
          context: personal_testing
jobs:
  test:
    working_directory: ~/app
    docker:
      - image: cimg/python:3.9
        auth:
          username: animaldna
          password: $DOCKERHUB_PASSWORD
        environment:
          AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID
          AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY
          AWS_DEFAULT_REGION: us-east-2
    resource_class: small
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run: sudo chown -R circleci:circleci /usr/local/bin
      - run: sudo chown -R circleci:circleci /home/circleci/.pyenv/versions/3.9.9/lib/python3.9/site-packages
      - run: sudo chown -R circleci:circleci /home/circleci/.local/share/
      - restore_cache:
          key: deps9-{{ .Branch }}-{{ checksum "Pipfile.lock" }}
      - run:
          command: pipenv install
      - save_cache:
          key: deps9-{{ .Branch }}-{{ checksum "Pipfile.lock" }}
          paths:
            - ".venv"
            - "/usr/local/bin"
            - "/home/circleci/.pyenv/versions/3.9.9/lib/python3.9/site-packages"
            - "/home/circleci/.local/share/virtualenvs/"
      - run:
          command: |
            mkdir test-results
            pipenv run pytest -v --junitxml=test-results/junit.xml
      - store_test_results:
          path: test-results
  build_and_push:
    working_directory: ~/app
    docker:
      - image: animaldna/cimg-py-aws:latest
        auth:
          username: animaldna
          password: $DOCKERHUB_PASSWORD
    resource_class: small
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run: 
          command: |
            sudo chown -R circleci:circleci /usr/local/bin
            sudo chown -R circleci:circleci /home/circleci/.pyenv/versions/3.9.9/lib/python3.9/site-packages
            sudo chown -R circleci:circleci /home/circleci/.local/share/
      - run: 
          command: aws ecr get-login-password | docker login -u ${AWS_ACCESS_KEY} AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
      - run:
          command: |
            docker build -t demo-catalog_api:${CIRCLE_SHA1} .
            docker tag demo-catalog_api:${CIRCLE_SHA1} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/demo-catalog_api:${CIRCLE_SHA1}
            docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/demo-catalog_api:${CIRCLE_SHA1} 
