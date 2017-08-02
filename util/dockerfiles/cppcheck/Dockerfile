FROM fedora

RUN dnf -y update && dnf clean all
RUN dnf -y install cppcheck && dnf clean all

RUN useradd -ms /bin/bash kiskadee

USER kiskadee

ENTRYPOINT ["cppcheck", "--enable=all", "--xml-version=2", "--quiet"]
