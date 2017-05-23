# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
import tarfile
import tempfile
from kiskadee.helpers import to_firehose
from kiskadee.helpers import enqueue_source, enqueue_pkg
import kiskadee
import urllib.request
from subprocess import check_output
from deb822 import Sources
from time import sleep
from kiskadee.helpers import chdir

running = True


class Plugin(kiskadee.plugins.Plugin):

    def watch(self):
        """ Starts the continuing monitoring process of Debian
        Repositories. Each package monitored by the plugin will be
        queued using the enqueue_pkg decorator. """

        while running:
            url = self._sources_gz_url()
            sources_gz_dir = self._download_sources_gz(url)
            self._uncompress_gz(sources_gz_dir)
            self._queue_sources_gz_pkgs(sources_gz_dir)
            sleep(self.config['schedule'] * 60)

    @enqueue_source
    def get_sources(self, source_data):
        """Download packages from some debian mirror."""

        path = tempfile.mkdtemp()
        with chdir(path):
            url = self._dsc_url(source_data)
            check_output(['dget', url])

        return path


    def _queue_sources_gz_pkgs(self, path):
        sources = os.path.join(path, 'Sources')
        with open(sources) as sources_file:
            for src in Sources.iter_paragraphs(sources_file):
                self._create_package_dict(src)


    @enqueue_pkg
    def _create_package_dict(self, src):
        return {'name': src["Package"],
            'version': src["Version"],
            'plugin': kiskadee.plugins.debian,
            'meta': { 'directory': src['Directory']}
            }



    def _dsc_url(self, source_data):
        """ Mount the dsc url required by dget tool to download the
        source of a debian package.
        (a.g dget http://ftp.debian.org/debian/pool/main/0/0ad/0ad_0.0.21-2.dsc)

        """

        name = source_data['name']
        version = source_data['version']
        directory = source_data['directory']
        return ''.join([self.config['target'], '/',
                        directory, '/', name, '_', version, '.dsc'])


    def _sources_gz_url(self):
        """ Mount the Sources.gz url"""

        return "%s/dists/%s/main/source/Sources.gz" % (self.config['target'],
                                                        self.config['release'])


    def _download_sources_gz(self, url):
        """Download and Extract the Sources.gz file, from some Debian Mirror.

        :data: The config.json file as a dict
        :returns: The path to the Sources.gz file

        """

        path = tempfile.mkdtemp()
        with chdir(path):
            in_file = urllib.request.urlopen(url)
            data = in_file.read()
            with open('Sources.gz', 'wb') as info:
                info.write(data)
        return path


    def _uncompress_gz(self, path):
        """Extract Some .gz file"""
        compressed_file_path = os.path.join(path, self.config['meta'])
        check_output(['gzip', '-d', '-k', '-f', compressed_file_path])
        return path
