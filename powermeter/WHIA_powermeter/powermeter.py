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

import serial, struct

class PowerMeter(object):
    def __init__(self, port):
        self.serial = serial.Serial(port, 115200, timeout=2)
        
    def __isValid(self, measure, checksum):
        return True
    
    def __readNumber(self):
        readed = []
        for i in range(4):
            readed.append(self.serial.read())
        checksum = self.serial.read()
        if self.__isValid(readed, checksum):
            return struct.unpack(">I", readed[3]+readed[2]+readed[1]+readed[0])[0]
        
    def getPower(self):
        self.serial.write("A")
        return self.__readNumber()
    
    def getEnergy(self):
        self.serial.write("B")
        readed = [0,0,0]
        for i in range(3):
            readed[i] = self.__readNumber()
        res = readed[2]+100*readed[1]+10000*readed[0]
        return res
    
    def __getFloatValues(self, msg):
        """TODO: wrong implementation"""
        self.serial.write(msg)
        readed = []
        for i in range(200):
            readed.append('')
            for j in range(4):
                readed[i] = self.serial.read()+readed[i]
            readed[i] = struct.unpack("f", readed[i])
        return readed
    
    def getVoltage(self):
        return 0 #self.__getFloatValues("C")
    
    def getCurrent(self):
        return 0 #self.__getFloatValues("D")
    
    def close(self):
        self.serial.close()