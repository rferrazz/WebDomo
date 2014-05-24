'''
Copyright (C) 2013 Riccardo Ferrazzo <f.riccardo87@gmail.com>

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
from ola.ClientWrapper import ClientWrapper
import array

class DMXActuator(DomoActuator):
    def __init__(self, applianceFile):
        DomoActuator.__init__(self, applianceFile)
        self.universe = int(self.universe)
        self.wrapper = ClientWrapper()
        self.client = self.wrapper.Client()
        self.data = array.array('B')
        
    def sent(self):
        self.wrapper.Stop()
    
    def put(self, *subtypes, **parameters):
        if "values" not in parameters.keys():
            return False
        values = eval(parameters["values"])
        for app in self.getAppliance(*subtypes):
            if int(app.channels) > 1 and len(values) > int(app.channels):
                return False
            new = [0]*(int(app.offset)-1)
            if type(values).__name__ == 'int':
                new.append(values)
            else:
                for val in values:
                    new.append(val)
            for i in range(len(new)):
                try:
                    if new[i] != self.data[i] and new[i] != 0:
                        self.data[i] = new[i]
                except Exception:
                    self.data.append(new[i])
        self.client.SendDmx(self.universe, self.data, lambda *args, **kwargs: self.sent())
        self.wrapper.Run()
        return True
    
    def get(self, *subtypes, **parameters):
        apps = self.getAppliance(*subtypes, **parameters)
        res = []
        for a in apps:
            app = a.render()
            data = self.data[int(a.offset)-1:int(a.offset)+int(a.channels)-1]
            app["values"] = data.tolist()
            res.append(app)
        return res