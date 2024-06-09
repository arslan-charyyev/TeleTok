FROM python:3.12.4-alpine

WORKDIR /code

COPY pyproject.toml requirements.txt ./

RUN pip install -r requirements.txt

COPY app app

CMD [ "python", "app/main.py" ]