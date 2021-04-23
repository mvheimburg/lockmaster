FROM balenalib/raspberrypi3-python:3.8-buster-build as builder

ARG VIRTUAL_ENV


RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip
RUN pip3 install \
    setuptools \
    wheel 


COPY requirements.txt requirements.txt

RUN pip3 install --ignore-installed -r requirements.txt





FROM balenalib/raspberrypi3-python:3.8-buster-run

ARG VIRTUAL_ENV
ARG DOMAIN
ARG CERTRESOLVER

LABEL   traefik.enable="true" \
        traefik.http.routers.doormanager.entrypoints="websecure" \
        # traefik.http.routers.doormanager.rule="PathPrefix(`/doormanager{regex:$$|/.*}`) || Host(`doorcontrol.${DOMAIN}`) && PathPrefix(`/doormanager{regex:$$|/.*}`)" \
        traefik.http.routers.doormanager.rule="Host(`doorcontrol.${DOMAIN}`) && PathPrefix(`/doormanager{regex:$$|/.*}`)" \
        traefik.http.routers.doormanager.middlewares="doormanager-stripprefix" \
        traefik.http.routers.doormanager.tls="true" \
        traefik.http.routers.doormanager.tls.certresolver=${CERTRESOLVER} \
        traefik.http.middlewares.doormanager-stripprefix.stripprefix.prefixes="/doormanager" \
        traefik.http.services.doormanager.loadbalancer.server.port="5555"


ARG POSTGRES_SERVER
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

ENV POSTGRES_SERVER=$POSTGRES_SERVER
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB


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

# ENV UDEV=1

