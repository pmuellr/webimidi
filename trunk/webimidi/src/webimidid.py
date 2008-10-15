#!/usr/bin/env python

#-------------------------------------------------------------------
# 
# The MIT License
# 
# Copyright (c) 2008 Patrick Mueller
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
#-------------------------------------------------------------------

import os
import sys
import re
import StringIO

import wsgiref
import wsgiref.simple_server

import mwMIDI

__author__  = "Patrick Mueller <pmuellr@yahoo.com>"
__date__    = "2008-10-14"
__version__ = "0.1"

program = os.path.splitext(os.path.basename(sys.argv[0]))[0]

#-------------------------------------------------------------------
def help():
    print "%s - %s" % (program, __version__)
    print "usage: %s config-file" % program
    sys.exit()
    
#-------------------------------------------------------------------
class Config:
    def __init__(self, config_file_name):
        config_file = file(config_file_name)
        contents = config_file.read()
        config_file.close()
        
        exec contents
        self.port    = port
        self.devices = devices

#-------------------------------------------------------------------
def handler_root(environ, start_response):
    status           = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)

    output = StringIO.StringIO()
    output.write("<h1>webimidi: root</h1>\n")
    output.write("<h2><a href='devices/'>devices</a></h2>")
    output.write("<h2><a href='environ/'>environ</a></h2>")

    result = output.getvalue()
    output.close()
    return [result]
        
#-------------------------------------------------------------------
def handler_devices_root(environ, start_response):
    status           = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)

    output = StringIO.StringIO()
    output.write("<h1>devices</h1>\n")
    
    for device in config.devices:
        output.write("<h2><a href='devices/%s'>%s</a></h2>" % (device.name(), device.name()))

    result = output.getvalue()
    output.close()
    return [result]
        
#-------------------------------------------------------------------
def handler_environ(environ, start_response):
    
    status           = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)
    
    output = StringIO.StringIO()
    output.write("<h1>environ</h1>\n")
    output.write("<table>\n")
    for k, v in environ.iteritems():
        output.write("<tr><td>%s</td><td>&nbsp;&nbsp;</td><td>%s</td></tr>" % (k,v))
    output.write("<table>\n")
    
    result = output.getvalue()
    output.close()
    return [result]
        
#-------------------------------------------------------------------
def handler_404(environ, start_response):
    
    status           = '404 Not Found'
    response_headers = [('Content-type','text/plain')]
    start_response(status, response_headers)
    
    return ["what you talking about?"]
        
#-------------------------------------------------------------------
def webimidi_app(environ, start_response):
    pathInfo = environ["PATH_INFO"]
    
    handler_list = [
        (r"^/$",         handler_root),
        (r"^/devices/$", handler_devices_root),
        (r"^/environ/$", handler_environ)
    ]
    
    handler_list = [(re.compile(handler[0]), handler[1]) for handler in handler_list]
    
    for handler in handler_list:
        (urlPattern, handlerFunction) = handler
        if None == urlPattern.search(pathInfo): continue
        
        return handlerFunction(environ, start_response)
    
    return handler_404(environ, start_response)
            
#-------------------------------------------------------------------
if len(sys.argv) < 2: help()

config_file_name = sys.argv[1]
config = Config(config_file_name)

#-------------------------------------------------------------------
client = mwMIDI.Client("127.0.0.1:%d" % config.port)

config.devices = [mwMIDI.Source(client,device) for device in config.devices]
config.deviceMap = {}
for device in config.devices:
    config.deviceMap[device.name()] = device

print "Devices created:"
for device in config.devices:
    print "   %s" % device.name()
print
    
#-------------------------------------------------------------------

httpd = wsgiref.simple_server.make_server('', config.port, webimidi_app)
print "Starting server at http://127.0.0.1:%d" % config.port

httpd.serve_forever()
