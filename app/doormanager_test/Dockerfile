FROM python:3.8-buster as builder
ARG VIRTUAL_ENV


RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip
RUN pip3 install \
    setuptools \
    wheel 


COPY requirements.txt requirements.txt

RUN pip3 install --ignore-installed -r requirements.txt

FROM python:3.8
ARG VIRTUAL_ENV

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# RUN : \
#     && apt update \
#     && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
#     rpi.gpio \
#     python3-gpiozero \
#     && apt-get clean \
#         && rm -rf /var/lib/apt/lists/* \
#         && :

WORKDIR /app

COPY src/ .

ENV UDEV=1

