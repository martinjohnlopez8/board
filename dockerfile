FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /board
WORKDIR /board
COPY requirements.txt /board/
RUN pip install -r requirements.txt
COPY . /board/