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

import sys
from ctypes import *
import ctypes.util

CoreFoundation = ctypes.util.find_library("CoreFoundation")
CoreMIDI       = ctypes.util.find_library("CoreMIDI")

if not CoreFoundation: raise Error, "unable to find the CoreFoundation framework"
if not CoreMIDI:       raise Error, "unable to find the CoreMIDI framework"

CoreFoundation = CDLL(CoreFoundation)
CoreMIDI       = CDLL(CoreMIDI)

if not CoreFoundation: raise Error, "unable to load the CoreFoundation framework"
if not CoreMIDI:       raise Error, "unable to load the CoreMIDI framework"

#-------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------

kCFStringEncodingUTF8   = 0x08000100

kMIDIInvalidClient		= -10830
kMIDIInvalidPort		= -10831
kMIDIWrongEndpointType	= -10832
kMIDINoConnection		= -10833
kMIDIUnknownEndpoint	= -10834
kMIDIUnknownProperty	= -10835
kMIDIWrongPropertyType	= -10836
kMIDINoCurrentSetup		= -10837
kMIDIMessageSendErr		= -10838
kMIDIServerStartErr		= -10839
kMIDISetupFormatErr		= -10840
kMIDIWrongThread		= -10841
kMIDIObjectNotFound		= -10842
kMIDIIDNotUnique		= -10843

#-------------------------------------------------------------------
# simple typedefs
#-------------------------------------------------------------------
        
OSStatus                  = c_int16
MIDIObjectRef             = c_uint32
MIDIClientRef             = MIDIObjectRef
MIDIEndpointRef           = MIDIObjectRef
MIDITimeStamp             = c_uint64
ByteCount                 = c_uint32
Byte                      = c_ubyte
CFAbsoluteTime            = c_double
CFAllocatorRef            = c_void_p
CFStringRef               = c_void_p
CFStringEncoding          = c_uint32
CFIndex                   = c_int32

#-------------------------------------------------------------------
# struct MIDIPacket{}
#-------------------------------------------------------------------

class MIDIPacket(ctypes.Structure):
    pass
MIDIPacket._fields_ = [
    ("timestamp",   MIDITimeStamp),
    ("length",      ctypes.c_uint16),
    ("data",        ctypes.c_uint8 * 3),
]

#-------------------------------------------------------------------
# struct MIDIPacketList{}
#-------------------------------------------------------------------

class MIDIPacketList(ctypes.Structure):
    pass
MIDIPacketList._fields_ = [
    ("length",      ctypes.c_uint32),
    ("packet",      MIDIPacket * 1),
]

#-------------------------------------------------------------------
# CFAbsoluteTimeGetCurrent()
#-------------------------------------------------------------------

_prototype = CFUNCTYPE(CFAbsoluteTime)

CFAbsoluteTimeGetCurrent = _prototype(("CFAbsoluteTimeGetCurrent", CoreFoundation))

#-------------------------------------------------------------------
# CFStringCreateWithCString()
#-------------------------------------------------------------------

_prototype = CFUNCTYPE(CFStringRef, CFAllocatorRef, c_char_p, CFStringEncoding)
_paramflags = (
    (1, "alloc", None), 
    (1, "cStr"),
    (1, "encoding", kCFStringEncodingUTF8),
)
    
CFStringCreateWithCString = _prototype(("CFStringCreateWithCString", CoreFoundation), _paramflags)
    
#-------------------------------------------------------------------
# MIDIClientCreate()
#-------------------------------------------------------------------

_prototype = CFUNCTYPE(OSStatus, CFStringRef, c_void_p, c_void_p, POINTER(MIDIClientRef))
_paramflags = (
    (1, "name"), 
    (1, "notifyProc", None),
    (1, "notifyRefCon", None),
    (1, "outClient"),
)

MIDIClientCreate = _prototype(("MIDIClientCreate", CoreMIDI), _paramflags)
    
#-------------------------------------------------------------------
# MIDIClientDispose()
#-------------------------------------------------------------------

_prototype = CFUNCTYPE(OSStatus, MIDIClientRef)
_paramflags = (
    (1, "client"), 
)

MIDIClientDispose = _prototype(("MIDIClientDispose", CoreMIDI), _paramflags)
    
#-------------------------------------------------------------------
# MIDISourceCreate()
#-------------------------------------------------------------------

_prototype = CFUNCTYPE(OSStatus, MIDIClientRef, CFStringRef, POINTER(MIDIEndpointRef))
_paramflags = (
    (1, "client"), 
    (1, "name"),
    (1, "outSrc"),
)

MIDISourceCreate = _prototype(("MIDISourceCreate", CoreMIDI), _paramflags)

#-------------------------------------------------------------------
# MIDIEndpointDispose()
#-------------------------------------------------------------------

_prototype = CFUNCTYPE(OSStatus, MIDIEndpointRef)
_paramflags = (
    (1, "endpt"), 
)

MIDIEndpointDispose = _prototype(("MIDIEndpointDispose", CoreMIDI), _paramflags)

#-------------------------------------------------------------------
# MIDIPacketListInit()
#-------------------------------------------------------------------

_prototype = CFUNCTYPE(POINTER(MIDIPacket), POINTER(MIDIPacketList))
_paramflags = (
    (1, "pktlist"), 
)

MIDIPacketListInit = _prototype(("MIDIPacketListInit", CoreMIDI), _paramflags)

#-------------------------------------------------------------------
# MIDIPacketListAdd()
#-------------------------------------------------------------------

_prototype = CFUNCTYPE(POINTER(MIDIPacket), POINTER(MIDIPacketList), ByteCount, POINTER(MIDIPacket), MIDITimeStamp, ByteCount, POINTER(Byte))
_paramflags = (
    (1, "pktlist"), 
    (1, "listSize"), 
    (1, "curPacket"), 
    (1, "time", 0), 
    (1, "nData"), 
    (1, "data"),
)

MIDIPacketListAdd = _prototype(("MIDIPacketListAdd", CoreMIDI), _paramflags)

#-------------------------------------------------------------------
# MIDIReceived()
#-------------------------------------------------------------------

_prototype = CFUNCTYPE(OSStatus, MIDIEndpointRef, POINTER(MIDIPacketList))
_paramflags = (
    (1, "src"), 
    (1, "pktlist"), 
)

MIDIReceived = _prototype(("MIDIReceived", CoreMIDI), _paramflags)

