"""Firehose static analysis report format converter.

Module providing functions to convert analysis reports to the firehose format.
"""

from importlib import import_module
import io
import json


def to_firehose(bytes_input, analyzer):
    """Parser the analyzer report to Firehose format.

    :bytes_input: The analyzer report, as a byte string
    :returns: A json as string.
    """
    in_memory_file = io.StringIO(str(bytes_input, 'utf-8'))
    analyzer_module = import_firehose_parser(analyzer)
    analysis = analyzer_module.parse_file(in_memory_file)
    analysis_as_json = analysis.to_json()
    return json.dumps(analysis_as_json)


def import_firehose_parser(parser):
    """Import a firehose parser.

    parser: The name of the parser that will be imported
    :returns: Some firehose parser
    """
    try:
        return import_module("firehose.parsers.%s" % (parser))
    except ImportError:
        print("ERROR: Firehose parser %s not found" % parser)
