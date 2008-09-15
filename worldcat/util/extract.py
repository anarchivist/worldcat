# Copyright (C) 2008 Mark A. Matienzo
# 
# This file is part of worldcat, the Python WorldCat API module.
# 
# worldcat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# worldcat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with worldcat.  If not, see <http://www.gnu.org/licenses/>.

# util/srumarc.py - Parse SRU response XML into pymarc objects

from xml.sax import make_parser
from xml.sax.handler import ContentHandler, feature_namespaces

try:
    import xml.etree.ElementTree as ET  # builtin in Python 2.5
except ImportError:
    import elementtree.ElementTree as ET

import pymarc

from worldcat.exceptions import ExtractError

def parse_xml_string(xml_string, handler):
    """comparable function to pymarc's parse_xml; push to pymarc eventually"""
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setFeature(feature_namespaces, 1)
    parser.parseString(xml_string)

def ns_extract(xml, element='{http://www.loc.gov/MARC21/slim}record',
                return_as='string'):
    """worldcat.util.ns_extract: extract elements based on namespace"""
    tree = ET.fromstring(xml)
    elements = tree.getiterator(element)
    records = [ET.tostring(record) for record in extracted]
    if return_as is 'string':
        return ''.join(records)
    elif return_as is 'string_list':
        return records
    elif return_as is 'element_list':
        return elements
    else:
        raise ExtractError("Can't extract to format %s" % return_as)

def pymarc_extract(xml):
    records = ns_extract(xml)
    handler = pymarc.XmlHandler()
    parse_xml_string(records, handler)
    return handler.records