# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from importlib import import_module
import shutil
import tempfile
import os
from contextlib import contextmanager


def to_firehose(bytes_input, analyzer):
    """ Parser the analyzer report to Firehose format
    :bytes_input: The analyzer report, as a byte string
    :returns: A xml.etree.ElementTree object, representing the firehose report
    """

    tempdir = tempfile.mkdtemp()
    tmp_report_file = "tmp_%s_report.xml" % analyzer
    report_directory = os.path.join(os.path.abspath("."), "reports/")

    try:
        os.mkdir(report_directory)
    except OSError:
        pass

    file_to_parse = os.path.join(tempdir, tmp_report_file)
    with open(file_to_parse, 'w') as f:
        f.write(bytes_input.decode('UTF-8'))

    analyzer_module = import_analyzer_module(analyzer)

    if (analyzer_module):
        firehose_tree = analyzer_module.parse_file(file_to_parse).to_xml_bytes()

    shutil.rmtree(tempdir)

    return firehose_tree


def import_analyzer_module(analyzer):
    """ Import a firehose parser

    analyzer: The name of the parser that will be imported
    :returns: Some firehose parser
    """

    try:
        return import_module("firehose.parsers.%s" % (analyzer))
    except ImportError:
        print("ERROR: Firehose parser %s not found" % analyzer)


@contextmanager
def chdir(path):
    initial_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(initial_dir)
