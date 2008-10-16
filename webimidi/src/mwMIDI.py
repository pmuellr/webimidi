"""Python MIDI interface.

Currently, many constraints:
- only runs on Mac OS X
- only supports Note On, Note Off, Control Change
- only supports writing, not reading
"""

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

__author__  = "Patrick Mueller <pmuellr@yahoo.com>"
__date__    = "2008-10-14"
__version__ = "0.1"

__all__ = [
    "MwMIDIException", "Client", "Source", "MIDIMessage", 
    "NoteOn", "NoteOff", "ControlChange"
]

import time
from ctypes import *

from mwCoreMIDI import *

import simplejson as json

#-------------------------------------------------------------------
class MwMIDIException(Exception):
    """Exception type thrown by code in this module"""
    pass
    
#-------------------------------------------------------------------
class Client(object):
    """Models a client program interacting with MIDI devices.
    
    This is the root of the call chain into the framework.  You will
    need to create one of these objects to send MIDI messages.
    """
    
    #-------------------------------------------------------------------
    def __init__(self, clientName):
        """Create a new instance of this class with the given clientName"""
        
        self.name          = clientName
        self.clientNameRef = CFStringCreateWithCString(cStr=clientName)

        self.client = MIDIClientRef()
        status = MIDIClientCreate(name=self.clientNameRef, outClient=byref(self.client))
        
        if 0 != status:
            raise MwMIDIException, "error creating client '%s': %d" % (clientName, status)
    
    #-------------------------------------------------------------------
    def destroy(self):
        """Destroy this instance"""
        status = MIDIClientDestroy(self.client)
        self.client = None
        return status

#-------------------------------------------------------------------
class Source(object):
    """Models a MIDI source that you send messages to, that some other program reads."""

    #-------------------------------------------------------------------
    def __init__(self, client, sourceName):
        """Create a new instance of this class given the client and name of the MIDI source"""
        
        self.client        = client
        self.name          = sourceName
        self.sourceNameRef = CFStringCreateWithCString(cStr=sourceName)

        self.src = MIDIEndpointRef()
        status = MIDISourceCreate(client=self.client.client, name=self.sourceNameRef, outSrc=byref(self.src))
        
        if 0 != status:
            raise MwMIDIException, "error creating source '%s': %d" % (sourceName, status)
        
    #-------------------------------------------------------------------
    def destroy(self):
        """Destroy this instance"""
        status = MIDIEndpointDispose(self.src)
        self.src = None
        return status

    #-------------------------------------------------------------------
    def send(self, messages):
        """Send a set of MIDIMessage objects to the MIDI device"""
        if   isinstance(messages, list): pass
        elif isinstance(messages, tuple): pass
        else: messages = [messages]
        
        status = -1
        for message in messages:
            status = self.sendMessage(message)
            
        return status

    #-------------------------------------------------------------------
    def sendMessage(self, message):
        """Send a single MIDIMessage object to the MIDI device"""
        
        # print "sendMessage(%s)" % message.toJSON()
        
        midiPacketList = MIDIPacketList()
        midiPacketPtr  = MIDIPacketListInit(byref(midiPacketList))
        midiPacket     = midiPacketPtr.contents

        midiPacket.timestamp = int(time.time())
        midiPacket.length    = 1 + len(message.data)
        midiPacket.data[0]   = message.status + message.channel
        
        dataIndex = 1
        for datum in message.data:
            midiPacket.data[dataIndex] = datum
            dataIndex += 1
            
        MIDIPacketListAdd(midiPacketList, 100, midiPacketPtr.contents, 0, midiPacket.length, midiPacket.data)
        status = MIDIReceived(self.src, midiPacketList)
        
        return status

#-------------------------------------------------------------------
class MIDIMessage(object):
    """Models a MIDI message.
    
    This class is not meant to be instantiated directly, use one of it's subclasses instead.
    """

    #-------------------------------------------------------------------
    @staticmethod
    def fromJSON(jsonString):
        """return an instance of this class from it's JSON representation"""
        jsonObject = json.loads(jsonString)
        
        if 1 != len(jsonObject): raise MwMIDIException, "Invalid JSON MIDI Message: %s" % jsonString
        
        messageType = jsonObject.keys()[0]
        if messageType == "NoteOn":        return NoteOn._fromJSON(jsonObject[messageType])
        if messageType == "NoteOff":       return NoteOff._fromJSON(jsonObject[messageType])
        if messageType == "ControlChange": return ControlChange._fromJSON(jsonObject[messageType])
        
        raise MwMIDIException, "Invalid JSON MIDI Message: %s" % jsonString
    
    #-------------------------------------------------------------------
    def __init__(self, channel, status, databytes):
        """initialize a MIDI message with the channel, status and data bytes."""
        
        self.channel   = channel
        self.status    = status
        self.data      = databytes
        
    #-------------------------------------------------------------------
    def __str__(self):
        """return a string representation of the message."""
        
        string = "MIDIMessage { channel: %2d; status: %2X; data: %s" % (
            self.channel,
            self.status,
            ", ".join([str(x) for x in self.data])
            )
            
        return string

#-------------------------------------------------------------------
class NoteOn(MIDIMessage):
    """Models a MIDI Note On message."""
    
    #-------------------------------------------------------------------
    @staticmethod
    def _fromJSON(jsonObject):
        """return an instance of this class from it's JSON representation"""
        
        if 3 != len(jsonObject): "Invalid JSON MIDI Message: %s" % json.dumps(jsonString)
        if "channel"  not in jsonObject: "Invalid JSON MIDI Message, missing 'channel': %s"  % json.dumps(jsonString)
        if "key"      not in jsonObject: "Invalid JSON MIDI Message, missing 'key': %s"      % json.dumps(jsonString)
        if "velocity" not in jsonObject: "Invalid JSON MIDI Message, missing 'velocity': %s" % json.dumps(jsonString)
        
        return NoteOn(jsonObject["channel"], jsonObject["key"], jsonObject["velocity"])
        
    #-------------------------------------------------------------------
    def __init__(self, channel, key, velocity):
        """Create a new instance of this class with the given channel, key, and velocity."""
        
        if (channel  < 0 or channel  > 15):  raise MwMIDIException, "channel value out of range"
        if (key      < 0 or key      > 127): raise MwMIDIException, "key value out of range"
        if (velocity < 0 or velocity > 127): raise MwMIDIException, "velocity value out of range"
        
        MIDIMessage.__init__(self, channel, 0x90, (key,velocity))
        
        self.key      = key
        self.velocity = velocity
        
    #-------------------------------------------------------------------
    def toJSON(self):
        """Return a JSON representation of this object"""
        result = { "NoteOn" : {
            "channel":  self.channel,
            "key":      self.key,
            "velocity": self.velocity,
            }
        }
        return json.dumps(result)

#-------------------------------------------------------------------
class NoteOff(MIDIMessage):
    """Models a MIDI Note Off message."""
    
    #-------------------------------------------------------------------
    @staticmethod
    def _fromJSON(jsonObject):
        """return an instance of this class from it's JSON representation"""
        
        if 3 != len(jsonObject): "Invalid JSON MIDI Message: %s" % json.dumps(jsonString)
        if "channel"  not in jsonObject: "Invalid JSON MIDI Message, missing 'channel': %s"  % json.dumps(jsonString)
        if "key"      not in jsonObject: "Invalid JSON MIDI Message, missing 'key': %s"      % json.dumps(jsonString)
        if "velocity" not in jsonObject: "Invalid JSON MIDI Message, missing 'velocity': %s" % json.dumps(jsonString)
        
        return NoteOff(jsonObject["channel"], jsonObject["key"], jsonObject["velocity"])
        
    #-------------------------------------------------------------------
    def __init__(self, channel, key, velocity):
        """Create a new instance of this class with the given channel, key, and velocity."""
        
        if (channel  < 0 or channel  > 15):  raise MwMIDIException, "channel value out of range"
        if (key      < 0 or key      > 127): raise MwMIDIException, "key value out of range"
        if (velocity < 0 or velocity > 127): raise MwMIDIException, "velocity value out of range"
        
        MIDIMessage.__init__(self, channel, 0x80, (key,velocity))
        self.key      = key
        self.velocity = velocity

    #-------------------------------------------------------------------
    def toJSON(self):
        """Return a JSON representation of this object"""
        result = { "NoteOff" : {
            "channel":  self.channel,
            "key":      self.key,
            "velocity": self.velocity,
            }
        }
        return json.dumps(result)

#-------------------------------------------------------------------
class ControlChange(MIDIMessage):
    """Models a MIDI Control Change message."""
    
    #-------------------------------------------------------------------
    @staticmethod
    def _fromJSON(jsonObject):
        """return an instance of this class from it's JSON representation"""
        
        if 3 != len(jsonObject): "Invalid JSON MIDI Message: %s" % json.dumps(jsonString)
        if "channel"    not in jsonObject: "Invalid JSON MIDI Message, missing 'channel': %s"  % json.dumps(jsonString)
        if "controller" not in jsonObject: "Invalid JSON MIDI Message, missing 'controller': %s"      % json.dumps(jsonString)
        if "value"      not in jsonObject: "Invalid JSON MIDI Message, missing 'velocity': %s" % json.dumps(jsonString)
        
        return ControlChange(jsonObject["channel"], jsonObject["controller"], jsonObject["value"])
    
    #-------------------------------------------------------------------
    def __init__(self, channel, controller, value):
        """Create a new instance of this class with the given channel, controller, and value."""
        
        if (channel    < 0 or channel    > 15):  raise MwMIDIException, "channel value out of range"
        if (controller < 0 or controller > 127): raise MwMIDIException, "controller value out of range"
        if (value      < 0 or value      > 127): raise MwMIDIException, "value value out of range"
        
        MIDIMessage.__init__(self, channel, 0xB0, (controller,value))
        self.controller = controller
        self.value      = value

    #-------------------------------------------------------------------
    def toJSON(self):
        """Return a JSON representation of this object"""
        result = { "ControlChange" : {
            "channel":    self.channel,
            "controller": self.controller,
            "value":      self.value,
            }
        }
        return json.dumps(result)

