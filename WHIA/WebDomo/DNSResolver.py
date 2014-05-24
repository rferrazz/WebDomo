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
'''TODO: refactor everything to a more object oriented programming'''
'''TODO: client nodes are discovered but not used'''
'''TODO: allow client disconnection whith a more extensive dnssd management'''
import pybonjour, socket
from twisted.internet.interfaces import IReadDescriptor
from zope import interface

#GLOBAL
_port=8787
#END_GLOBAL

class DNSResolver(object):
    def __init__(self, reactor, mode="master", port=8787, capabilities=[]):
        self.reactor = reactor
        self.name = "WebDomo%s" % (mode.capitalize(),)
        sdref = pybonjour.DNSServiceRegister(name = "WebDomo%s" % (mode.capitalize(),),
                                         regtype = "_wd-%s._tcp" % (mode,),
                                         port = port)
        self.reactor.addReader(ServiceDescriptor(sdref))

class ServiceDescriptor(object):
    
    interface.implements(IReadDescriptor)
    
    def __init__(self, sd):
        self.sd = sd
        
    def doRead(self):
        pybonjour.DNSServiceProcessResult(self.sd)
        
    def fileno(self):
        return self.sd.fileno()
    
    def logPrefix(self):
        return "bonjour"
    
    def connectionLost(self, reason):
        self.sd.close()
        
def server_scan(root, reactor):
    def ip_callback(sdRef, flags, interfaceIndex, errorCode, fullname, rrtype, rrclass, rdata, ttl):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            '''TODO: systemWide.addSlave(socket.inet_ntoa(rdata), _port)'''
            pass
            
    def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname, hosttarget, port, txtRecord):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            global _port
            _port = port
            ip_sdref = pybonjour.DNSServiceQueryRecord(interfaceIndex = interfaceIndex,
                                                       fullname = hosttarget,
                                                       rrtype = pybonjour.kDNSServiceType_A,
                                                       callBack = ip_callback)
            reactor.addReader(ServiceDescriptor(ip_sdref))
    
    def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName, regtype, replyDomain):
        if errorCode != pybonjour.kDNSServiceErr_NoError and not (flags & pybonjour.kDNSServiceFlagsAdd):
            return
        resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                    interfaceIndex,
                                                    serviceName,
                                                    regtype,
                                                    replyDomain,
                                                    resolve_callback)
        reactor.addReader(ServiceDescriptor(resolve_sdRef))
    
    browse_sdRef = pybonjour.DNSServiceBrowse(regtype="_wd-slave._tcp", callBack=browse_callback)
    reactor.addReader(ServiceDescriptor(browse_sdRef))