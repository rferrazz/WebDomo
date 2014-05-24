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

from WHIA.plugins.Actuator import DomoActuator
from powermeter import PowerMeter

class PowermeterActuator(DomoActuator):
    def __init__(self, applianceFile):
        DomoActuator.__init__(self, applianceFile)
        self.powermeters = {}
        for app in self.getAppliance():
            self.powermeters[app.name] = PowerMeter(str(app.port))
        
    def get(self, *subtypes, **parameters):
        results = []
        apps = self.getAppliance(*subtypes, **parameters)
        for a in apps:
            vars = a.__dict__
            vars["power"] = self.powermeters[a.name].getPower()
            vars["energy"] = self.powermeters[a.name].getEnergy()
            vars["current"] = self.powermeters[a.name].getCurrent()
            vars["voltage"] = self.powermeters[a.name].getVoltage()
            results.append(vars)
        return results
    
    def put(self, *subtypes, **parameters):
        "It is a readonly device"
        return False
            