FROM balenalib/raspberrypi4-64-python:3.8-buster-build as builder

ARG VIRTUAL_ENV

RUN : \
    && apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && :

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip
RUN pip3 install \
    setuptools \
    wheel 


COPY requirements.txt requirements.txt

RUN pip3 install --ignore-installed -r requirements.txt





FROM balenalib/raspberrypi4-64-python:3.8-buster-run

ARG VIRTUAL_ENV
ARG DOMAIN
ARG CERTRESOLVER
ARG BUILD_TYPE

ARG POSTGRES_SERVER
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG BUILD_TYPE
ARG MQTT_CLIENT_ID
ARG MQTT_HOST
ARG MQTT_PORT
ARG MQTT_USERNAME
ARG MQTT_PASSWORD

ENV POSTGRES_SERVER=$POSTGRES_SERVER
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB
ENV BUILD_TYPE=$BUILD_TYPE
ENV MQTT_CLIENT_ID=$MQTT_CLIENT_ID
ENV MQTT_HOST=$MQTT_HOST
ENV MQTT_PORT=$MQTT_PORT
ENV MQTT_USERNAME=$MQTT_USERNAME
ENV MQTT_PASSWORD=$MQTT_PASSWORD


COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"



RUN : \
    && apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    libpq5 \
    && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && :

WORKDIR /app

COPY src/ .

LABEL   traefik.enable="true" \
        traefik.http.routers.doormanager-secure.entrypoints="websecure" \
        traefik.http.routers.doormanager-secure.rule="Host(`doorcontrol.${DOMAIN}`) && PathPrefix(`/doormanager`)" \
        traefik.http.routers.doormanager-secure.middlewares="doormanager-strip" \
        traefik.http.routers.doormanager-secure.tls="true" \
        traefik.http.routers.doormanager-secure.tls.certresolver=${CERTRESOLVER} \
        traefik.http.routers.doormanager-secure.service="doormanager"\
        traefik.http.routers.doormanager.entrypoints="web" \
        traefik.http.routers.doormanager.rule="PathPrefix(`/doormanager`)" \
        traefik.http.routers.doormanager.middlewares="doormanager-strip" \
        traefik.http.routers.doormanager.service="doormanager"\
        traefik.http.middlewares.doormanager-strip.stripprefix.prefixes="/doormanager" \
        traefik.http.services.doormanager.loadbalancer.server.port="5555"

# RUN echo 'alias run="gunicorn main:app -b 0.0.0.0:5555 -k uvicorn.workers.UvicornWorker"' >> ~/.bashrc
# ENV UDEV=1

