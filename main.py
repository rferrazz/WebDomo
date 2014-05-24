#!/usr/bin/env python
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
from WHIA.WebDomo.BootManager import BootManager
from WHIA.WebDomo.daemonizer import createDaemon
import argparse

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Server that provides a set of RESTFUL API")
    parser.add_argument('-d', dest='daemon', action='store_true', help="Execute WebDomo as a daemon")
    
    args = parser.parse_args()
    if args.daemon:
        createDaemon()
        
    bootManager = BootManager() 
    bootManager.startServer()