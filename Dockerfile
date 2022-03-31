FROM python:3.8
ENV PYTHONUNBUFFERED=1

# creating the code directory in Docker 
RUN mkdir /code 

# making code directory the working file
WORKDIR /code

RUN pip install --upgrade pip

# usng pipenv to manage dependencies
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

COPY ./LeisureInn/.env /code/
COPY . /code/