FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED = 1
# base setting
RUN apt-get -y update
RUN apt-get -y install vim
RUN mkdir /app

# install packages
WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
