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
from kiskadee.queue import enqueue_analysis, \
        enqueue_package
from contextlib import contextmanager


def to_firehose(bytes_input, analyzer):
    """ Parser the analyzer report to Firehose format
    :bytes_input: The analyzer report, as a byte string
    :returns: A xml.etree.ElementTree object, representing the firehose report
    """

    tempdir = tempfile.mkdtemp()
    tmp_report_file = "tmp_%s_report.xml" % analyzer
    firehose_report_file = "firehose_%s_report.xml" % analyzer
    report_directory = os.path.join(os.path.abspath("."), "reports/")

    try:
        os.mkdir(report_directory)
    except OSError:
        pass

    file_to_parse = os.path.join(tempdir, tmp_report_file)
    with open(file_to_parse) as f:
        f.write(bytes_input.decode('UTF-8'))

    analyzer_module = import_analyzer_module(analyzer)

    if (analyzer_module):
        analyzer_report_file = report_directory + firehose_report_file
        firehose_tree = analyzer_module.parse_file(file_to_parse).to_xml()
        firehose_tree.write(analyzer_report_file, encoding='UTF-8')

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


def enqueue_source(func):
    """ Decorator to add the behavior of
    queue in the enqueue_analysis,
    some random value. """
    def wrapper(*args, **kwargs):
        source = func(*args, **kwargs)
        enqueue_analysis(source)
    return wrapper


def enqueue_pkg(func):
    """ Decorator to add the behavior of
    queue in the enqueue_package,
    some random value. """
    def wrapper(*args, **kwargs):
        package = func(*args, **kwargs)
        enqueue_package(package)
    return wrapper

@contextmanager
def chdir(path):
    initial_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(initial_dir)
