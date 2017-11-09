# bash is needed to run pushd/popd for the analyzers target
SHELL:=/bin/bash

help:
	@printf "Available targets: check, analyzers, clean\n\n"

check:
	coverage run --omit="lib/*","setup.py","kiskadee/tests/*",".eggs/*",".venv/*" ./setup.py test
	coverage html

analyzers:
	docker ps 2> /dev/null; \
	if [ $$? -ne 1 ]; then \
			echo "docker daemon properly configured. Building images..."; \
	else \
			echo "docker daemon was not properly configured, is the service running?"; \
			exit; \
	fi; \
	pushd util/dockerfiles; \
	for analyzer in `ls`; do \
		pushd $$analyzer; \
		docker build . -t $$analyzer; \
		popd; \
	done

deploy:
	echo "Installing kiskadee...";
	ansible-playbook -i playbook/${INVENTORY} playbook/site.yml -f 10;

clean:
	rm -rf htmlcov .coverage kiskadee.egg-info build dist
