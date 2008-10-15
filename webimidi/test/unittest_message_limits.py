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

import mwMIDI
import unittest

class Test(unittest.TestCase):
    
    def setUp(self): pass
    def tearDown(self): pass

    def test_NoteOn(self):
        message = mwMIDI.NoteOn( 0,   0,   0)
        message = mwMIDI.NoteOn(15, 127, 127)
        
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOn, -1,  0,  0)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOn,  0, -1,  0)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOn,  0,  0, -1)
        
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOn, 16, 127, 127)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOn, 15, 128, 127)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOn, 15, 127, 128)
        
    def test_NoteOff(self):
        message = mwMIDI.NoteOff( 0,   0,   0)
        message = mwMIDI.NoteOff(15, 127, 127)
        
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOff, -1,  0,  0)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOff,  0, -1,  0)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOff,  0,  0, -1)
        
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOff, 16, 127, 127)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOff, 15, 128, 127)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.NoteOff, 15, 127, 128)

    def test_ControlChange(self):
        message = mwMIDI.ControlChange( 0,   0,   0)
        message = mwMIDI.ControlChange(15, 127, 127)
        
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.ControlChange, -1,  0,  0)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.ControlChange,  0, -1,  0)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.ControlChange,  0,  0, -1)
        
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.ControlChange, 16, 127, 127)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.ControlChange, 15, 128, 127)
        self.assertRaises(mwMIDI.MwMIDIException, mwMIDI.ControlChange, 15, 127, 128)

    def assertNoteXxxEquals(self, message, channel, key, velocity):
        self.assertEqual(channel,  message.channel)
        self.assertEqual(key,      message.key)
        self.assertEqual(velocity, message.velocity)
        
    def assertControlChangeEquals(self, message, channel, controller, value):
        self.assertEqual(channel,    message.channel)
        self.assertEqual(controller, message.controller)
        self.assertEqual(value,      message.value)
        
if __name__ == '__main__':
    unittest.main()

