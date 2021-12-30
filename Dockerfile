FROM python:3.9 as reqs-stage
WORKDIR /tmp
RUN pip install pipenv
COPY ./Pipfile ./Pipfile.lock /tmp/
RUN pipenv lock --keep-outdated --requirements > requirements.txt
FROM python:3.9
WORKDIR /code
COPY --from=reqs-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]