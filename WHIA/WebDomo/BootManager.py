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
from twisted.internet import reactor
from twisted.web import server
import DNSResolver
from WebDomo import WebDomoServer

class Configurator(object):
    def __init__(self):
        self.mainConf = xml.parse("/etc/whia/whia.conf")
        
    def __getAttributeIfPresent(self, DOMElement, attributeName, nullValue=None):
        try:
            return DOMElement.attributes[attributeName].value
        except KeyError:
            return nullValue
        
    def getServerPort(self):
        portNode = self.mainConf.getElementsByTagName("port")[0]
        return int(portNode.firstChild.data)
    
    def getActuators(self):
        actuators = []
        actuatorsNode = self.mainConf.getElementsByTagName("actuators")[0]
        for act in actuatorsNode.getElementsByTagName("actuator"):
            actuators.append({"name": act.attributes["name"].value,
                              "minVersion": float(self.__getAttributeIfPresent(act, "minVersion", nullValue=0)),
                              "variant": self.__getAttributeIfPresent(act, "variant"),
                              "confFile": act.attributes["file"].value})
        return actuators
    
    def getServerMode(self):
        server = self.mainConf.getElementsByTagName("WebDomoServer")[0]
        return server.attributes["mode"].value
        
class BootManager(object):
    def __init__(self):
        self.config = Configurator()
    
    def startServer(self):
        root = WebDomoServer(self.config.getActuators())
        mode = self.config.getServerMode()
        DNSResolver.DNSResolver(reactor, mode)
        if mode == "master":
            DNSResolver.server_scan(root, reactor)
        srv = server.Site(root)
        reactor.listenTCP(self.config.getServerPort(), srv)
        reactor.run()