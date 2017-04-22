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
import subprocess
import pdb


def cppcheck(source_dir):
    """ Run Cppcheck on source code, inside source_dir
    :source_dir: Absolute path to source code
    :returns: Write cppcheck report inside kiskadee/reports directory
    """
    report_directory = os.path.join(os.path.abspath("."), "reports/")
    try:
        os.mkdir(report_directory)
    except OSError:
        pass

    report_file = "cppcheck_report.xml"
    initial_dir =os.getcwd()
    # TODO: Use 'with' to change to the extracted
    # source directory, instead of os.getcwd()
    os.chdir(source_dir)
    pipes = subprocess.Popen([ 'cppcheck', '-j8', '--enable=all', 
                               '--xml-version=2', '.'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)

    std_out, std_err = pipes.communicate()

    f = open(report_directory + report_file, 'w')
    f.write(std_err.decode('utf-8'))
    f.close
    os.chdir(initial_dir)
    


def to_firehose(report):
    """ Parser the analyzer report to Firehose format
    :report: The analyzer report
    :returns: Firehose report
    """
    pass

def version():
    try:
        return check_output(['cppcheck', '--version']).strip()
    except Exception:
        print("Cppcheck not found")
