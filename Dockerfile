# Set up base environment
FROM python:3.8.11

# Expose Ports
ENV LISTEN_PORT=80
EXPOSE 80

#update environment
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install -U pip

# Set working directory
WORKDIR /RAFA

#Install Requirements
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy Files to container image
COPY . .
# start app
CMD ["python", "index.py"]

