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
import json
import xml.dom.minidom as xml
from twisted.web import resource
from WHIA.plugins.PluginsManager import PluginsManager

class WebDomoServer(resource.Resource):
    def __init__(self, plugins=[]):
        resource.Resource.__init__(self)
        self.pluginsManager = PluginsManager()
        for plugin in plugins:
            instances = self.pluginsManager.createModuleInstanceFromQuery("WHIA/Actuator", **plugin)
            for i in instances:
                self.putChild(i.name, i)
            
    def render_GET(self, request):
        return json.dumps(self.children.keys())
    
    def getChild(self, path, request):
        if path == "":
            return self
        else:
            if path in self.children.keys():
                return resource.Resource.getChild(self, path, request)
            else:
                '''TODO: se master vedi se un qualche slave ha il plugin giusto e invia la richiesta'''
                return PageNotFoundError()

class PageNotFoundError(resource.Resource):
    def render_GET(self, request):
        return json.dumps([{"error": "module not found"}])