kiskadee documentation
======================

Performing source code static analysis during the software development cycle
may be a difficult task: there are different static analyzers available and
each of them usually performs better in a small set of problems, making it hard
to choose one tool. Combining the analysis of different tools solves this
problem but, then, other problems arise, namely the generated false positives
and the fact that some alarms are more relevant than others.  kiskadee is a
system to support static analysis usage during software development by
providing ranked static analysis reports. First, it runs multiple
security-oriented static analyzers on the source code. Then, using a
classification model, the possible bugs detected by the static analyzers are
ranked based on their importance, where critical flaws are ranked first and
potential false positives are ranked last.

License
-------

## License
Copyright (C) 2017 the AUTHORS (see the AUTHORS file)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: User Documentation

   introduction
   architecture
   analyzers
   fetchers
   config_file
   installing

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Developer Documentation

   development
