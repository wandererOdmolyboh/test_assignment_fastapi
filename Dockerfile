FROM python:3.10

RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev

RUN mkdir /test_assignment_fastapi

WORKDIR /test_assignment_fastapi

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

COPY docker /docker

RUN chmod a+x docker/*.sh
