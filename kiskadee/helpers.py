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
import json

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
    f = open(file_to_parse, 'w')
    f.write(bytes_input.decode('UTF-8'))
    f.close()

    analyzer_module = import_analyzer_module(analyzer)

    if (analyzer_module):
        analyzer_report_file = report_directory  + firehose_report_file
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

def load_config(plugin):
    """Read the plugin config
    :plugin: The name of the plugin
    :returns: A dict with the plugin configuration
    """

    config_path = 'kiskadee/plugins/config.json'
    f = open(config_path, 'r')
    try:
        data = json.load(f)
        return data[plugin]
        f.close()
    except KeyError:
        f.close()
        return {}

