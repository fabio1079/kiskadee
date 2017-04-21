# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

def init():
    """TODO: Docstring for init.

    :arg1: TODO
    :returns: TODO

    """
    print(cppcheck.version())

def download_source_package(pkg_name, pkg_version):
    """Download packages from some debian mirror.

    :pkg_name: package name (a.g mutt)
    :pkg_version: package version (a.g 1.7.5-1)
    :returns: source package

    OBS: Other plugins may have this behavior,
    find a better place (module) to this method.
    """

def extract_source_package(pkg_dir):
    """Extract the source code to a randomic dir.

    :arg1: the tar.gz directory of the downloaded package. 
    :returns: the randomic path to the extracted package.

    """

def plugins():
    """ Read wich plugins will be run on the source code

    :returns: List of defined plugins

    """
    pass
