#!/usr/bin/env python
# encoding: utf-8
"""
globomatic.py

Created by David Wagner on 2010-03-14.

The MIT License

Copyright (c) 2010 David Wagner.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from optparse import OptionParser
import sys
import os
import glob
import time

class GlobOMaticListener(object):
    def on_filematch(self, filename, globomatic):
        """Called for each file that matches the input pattern. Return False 
        to terminate processing."""
        print 'on_filematch: ' + filename
        return True

class GlobOMatic(object):
    def __init__(self, listener, targetPattern, sleepTime = 5.0):
        self.listener = listener
        self.targetPattern = targetPattern
        self.sleepTime = sleepTime
        
        # TODO: Work out how class properties work to provide read only access to these
        self._filesProcessed = 0
        self._filesProcessedTotal = 0
        
        print "Created a GlobOMatic.\nWill look for %s every %d seconds and send them to %s\n" % (self.targetPattern, self.sleepTime, str(self.listener))
    
    def run(self, once = False):
        running = True
        self._filesProcessedTotal = 0
        try:
            while running:
                self._filesProcessed = 0
                filelist = glob.glob(self.targetPattern)
                if len(filelist) > 0:
                    print 'Found %d files to process matching "%s"' % (len(filelist), self.targetPattern)
                    for filename in filelist:
                        if not self.listener.on_filematch(filename, self):
                            print "GlobOMaticListener decided it didn't want anymore."
                            running = False
                            
                        self._filesProcessed += 1
                        
                    self._filesProcessedTotal += self._filesProcessed
                
                if self._filesProcessed > 0:
                    print 'Processed ' + str(self._filesProcessed) + ' this time. Total processed so far: ' + str(self._filesProcessedTotal) + '.',
                else:
                    print 'No new files to process.',
                
                if once:
                    print 'GlobOMatic has only been asked to run once. Bye!'
                    running = False
                else:
                    print 'Sleeping for %ds' % (self.sleepTime)
                    time.sleep(self.sleepTime)
        except KeyboardInterrupt:
            print "\nGlobomatic exited because you killed it with the keyboard. You evil person.\n"
            running = False
    
def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    # Setup the options parser and get the options passed
    parser = OptionParser()
    parser.add_option("-t", "--sleeptime", dest="sleeptime", default="5", type="int", help="Time to wait in seconds between processing runs.", metavar="<seconds>")
    parser.add_option("-i", "--input", dest="input", default="./*", help="Input pattern", metavar="<input pattern>")
    (options, args) = parser.parse_args()
    
    gom = GlobOMatic(GlobOMaticListener(), options.input, options.sleeptime)
    gom.run()

if __name__ == '__main__':
    main()

