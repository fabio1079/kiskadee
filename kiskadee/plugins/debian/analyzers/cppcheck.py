# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from firehose.model import Issue, Message, File, Location, Point
import tempfile
import os
from subprocess import check_output


def cppcheck(source_dir):
    """ Run Cppcheck on source code, inside source_dir
    :source_dir: Absolute path to source code
    :returns: Cppcheck report
    """
    os.chdir(source_dir)
    run_command([ 'cppcheck', '-j8', '--enable=all', '--xml-version=2', '.'])


def to_firehose(report):
    """ Parser the analyzer report to Firehose format
    :report: The analyzer report
    :returns: Firehose report
    """
    pass


def run_command(arg1):
    """TODO: Docstring for run_command.

    :arg1: TODO
    :returns: TODO

    """
    pass


def version():
    try:
        return check_output(['cppcheck', '--version']).strip()
    except Exception:
        print("Cppcheck not found")
