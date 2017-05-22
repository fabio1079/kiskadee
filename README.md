# kiskadee

kiskadee is a continuous static analysis tool which writes the analyses
results into a Firehose database.

## Dependencies

In order to install kiskadee dependencies, just run `pip install -e .`

## Architecture

#### monitor
  
* loads all plugins watch() functions
* load all repositories package versions with the watch() functions 
* compares repository versions against db versions
* writes differences in the analysis queue

#### runner

* consume the analysis queue and compare messages with plugin messages
  * on matches, run all analyzers listed by the plugin in upstream source code
* Convert static analyzer output to firehose
* save file in DB

We think kubernetes may be a good idea for each plugin run. Not sure if
possible.

### plugins subpackage

kiskadee needs plugins to run static analyzers. Each plugin must inherit from
the Plugin class and implement its abstract methods.

## License

Copyright (C) 2017 the AUTHORS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
