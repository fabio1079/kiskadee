FROM fedora

RUN dnf -y update && dnf clean all
RUN dnf -y install python flawfinder && dnf clean all

RUN useradd -ms /bin/bash kiskadee
USER kiskadee

ENTRYPOINT ["flawfinder"]
