#!/usr/bin/env python
# $Id: $
from copy import deepcopy
from syslog import LOG_ERR, syslog

from Bcfg2.Server.Generator import SingleXMLFileBacked, XMLFileBacked, DirectoryBacked
from Bcfg2.Server.Structure import Structure

from elementtree.ElementTree import Element, XML, tostring

class BaseFile(SingleXMLFileBacked):
    def Index(self):
        self.store = {}
        self.store['Image'] = {}
        self.store['Class']  = {}
        self.store['Host'] = {}
        a = XML(self.data)
        self.entries = a.getchildren()
        for e in self.entries:
            self.store[e.tag][e.attrib['name']] = e.getchildren()

    def Construct(self, metadata):
        r = Element("Independant", version='2.0')
        for entry in self.store['Image'].get(metadata.image, []):
            r.append(deepcopy(entry))
        for c in metadata.classes:
            for entry in self.store['Class'].get(c, []):
                r.append(deepcopy(entry))
        for entry in self.store['Host'].get(metadata.hostname, []):
            r.append(deepcopy(entry))
        return [r]

class base(Structure):
    __name__ =  'base'
    __version__ = '$Id$'
    
    '''base creates independent clauses based on client metadata'''
    def __init__(self, core, datastore):
        Structure.__init__(self, core, datastore)
        self.base = BaseFile("%s/common/base.xml"%(datastore), self.core.fam)
        self.Construct = self.base.Construct
