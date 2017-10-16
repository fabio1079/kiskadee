FROM fedora

RUN dnf -y update && dnf clean all
RUN dnf -y install python flawfinder && dnf clean all

WORKDIR /tmp
ENTRYPOINT ["/tmp/docker-entrypoint.sh"]
COPY ./docker-entrypoint.sh /tmp
RUN chmod 777 docker-entrypoint.sh
