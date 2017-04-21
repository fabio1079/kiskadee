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

def watch():
    """Monitor Debian repositories

    :returns: I not know yet, for now will return
    only the path to a source package, that will
    be analyzed by some analyzer.
    """
    requested_pkg_path = sys.argv[1]
    extracted_pkg_path = extract_source_package(requested_pkg_path)
    plugins().cppcheck(extracted_pkg_path)




def download_source_package(pkg_name, pkg_version):
    """Download packages from some debian mirror.

    :pkg_name: package name (a.g mutt)
    :pkg_version: package version (a.g 1.7.5-1)
    :returns: path to downloaded source package

    OBS: Other plugins may have this behavior,
    find a better place (module) to this method.
    """

def extract_source_package(pkg_dir):
    """Extract the source code to a randomic dir.

    :arg1: the absolute tar.gz directory of the downloaded package. 
    :returns: the randomic path to the extracted package.

    """

    absolute_pkg_dir = os.path.abspath(pkg_dir)
    extraction_dir = tempfile.mkdtemp()
    copy2(absolute_pkg_dir, extraction_dir)
    abs_tar_path = extraction_dir + '/' + pkg_dir
    pkg_tarfile = tarfile.open(abs_tar_path)
    pkg_tarfile.extractall(extraction_dir)
    os.remove(abs_tar_path)
    return extraction_dir






def plugins():
    """ Read wich plugins will be run on the source code

    :returns: List of plugins to run on source code.

    """
    import kiskadee.analyzers.cppcheck as cppcheck

    return cppcheck
