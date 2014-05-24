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
import pyduino

class ArduinoActuator(DomoActuator):
    def __init__(self, applianceFile):
        DomoActuator.__init__(self, applianceFile)
        self.arduino = pyduino.Arduino(str(self.port))
        self.__setupOutput()
    
    def put(self, *subtypes, **parameters):
        if parameters["state"] == "on":
            state = 1
        elif parameters["state"] == "off":
            state = 0
        else:
            return False
        apps = self.getAppliance(*subtypes)
        for a in apps:
            self.arduino.digital[int(a.pin)].write(state)
            a.state = parameters["state"]
        return True
        
    def __setupOutput(self):
        for v in self.getAppliance():
            self.arduino.digital_ports[int(v.pin) >> 3].set_active(1)
            self.arduino.digital[int(v.pin)].set_mode(pyduino.DIGITAL_OUTPUT)
    
    def applianceSwitch(self, appliance, state):
        pin = self.__getPin(appliance)
        self.arduino.digital[pin].write(state)