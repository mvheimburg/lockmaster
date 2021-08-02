FROM postgres:latest

ARG POSTGRES_SERVER
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

ENV POSTGRES_SERVER=$POSTGRES_SERVER
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB

# ARG DOMAIN
# ARG CERTRESOLVER

# LABEL   traefik.enable="true" \
#         traefik.http.routers.db.entrypoints="websecure" \
#         # traefik.http.routers.db.rule="PathPrefix(`/db{regex:$$|/.*}`) || Host(`doorcontrol.${DOMAIN}`) && PathPrefix(`/db{regex:$$|/.*}`)" \
#         traefik.http.routers.db.rule="Host(`doorcontrol.${DOMAIN}`) && PathPrefix(`/db{regex:$$|/.*}`)" \
#         traefik.http.routers.db.tls="true" \
#         traefik.http.routers.db.tls.certresolver=${CERTRESOLVER} 
#         # traefik.http.services.db.loadbalancer.server.port="5432"