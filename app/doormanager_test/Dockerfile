FROM python:3.7.8



ENV APP = /app
WORKDIR "${APP}"

# Copy requirements.txt first for better cache on later pushes
COPY requirements.txt requirements.txt

# pip install python deps from requirements.txt on the resin.io build server
RUN pip3 install -U pip && \
    pip3 install -U setuptools && \
    pip3 install -U wheel

RUN pip3 install -r requirements.txt

# This will copy all files in our root to the working  directory in the container
COPY src doormanager/

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1
