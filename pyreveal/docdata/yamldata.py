"""
YAML Meta-Data

Extracts, parses and transforms YAML style data from documents.

"""


import re
import yaml
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


BLOCK_RE = re.compile(r'^-{3}[ \t]*\n(.*?\n)(?:\.{3}|-{3})[ \t]*\n', re.UNICODE|re.DOTALL)


def get_data(doc):
    """
    Extract meta-data from a text document.

    Returns a tuple of document and data.
    """
    data = {}
    m = BLOCK_RE.match(doc)
    if m:
        try:
            data = yaml.load(m.group(1), SafeLoader)
            if isinstance(data, dict):
                doc = doc[m.end():].lstrip('\n')
            else:
                data = {}
        except:
            pass
    return doc, data