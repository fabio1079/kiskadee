FROM fedora

RUN dnf -y update && dnf clean all
RUN dnf -y install cppcheck && dnf clean all

ENTRYPOINT ["cppcheck", "--enable=all", "--xml-version=2"]
