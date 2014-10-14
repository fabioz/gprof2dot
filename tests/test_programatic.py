#!/usr/bin/env python
#
# Copyright 2014 Fabio Zadrozny
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
import pstats
import os
import sys

PYTHON_3 = False
if sys.version_info[0] >= 3:
    PYTHON_3 = True

if not PYTHON_3:
    from cStringIO import StringIO
else:
    from io import StringIO

# Make True to regenerate all the files when running the tests.
REGENERATE_FILES = False

class Test(unittest.TestCase):

    def testProgramaticAPIPStats(self):
        '''
        To use PStats programatically it's possible to do:
        
            stats = pstats.Stats (created from file or profile session).
        
            options = gprof2dot.Options()
            options.format = "pstats"

            options.output = StringIO()
            options.input = stats

            def onerror(error):
                raise AssertionError(error)
            gprof2dot.handle_options(options, [], onerror)

        '''
        import gprof2dot

        test_dir = os.path.dirname(os.path.abspath(__file__))
        pstats_dir = os.path.join(test_dir, 'pstats')

        for full_names in (True, False):
            for filename in os.listdir(pstats_dir):
                if filename.endswith('.pstats'):
                    pstats_file = os.path.join(pstats_dir, filename)
    
                    stats = pstats.Stats(pstats_file)
    
                    options = gprof2dot.Options()
                    options.format = "pstats"
                    options.full_names = full_names
    
                    options.output = StringIO()
                    options.input = stats
    
                    def onerror(error):
                        raise AssertionError(error)
                    gprof2dot.handle_options(options, [], onerror)
                    value = options.output.getvalue()
    
                    if full_names:
                        expected_file = pstats_file + '.full_names.expected'
                    else:
                        expected_file = pstats_file + '.expected'
                    if REGENERATE_FILES:
                        with open(expected_file, 'w') as stream:
                            stream.write(value)
                            
                    else:
                        with open(expected_file, 'r') as stream:
                            self.assertEqual(value, stream.read())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testProgramaticAPIPStats']
    unittest.main()
