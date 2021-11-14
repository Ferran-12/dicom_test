FROM ubuntu:20.04
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential
RUN apt install -y python3-pip
RUN pip3 install -r requirements.txt

CMD ["python3", "-m" , "dicomhandling", "T1_3D_TFE-301"]