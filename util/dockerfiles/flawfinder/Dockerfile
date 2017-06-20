FROM fedora

RUN dnf -y update && dnf clean all
RUN dnf -y install python flawfinder && dnf clean all

ENTRYPOINT ["flawfinder"]
