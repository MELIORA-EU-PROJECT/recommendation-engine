FROM python:3.10
LABEL authors="Nikos Gournakis"

WORKDIR /app


RUN pip install "fastapi[standard]"
RUN pip install json5
RUN pip install numpy
RUN pip install requests
RUN pip install colorama

COPY *.py .
COPY ./models ./models
COPY .env .


ENTRYPOINT ["fastapi", "dev", "main.py", "--port", "1564","--host","0.0.0.0"]