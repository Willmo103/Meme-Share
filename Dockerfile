FROM python:latest

WORKDIR /src

COPY requirements.txt /src/requirements.txt

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /src

EXPOSE 9876

ENV FLASK_APP=app

CMD ["flask", "run", "--host=0.0.0.0", "--port=9876"]
