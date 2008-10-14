#!/usr/bin/env python
#-------------------------------------------------------------------
# test-mwMIDI: test the mwMIDI module
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

import mwMIDI
import os
import sys
import time
import random

#-------------------------------------------------------------------
# get the program name
#-------------------------------------------------------------------
program = os.path.splitext(os.path.basename(sys.argv[0]))[0]

#-------------------------------------------------------------------
# create the client
#-------------------------------------------------------------------
client = mwMIDI.Client(program)
print "client(%s): %s" % (program, repr(client))

#-------------------------------------------------------------------
# create the source
#-------------------------------------------------------------------
source = mwMIDI.Source(client, "%s-out" % program)
print "source(%s): %s" % ("%s-out" % program, repr(source))

#-------------------------------------------------------------------
# set the note parameters
#-------------------------------------------------------------------
noteMin = 50
noteMax = 80
note = random.randint(noteMin, noteMax)

cValue = random.randint(0,127)

#-------------------------------------------------------------------
# send notes
#-------------------------------------------------------------------
print "Sending notes and control 0 data"
while True:

    #----------------------------------------------------------------
    # calculate the next note
    #----------------------------------------------------------------
    note += random.randint(-2,2)
    
    if note < noteMin: note = noteMin
    if note > noteMax: note = noteMax

    #----------------------------------------------------------------
    # send note on
    #----------------------------------------------------------------
    time.sleep(0.2)
    status = source.send(mwMIDI.NoteOn(0, note, 127))
    
    #----------------------------------------------------------------
    # send note off
    #----------------------------------------------------------------
    time.sleep(0.1)
    source.send(mwMIDI.NoteOff(0, note, 127))
    
    #----------------------------------------------------------------
    # send control change
    #----------------------------------------------------------------
    cValue += random.randint(-10,10)
    if cValue < 0:   cValue = 0
    if cValue > 127: cValue = 127
    
    source.send(mwMIDI.ControlChange(0, 0, cValue))
    