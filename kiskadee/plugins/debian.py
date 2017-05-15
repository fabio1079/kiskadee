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
from shutil import copy2
from kiskadee.helpers import to_firehose
from kiskadee.helpers import enqueue_source, enqueue_pkg
import kiskadee
import urllib.request
from subprocess import check_output
from deb822 import Sources
from time import sleep

PLUGIN_DATA = kiskadee.config['debian_plugin']
running = True

def queue_sources_gz_pkgs(path):
    sources = os.path.join(path, 'Sources')
    with open(sources) as sources_file:
        for src in Sources.iter_paragraphs(sources_file):
            create_package_dict(src)


@enqueue_pkg
def create_package_dict(src):
    return {'name': src["Package"],
           'version': src["Version"],
           'plugin': kiskadee.plugins.debian,
           'meta': { 'directory': src['Directory']}
           }


@enqueue_source
def download_source(source_data):
    """Download packages from some debian mirror."""

    temp_dir = tempfile.mkdtemp()
    initial_dir = os.getcwd()
    os.chdir(temp_dir)
    url = dsc_url(source_data)
    check_output(['dget', url])
    os.chdir(initial_dir)
    return temp_dir


def collect():
    url = sources_gz_url()
    sources_gz_dir = download_sources_gz(url)
    uncompress_gz(sources_gz_dir)
    queue_sources_gz_pkgs(sources_gz_dir)


def watch():
    """ Starts the continuing monitoring process of Debian
    Repositories. Each package monitored by the plugin will be
    queued using the enqueue_pkg decorator. """

    while running:
        collect()
        sleep(PLUGIN_DATA.get('schedule') * 60)


# Former watch(); this is actually analyzing the packages
def analyze(requested_source):
    """Monitor Debian repositories

    :returns: I not know yet, for now will return
    only the path to a source package, that will
    be analyzed by some analyzer.
    """
    extracts_path = extracted_source_path()
    uncompress_tar_gz(requested_source, extracts_path)
    analyzer_output = analyzers().cppcheck(extracts_path)
    to_firehose(analyzer_output, 'cppcheck')


def uncompress_tar_gz(source, path):
    """Extract the source code to a randomic dir.

    :source: The source code (tar.gz) that will be analyzed.
    :path: The path where the tar.gz is located.
    """

    copy_source(source, path)
    abs_tar_path = path + '/' + os.path.basename(source)
    source_tarfile = tarfile.open(abs_tar_path)
    source_tarfile.extractall(path)
    os.remove(abs_tar_path)


def copy_source(source, path):
    """Copy the source code to a proper directory

    :arg1: source file
    """

    source_path = os.path.abspath(source)
    copy2(source_path, path)


def extracted_source_path():
    """Create a temporary directory
    """
    return tempfile.mkdtemp()



def dsc_url(source_data):
    """ Mount the dsc url required by dget tool to download the
    source of a debian package.
    (a.g dget http://ftp.debian.org/debian/pool/main/0/0ad/0ad_0.0.21-2.dsc)

    """

    name = source_data['name']
    version = source_data['version']
    directory = source_data['directory']
    mirror = PLUGIN_DATA['target']
    return ''.join([mirror, '/', directory, '/', name, '_', version, '.dsc'])


def sources_gz_url():
    """ Mount the Sources.gz url"""
    mirror = PLUGIN_DATA['target']
    release = PLUGIN_DATA['release']

    return "%s/dists/%s/main/source/Sources.gz" % (mirror, release)


def download_sources_gz(url):
    """Download and Extract the Sources.gz file, from some Debian Mirror.

    :data: The config.json file as a dict
    :returns: The path to the Sources.gz file

    """

    temp_dir = tempfile.mkdtemp()

    initial_dir = os.getcwd()
    os.chdir(temp_dir)
    in_file = urllib.request.urlopen(url)
    data = in_file.read()

    with open('Sources.gz', 'wb') as info:
        info.write(data)

    os.chdir(initial_dir)
    return temp_dir


def uncompress_gz(path):
    """Extract Some .gz file"""
    compressed_file_path = os.path.join(path, PLUGIN_DATA['meta'])
    check_output(['gzip', '-d', '-k', '-f', compressed_file_path])
    return path


def analyzers():
    """ Read wich plugins will be run on the source code

    :returns: List of plugins to run on source code.

    """
    import kiskadee.analyzers.cppcheck as cppcheck
    return cppcheck
