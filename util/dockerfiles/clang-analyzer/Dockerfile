FROM fedora
RUN dnf -y update && dnf clean all
RUN dnf -y install clang-analyzer make && dnf clean all

COPY ./docker-entrypoint.sh /tmp
WORKDIR /tmp
RUN chmod 777 docker-entrypoint.sh
ENTRYPOINT ["/tmp/docker-entrypoint.sh"]
