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

from ctypes import *
from mwCoreMIDI import *

import sys
import os

#-------------------------------------------------------------------
# get the program name
#-------------------------------------------------------------------
program = os.path.splitext(os.path.basename(sys.argv[0]))[0]

#-------------------------------------------------------------------
# build the client and MIDI source names
#-------------------------------------------------------------------
clientString = program
sourceString = "%s-out" % program

#-------------------------------------------------------------------
# allocate the strings for the names
#-------------------------------------------------------------------
clientStringRef = CFStringCreateWithCString(cStr = clientString)
sourceStringRef = CFStringCreateWithCString(cStr = sourceString)

#-------------------------------------------------------------------
# create the MIDIClient
#-------------------------------------------------------------------
client = MIDIClientRef()
status = MIDIClientCreate(name=clientStringRef, outClient=byref(client))
print "MIDIClientCreate(%s): %d" % (clientString, status)

#-------------------------------------------------------------------
# create the MIDISource
#-------------------------------------------------------------------
src = MIDIEndpointRef()
status = MIDISourceCreate(client=client, name=sourceStringRef, outSrc=byref(src))
print "MIDISourceCreateCreate(%s): %d" % (sourceString, status)

import time
import random

#-------------------------------------------------------------------
# send notes
#-------------------------------------------------------------------
midiPacketList = MIDIPacketList()

print "Sending notes ..."
while True:
    
    #----------------------------------------------------------------
    # the note to play  
    #----------------------------------------------------------------
    note = random.randint(40,80)
    
    #----------------------------------------------------------------
    # note on
    #----------------------------------------------------------------
    time.sleep(0.1)
    
    midiPacketPtr = MIDIPacketListInit(byref(midiPacketList))
    midiPacket    = midiPacketPtr.contents
    
    midiPacket.timestamp = 0
    midiPacket.length    = 3
    midiPacket.data[0]   = 0x90
    midiPacket.data[1]   = note
    midiPacket.data[2]   = 127        
    
    MIDIPacketListAdd(midiPacketList, 100, midiPacketPtr.contents, 0, 3, midiPacket.data)
    MIDIReceived(src, midiPacketList)
    
    #----------------------------------------------------------------
    # note off 
    #----------------------------------------------------------------
    time.sleep(0.1)
    
    midiPacketPtr = MIDIPacketListInit(byref(midiPacketList))
    midiPacket    = midiPacketPtr.contents
    
    midiPacket.timestamp = 0
    midiPacket.length    = 3
    midiPacket.data[0]   = 0x80
    midiPacket.data[1]   = note
    midiPacket.data[2]   = 127
    
    MIDIPacketListAdd(midiPacketList, 100, midiPacketPtr.contents, 0, 3, midiPacket.data)
    MIDIReceived(src, midiPacketList)
    