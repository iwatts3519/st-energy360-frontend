# Set up base environment
FROM python:3.9

# Expose Ports
ENV LISTEN_PORT=80
EXPOSE 80

#update environment
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install -U pip

# Set working directory
WORKDIR /RAFA
# Install Tim
COPY ./setup.py ./setup.py
COPY ./tim_client ./tim_client
COPY requirements.txt ./requirements.txt
CMD ["python", "setup.py install"]

#Install Requirements
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy Files to container image
COPY ./apps ./apps
COPY ./Assets ./Assets
COPY ./Data ./Data
COPY ./app.py ./app.py
COPY ./credentials.json ./credentials.json
COPY ./deops.py ./deops.py
COPY ./helper_functions.py ./helper_functions.py
COPY ./index.py ./index.py
COPY ./iw_model_trial.py ./iw_model_trial.py
COPY ./keele_data.py ./keele_data.py
# start app
CMD ["python", "index.py"]

