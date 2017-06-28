FROM fedora

RUN dnf -y update && dnf clean all
RUN dnf -y install frama-c && dnf clean all
COPY ./run-analysis.sh /usr/bin/run-analysis

ENTRYPOINT ["run-analysis"]
