# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = kiskadee
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

release:
	rm -rf kiskadee
	git clone ssh://git@pagure.io/docs/kiskadee.git
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(0)
	cp -r _build/html/* kiskadee
	cd kiskadee; git diff
	@printf "Confirm new documentation? [y/N]"; read confirm; \
		if [ "$$confirm" = 'y' -o "$$confirm" = 'Y' ]; then \
			cd kiskadee; git add . ; git commit && git push; cd ..; \
			rm -rf kiskadee; \
		else \
			echo 'Aborting...'; \
			rm -rf kiskadee; \
			false; \
		fi
