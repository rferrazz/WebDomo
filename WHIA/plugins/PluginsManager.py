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
from ConfigParser import ConfigParser, NoOptionError
import os

DEFAULTSECT = "extension"

class FallToDefConfigParser(ConfigParser):
    '''If an option is not specified it try to get the deault option'''
    def get(self, section, option, raw=False, vars=None):
        try:
            return ConfigParser.get(self, section, option, raw=raw, vars=vars)
        except NoOptionError:
            return self.get(DEFAULTSECT, option, raw, vars)


class PluginsManager(object):
    '''
    Allows discovery of available plugins through a simple query language
    '''


    def __init__(self, pluginsPath="/usr/share/whia/plugins/"):
        '''
        Constructor
        '''
        self.path = pluginsPath
        self.extensions = {}
        for confFile in os.listdir(self.path):
            self.__parseConf(confFile)
            
    def __addExtension(self, type, values):
        try:
            self.extensions[type].append(values)
        except KeyError:
            self.extensions[type] = []
            self.__addExtension(type, values)
            
    def __parseConf(self, file):
        config = FallToDefConfigParser()
        config.read(os.path.join(self.path, file))
        type = config.get("extension", "type")
        values = {"name": config.get("extension", "name"),
                  "version": config.getfloat("extension", "version"),
                  "package": config.get("extension", "package"),
                  "class": config.get("extension", "defClass")}
        values["variants"] = []
        for i in range(100):
            if not config.has_option("variant %d" % (i,), "name"):
                break
            values["variants"].append({"name": config.get("variant %d" % (i,), "name"),
                                       "package": config.get("variant %d" % (i,), "package", values),
                                       "class": config.get("variant %d" % (i,), "class")})
        self.__addExtension(type, values)
                
    def query(self, serviceType="", name="", minVersion=0, variant=None):
        '''
        Returns an array of {name: x, package: x, class: x} 
        '''
        raw = []
        res = []
        for ext in self.extensions[serviceType]:
            if ext["name"] == name and ext["version"] >= minVersion:
                raw.append(ext)
        if variant != None:
            for ext in raw:
                for v in ext["variants"]:
                    if v["name"] == variant:
                        res.append({"name": ext["name"], "package": v["package"], "class": v["class"]})
        else:
            res = raw
        return res

    def createModuleInstanceFromQuery(self, serviceType="", name="", minVersion=0, variant=None, confFile=""):
        '''
        Returns a list of module instances
        '''
        res = []
        for ext in self.query(serviceType, name, minVersion, variant):
            mod = __import__(ext["package"], fromlist=[ext["class"]])
            res.append(getattr(mod, ext["class"])(confFile))
        return res
