FROM fedora

RUN dnf -y update && dnf clean all
RUN dnf -y install clang-analyzer make && dnf clean all
COPY ./run-analysis.sh /usr/bin/run-analysis

ENTRYPOINT ["run-analysis"]
