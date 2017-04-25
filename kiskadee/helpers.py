# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from subprocess import check_output
from importlib import import_module
import shutil
import tempfile
import os

def to_firehose(report, analyzer):
    """ Parser the analyzer report to Firehose format
    :report: The analyzer report
    :returns: create a firehose report inside reports directory
    """

    simple_report_file = "simple_cppcheck_report.xml"
    firehose_report_file = "firehose_%s_report.xml" % analyzer
    report_directory = os.path.join(os.path.abspath("."), "reports/")

    try:
        os.mkdir(report_directory)
    except OSError:
        pass

    tempdir = tempfile.mkdtemp()
    f = open(tempdir + simple_report_file, 'w')
    f.write(report.decode('UTF-8'))
    f.close()

    analyzer_module = import_analyzer_module(analyzer)

    if (analyzer_module):
        tree_analysis = analyzer_module.parse_file(tempdir + simple_report_file).to_xml()
        tree_analysis.write((report_directory  + firehose_report_file), encoding='UTF-8')

    shutil.rmtree(tempdir)

def import_analyzer_module(analyzer):
    """ Import a firehose parser

    analyzer: The name of the parser that will be imported
    :returns: Some firehose parser
    """

    try:
        return import_module("firehose.parsers.%s" % (analyzer))
    except ImportError:
        print("ERROR: Firehose parser %s not found" % analyzer)
