# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import tempfile
import os
from subprocess import check_output
import subprocess
import pdb
import shutil


def cppcheck(source_dir):
    """ Run Cppcheck on source code, inside source_dir
    :source_dir: Absolute path to source code
    :returns: Write cppcheck report inside kiskadee/reports directory
    """

    initial_dir = os.getcwd()
    # TODO: Use 'with' to change to the extracted
    # source directory, instead of os.getcwd()
    os.chdir(source_dir)
    pipes = subprocess.Popen([ 'cppcheck', '-j8', '--enable=all',
                               '--xml-version=2', '.'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    os.chdir(initial_dir)
    _, std_err = pipes.communicate()
    return std_err


def version():
    try:
        return check_output(['cppcheck', '--version']).strip()
    except Exception:
        print("Cppcheck not found")
