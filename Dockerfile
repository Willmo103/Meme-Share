FROM python:latest

WORKDIR /src

COPY requirements.txt /src/requirements.txt

RUN pip install -r requirements.txt

COPY . /src

EXPOSE 1234

CMD ["flask", "run", "--port=1234", "--host=0.0.0.0"]
