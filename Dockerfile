FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/test_assignment_fastapi

RUN mkdir /test_assignment_fastapi

WORKDIR /test_assignment_fastapi

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
