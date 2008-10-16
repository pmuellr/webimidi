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
import optparse

import wsgiref
import wsgiref.simple_server
import mimetypes

import simplejson as json

import mwMIDI

__author__  = "Patrick Mueller <pmuellr@yahoo.com>"
__date__    = "2008-10-14"
__version__ = "0.1"

program = os.path.splitext(os.path.basename(sys.argv[0]))[0]

#-------------------------------------------------------------------
def help():
    print "%s - %s" % (program, __version__)
    print "usage: %s port device-dir" % program
    print ""
    print "port:       port to run the HTTP server should be run on"
    print "device-dir: directory containing the devices to create"
    
    sys.exit()

#-------------------------------------------------------------------
class Context:
    pass

#-------------------------------------------------------------------
def handler_root(environ, start_response, matches):
    status           = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)

    output = StringIO.StringIO()
    output.write("<h1>webimidi: root</h1>\n")
    output.write("<h2><a href='devices.html'>devices</a></h2>")
    output.write("<h2><a href='environ.html'>environ</a></h2>")

    result = output.getvalue()
    output.close()
    return [result]
        
#-------------------------------------------------------------------
def handler_devices_html(environ, start_response, matches):
    status           = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)

    output = StringIO.StringIO()
    output.write("<h1>devices</h1>\n")
    output.write("<p><i><a href='/'>go home</a></i></p>\n")
    
    for device in context.devices.keys():
        output.write("<h2><a href='devices/%s/'>%s</a></h2>" % (device, device))

    result = output.getvalue()
    output.close()
    return [result]
        
#-------------------------------------------------------------------
def handler_devices_json(environ, start_response, matches):
    status           = '200 OK'
    response_headers = [('Content-type','text/json')]
    start_response(status, response_headers)

    result = context.devices.keys()
    output = StringIO.StringIO()
    output.write(json.dumps(result))
    
    result = output.getvalue()
    output.close()
    
    return [result]

#-------------------------------------------------------------------
def handler_device_root(environ, start_response, matches):
    device = context.devices.get(matches["device"], None)
    if not device: 
        return handler_bad_status(environ, start_response, 404, "Not Found")
    
    file_name = context.device_dir + "/" + device.name + "/index.html"
    
    if not os.path.exists(file_name):
        return handler_bad_status(environ, start_response, 404, "Not Found")
    
    status           = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)

    return wsgiref.util.FileWrapper(file(file_name))
        
#-------------------------------------------------------------------
def handler_device_io(environ, start_response, matches):
    request_method = environ["REQUEST_METHOD"]
    if (request_method != "POST"): 
        return handler_bad_status(environ, start_response, 405, "Method Not Allowed")
    
    device = context.devices.get(matches["device"], None)
    if not device: 
        return handler_bad_status(environ, start_response, 404, "Not Found")
    
    content_type = environ["CONTENT_TYPE"]
    if not content_type:
        return handler_bad_status(environ, start_response, 406, "Not Acceptable")
    
    if not re.match(r".*/json$", content_type):
        return handler_bad_status(environ, start_response, 415, "Unsupported Media Type")
              
    input = environ["wsgi.input"]                        
    message = input.read(int(environ['CONTENT_LENGTH']))
    input.close()
    
    try:
        midi_message = mwMIDI.MIDIMessage.fromJSON(message)
    except Exception, value:
        return handler_bad_status(environ, start_response, 406, "Not Acceptable")
    
    device.sendMessage(midi_message)
    
    status           = '200 OK'
    response_headers = [('Content-type','text/plain')]
    start_response(status, response_headers)
    
    return ["OK"]
        
#-------------------------------------------------------------------
def handler_device_file(environ, start_response, matches):
    device = context.devices.get(matches["device"], None)
    if not device: 
        return handler_bad_status(environ, start_response, 404, "Not Found")
    
    file_name = context.device_dir + "/" + device.name + "/" + matches["file"]
    
    if not os.path.exists(file_name):
        return handler_bad_status(environ, start_response, 404, "Not Found")
    
    (content_type, encoding) = mimetypes.guess_type(file_name)
    if not content_type:
        content_type = "application/octet-stream"
        
    status           = '200 OK'
    response_headers = [('Content-type', content_type)]
    start_response(status, response_headers)

    return wsgiref.util.FileWrapper(file(file_name))
        
#-------------------------------------------------------------------
def handler_devices_update(environ, start_response, matches):
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
def handler_environ_html(environ, start_response, matches):
    
    status           = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)
    
    output = StringIO.StringIO()
    output.write("<h1>environ</h1>\n")
    output.write("<p><i><a href='/'>go home</a></i></p>\n")
    output.write("<table>\n")
    for k, v in environ.iteritems():
        output.write("<tr><td>%s</td><td>&nbsp;&nbsp;</td><td>%s</td></tr>\n" % (k,v))
    output.write("<table>\n")
    
    result = output.getvalue()
    output.close()
    return [result]

#-------------------------------------------------------------------
def handler_bad_status(environ, start_response, status, message):
    
    status           = '%s %s' % (status, message)
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)
    
    return ["<p>HTTP Status: %s</p>" % (status)]
        
#-------------------------------------------------------------------
def webimidi_app(environ, start_response):
    pathInfo = environ["PATH_INFO"]
    
    handler_list = [
        (r"^/$",                                        handler_root),
        (r"^/devices\.html$",                           handler_devices_html),
        (r"^/devices\.json$",                           handler_devices_json),
        (r"^/devices\.update$",                         handler_devices_update),
        (r"^/devices/(?P<device>[^/]+)/$",              handler_device_root),
        (r"^/devices/(?P<device>[^/]+)/io$",            handler_device_io),
        (r"^/devices/(?P<device>[^/]+)/(?P<file>.+)$",  handler_device_file),
        (r"^/environ\.html$",                           handler_environ_html),
    ]
    
    handler_list = [(re.compile(handler[0]), handler[1]) for handler in handler_list]
    
    for handler in handler_list:
        (urlPattern, handlerFunction) = handler
        match = urlPattern.match(pathInfo)
        if not match: continue
        
        return handlerFunction(environ, start_response, match.groupdict())
    
    return handler_bad_status(environ, start_response, 404, "Not Found")

#-------------------------------------------------------------------
def context_init():
    if len(sys.argv) < 3: help()

    context = Context()
    
    port_string        = sys.argv[1]
    dir_string         = sys.argv[2]
    
    if not port_string.isdigit():
        raise Error, "port parameter is not numeric"
    
    context.port       = int(port_string)
    context.device_dir = dir_string
    context.devices    = {}

    client_name = "localhost-%d" % context.port
    context.client = mwMIDI.Client(client_name)

    update_devices(context)
    
    return context

#-------------------------------------------------------------------
def update_devices(context):
    
    old_device_list = set(context.devices.keys())
    new_device_list = set(os.listdir(context.device_dir))
    
    new_device_list = filter(lambda device: not device.startswith("."), new_device_list)
    new_device_list = set(new_device_list)
    
    new_device_names = new_device_list - old_device_list
    old_device_names = old_device_list - new_device_list
    
    for device_name in new_device_names:
        device = mwMIDI.Source(context.client, device_name)
        context.devices[device_name] = device
     
    for device_name in old_device_names:
        device = context.devices[device_name]
        device.destroy()
        del context.devices[device_name]
     

#-------------------------------------------------------------------
# main program
#-------------------------------------------------------------------

context = context_init()

print "Devices created:"
for device_name in context.devices.keys():
    print "   %s" % device_name
print
    
#-------------------------------------------------------------------

httpd = wsgiref.simple_server.make_server('', context.port, webimidi_app)
print "Starting server at http://127.0.0.1:%d" % context.port

httpd.serve_forever()
