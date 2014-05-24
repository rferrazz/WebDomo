'''
Copyright (C) 2012 Riccardo Ferrazzo <f.riccardo87@gmail.com>

This file is part of WebDomo.

    WebDomo is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    WebDomo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with WebDomo.  If not, see <http://www.gnu.org/licenses/>
'''
import xml.dom.minidom as xml
from twisted.web import resource

import json

class Appliance(object):
    '''Appliance descriptor'''
    
    def __init__(self, name, subtypes):
        self.name = name
        self.subtypes = subtypes
        
    def match(self, *args, **vs):
        keys = vs.keys()
        for a in args:
            if a not in self.subtypes and a != self.name:
                return False
        for k in keys:
            if vs[k] != self.__dict__[k]:
                return False
        return True
    
    def render(self):
        return self.__dict__
                
class DomoActuator(resource.Resource):
    '''Base class for every actuator'''
    
    def __init__(self, *args, **kwargs):
        '''
        An actuator can be instanciated in two ways
        1. with a config file
        2. manually putting the name of the actuator and leaf to True or False
        '''
        if "leaf" in kwargs.keys():
            return self.__initName(*args, **kwargs)
        return self.__initFile(*args)
    
    def __initName(self, name, leaf=True):
        resource.Resource.__init__(self)
        self.isLeaf = leaf
        self.name = name
    
    def __initFile(self, applianceFile):
        resource.Resource.__init__(self)
        self.isLeaf = True
        '''loads every appliance from an XML file'''
        doc = xml.parse(applianceFile)
        actuator = doc.getElementsByTagName("actuator")[0]
        self.name = actuator.attributes["type"].value
        '''setting object variables'''
        for var in actuator.getElementsByTagName("var"):
            setattr(self, var.attributes["name"].value, var.attributes["value"].value)
        '''adding appliances'''
        self.appliances = []
        node = actuator.firstChild
        while True:
            if node.nodeType == xml.Node.ELEMENT_NODE and node.tagName == "subtype":
                self.parseTree(node, [])
                return
            node = node.nextSibling
            if node == None:
                break
        self.appliances.append(self.parseAppliancesLevel(doc.getElementsByTagName("appliance")[0]))
        return
    
    def parseTree(self, root, subtypesList):
        if root.tagName == "appliance":
            self.parseAppliancesLevel(root, subtypesList)
            return
        subtypesList.append(root.attributes["name"].value)
        for node in root.childNodes:
            if node.nodeType == xml.Node.ELEMENT_NODE:
                self.parseTree(node, subtypesList[:])
        return
    
    def parseAppliancesLevel(self, element, subtypesList=[]):
        name = element.attributes["name"].value
        app = Appliance(name, subtypesList)
        for var in element.getElementsByTagName("var"):
            setattr(app, var.attributes["name"].value,
                       var.attributes["value"].value)
        self.appliances.append(app)
        
    def getAppliance(self, *subtypes, **parameters):
        result = []
        for a in self.appliances:
            if a.match(*subtypes, **parameters):
                result.append(a)
        return result
    
    def get(self, *subtypes, **parameters):
        '''basic get method'''
        apps = self.getAppliance(*subtypes, **parameters)
        res = []
        for a in apps:
            res.append(a.render())
        return res
    
    def put(self, *subtypes, **parameters):
        '''
        Act on the appliance
        subtypes = list of appliance subtypes
        parameters = dictionary of parameters on wich you have to act
        '''
        raise NotImplementedError();
    
    def __normalizeArgs(self, request):
        if len(request.postpath) > 0 and request.postpath[-1] == "":
            request.postpath.pop(-1)
        for k in request.args.keys():
            request.args[k] = request.args[k][0]
    
    def render_GET(self, request):
        self.__normalizeArgs(request)
        res = self.get(*request.postpath, **request.args)
        if not res:
            return json.dumps([{"result": False}])
        return json.dumps(res)
    
    def render_PUT(self, request):
        self.__normalizeArgs(request)
        res = self.put(*request.postpath, **request.args)
        return json.dumps([{"result": res}])