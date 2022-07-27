from abc import ABC
import os
from xml.dom.minidom import parse, parseString, Document, Element, Text
import xml.etree.ElementTree as ET


def getText(nodes):
    rc = []
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
            return ''.join(rc)
        else:
            for n in node.childNodes:
                if n.nodeType == n.TEXT_NODE:
                    rc.append(n.data)
                    return ''.join(rc)

def getDataFromElement(root:Element, tag:str)->str:
    child = root.documentElement.getElementsByTagName(tag)
    data = getText(child)
    return data

class AbcForm(ABC):
    def __init__(self, node:Element):
        self.node = node
        self._nodes = [n for n in node.childNodes if isinstance(n, Element)]

    def fill_data(self):
        pass

class Razdel(AbcForm):
    def __init__(self,
                node:Element,
                idrazdel:str=None,
                date_form:str=None,
                num_resh:str=None,
                grif:str=None):
        super().__init__(node=node)
        self.idrazdel = idrazdel
        self.date_form = date_form
        self.num_resh = num_resh
        self.grif = grif

    def fill_data(self):
        fills={}
        fills['IDRAZDEL'] = self.idrazdel
        fills['DATE_FORM'] = self.date_form
        fills['NUM_RESH'] = self.num_resh
        fills['GRIF'] = self.grif
        for n in self._nodes:
            fills[n.tagName ]=getText(n.childNodes)
        return fills

with open('an_solution.xml', 'rb') as doc:
    doc = doc.read()
    root = parseString(doc)

    test = []
    razdels = root.documentElement.getElementsByTagName('RAZDEL')
    for n in razdels:
        test.append(
            Razdel(n.getElementsByTagName('STR')[0],
            n.getAttribute('IDRAZDEL'),
            getDataFromElement(root,'DATE_FORM'),
            getDataFromElement(root,'NUM_RESH'),
            getDataFromElement(root,'GRIF')
            ).fill_data()
        )
    
    print(test)


"""
RESH:
    -DATE_FORM
    -NUM_RESH
    -GRIF
    -RAZDEL
    -RAZDEL

EXAMPLE:
    -root.childNodes[6].childNodes[1].childNodes[1].childNodes[0].data
    -"RESH"->"RAZDEL"->"STR"->"NUM_SPR_MF"
"""
