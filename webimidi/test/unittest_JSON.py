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

import simplejson as json
import mwMIDI
import unittest

class TestJSON(unittest.TestCase):
    
    def setUp(self): pass
    def tearDown(self): pass

    def test_NoteOn(self):
        message1 = mwMIDI.NoteOn(0, 63, 127)
        json     = message1.toJSON()
        message2 = mwMIDI.MIDIMessage.fromJSON(json)
        
        self.assert_(isinstance(message2, mwMIDI.NoteOn))
        self.assertEqual(0,   message2.channel)
        self.assertEqual(63,  message2.key)
        self.assertEqual(127, message2.velocity)

    def test_NoteOff(self):
        message1 = mwMIDI.NoteOff(15, 0, 63)
        json     = message1.toJSON()
        message2 = mwMIDI.MIDIMessage.fromJSON(json)
        
        self.assert_(isinstance(message2, mwMIDI.NoteOff))
        self.assertEqual(15, message2.channel)
        self.assertEqual(0,  message2.key)
        self.assertEqual(63, message2.velocity)

    def test_ControlChange(self):
        message1 = mwMIDI.ControlChange(7, 127, 0)
        json     = message1.toJSON()
        message2 = mwMIDI.MIDIMessage.fromJSON(json)
        
        self.assert_(isinstance(message2, mwMIDI.ControlChange))
        self.assertEqual(7,   message2.channel)
        self.assertEqual(127, message2.controller)
        self.assertEqual(0,   message2.value)

if __name__ == '__main__':
    unittest.main()

