# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
import os
import tarfile
import tempfile
from shutil import copy2
import pdb
from kiskadee.helpers import to_firehose

def watch():
    pass

# Former watch(); this is actually analyzing the packages
def analyze(requested_source):
    """Monitor Debian repositories

    :returns: I not know yet, for now will return
    only the path to a source package, that will
    be analyzed by some analyzer.
    """
    extracts_path = extracted_source_path()
    extract_source(requested_source, extracts_path)
    analyzer_output = analyzers().cppcheck(extracts_path)
    to_firehose(analyzer_output, 'cppcheck')


def download_source(pkg_name, pkg_version):
    """Download packages from some debian mirror.

    :pkg_name: package name (a.g mutt)
    :pkg_version: package version (a.g 1.7.5-1)
    :returns: path to downloaded source package

    OBS: Other plugins may have this behavior,
    find a better place (module) to this method.
    """

def extract_source(source, path):
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

    source_path = abs_source_path(source)
    copy2(source_path, path)


def abs_source_path(source):
    """Returns de absolute path to the source

    :arg1: source
    :returns: path
    """
    return os.path.abspath(source)


def extracted_source_path():
    """Create a temporary directory
    """
    return tempfile.mkdtemp()


def analyzers():
    """ Read wich plugins will be run on the source code

    :returns: List of plugins to run on source code.

    """
    import kiskadee.analyzers.cppcheck as cppcheck

    return cppcheck
