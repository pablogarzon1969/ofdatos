# pull official base image
FROM python:3.9.7
# install system dependencies
RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get clean
COPY . /app/app
WORKDIR /app/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]