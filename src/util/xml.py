"""
__author__ = "Patrick Renner"
__copyright__ = "Copyright 2020, Pomfort GmbH"
__credits__ = ["Jon Waggoner"]

__license__ = "MIT"
__maintainer__ = "Patrick Renner"
__email__ = "opensource@pomfort.com"
"""

from lxml import etree


def strip_ns_prefix(tree):
    # xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    # for each element returned by the above xpath query...
    for element in tree.xpath(query):
        # replace element name with its local name
        element.tag = etree.QName(element).localname
    return tree
