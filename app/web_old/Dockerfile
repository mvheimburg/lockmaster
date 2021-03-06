FROM balenalib/raspberrypi3-python:3.8-stretch-build as builder
ARG VIRTUAL_ENV

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip
RUN pip3 install \
    setuptools \
    wheel 


COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
RUN pip3 install --ignore-installed -r requirements.txt

RUN pip3 install --no-warn-script-location anvil-app-server

FROM balenalib/raspberrypi3-python:3.8-stretch-run
ARG VIRTUAL_ENV

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN install_packages openjdk-8-jdk-headless

RUN anvil-app-server || true

VOLUME /app
WORKDIR /app

RUN mkdir /anvil-data

RUN useradd anvil
RUN chown -R anvil:anvil /anvil-data
USER anvil

RUN ls
COPY src web/

ENTRYPOINT ["anvil-app-server", "--data-dir", "/anvil-data", "--origin", "https://doorcontrol.lvh.duckdns.org/80"]
# ENTRYPOINT ["anvil-app-server", "--data-dir", "/anvil-data"]
