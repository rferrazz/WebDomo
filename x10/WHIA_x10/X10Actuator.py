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
from x10.controllers import cm11, cm15, cm17a
        
class X10CM11Actuator(DomoActuator):
    def __init__(self, applianceFile):
        DomoActuator.__init__(self, applianceFile)
        self.controller = cm11.CM11(str(self.port))
        self.controller.open()
        
    def put(self, *subtypes, **parameters):
        apps = self.getAppliance(*subtypes)
        for a in apps:
            act = self.controller.actuator(a.housecode+a.unitcode)
            call = getattr(act, parameters["state"])
            call()
            a.state = parameters["state"]
        return True