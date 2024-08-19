


FROM balenalib/raspberrypi4-64-debian-python:latest

ARG BUILD_TYPE
ARG MQTT_CLIENT_ID
ARG MQTT_HOST
ARG MQTT_PORT
ARG MQTT_USERNAME
ARG MQTT_PASSWORD

ENV BUILD_TYPE=${BUILD_TYPE}
ENV MQTT_CLIENT_ID=${MQTT_CLIENT_ID}
ENV MQTT_HOST=${MQTT_HOST}
ENV MQTT_PORT=${MQTT_PORT}
ENV MQTT_USERNAME=${MQTT_USERNAME}
ENV MQTT_PASSWORD=${MQTT_PASSWORD}

RUN apt update && apt install -y --no-install-recommends \
	x11-apps \
	x11-xserver-utils \
	mesa-utils \
	mesa-common-dev \
	build-essential \
	wget \
	curl \
	# python${PYTHON_VERSION_MAJOR}-pip \
	# python${PYTHON_VERSION_MAJOR}-setuptools \
	# python${PYTHON_VERSION_MAJOR}-opengl \
	libmpv1 \
	libgtk-3-dev \
	libgstreamer1.0-dev \
	libgstreamer-plugins-base1.0-dev \
	&& rm -rf /var/lib/apt/lists/*


RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN curl -sSL https://pdm-project.org/install-pdm.py | python3 -
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY pdm.lock /app/pdm.lock
COPY doorbell/ /app/doorbell

RUN pdm sync --no-editable
RUN echo "BUILD FINISHED"

COPY hyper.toml/ /app/hyper.toml
COPY start.sh/ /app/start.sh

ENV PULSE_SERVER=unix:/run/pulse/pulseaudio.socket

ENTRYPOINT ["bash", "/app/start.sh"]


