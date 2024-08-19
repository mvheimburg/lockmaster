# FROM linuxserver/unifi-controller:latest
ARG DOMAIN
ARG CERTRESOLVER

FROM jacobalberty/unifi:latest

ARG DOMAIN
ARG CERTRESOLVER

# LABEL   traefik.enable="true" \
#         traefik.http.routers.unifi.entrypoints="websecure" \
#         # traefik.http.routers.unifi.rule="PathPrefix(`/unifi{regex:$$|/.*}`) || Host(`unifi.${DOMAIN}`)" \
#         traefik.http.routers.unifi.rule="Host(`unifi.${DOMAIN}`)" \
#         traefik.http.routers.unifi.tls="true" \
#         traefik.http.routers.unifi.tls.certresolver=${CERTRESOLVER} \
#         traefik.http.services.unifi.loadbalancer.server.scheme=https \
#         traefik.http.services.unifi.loadbalancer.server.port="8443"