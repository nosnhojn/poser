import unittest
from unittest.mock import patch, call
import re

import os.path
import sys
sys.path.append(os.path.abspath('../bin'))

from poser import ModuleParser, IO


class ModuleNameParseTests (unittest.TestCase):
  moduleSingleLine = "module singleLine();endmodule"
  moduleWhiteSpace = "  module    whiteSpace  ()  ;endmodule"
  moduleLeadingChars = "blah blah blah\nmodule leadingChars();endmodule"
  moduleLineComment = "// module bmodule blah\nmodule lineComment();\n// module bogus\nendmodule"
  moduleOpenCloseComment = "m/**/odule ocC/*blah */omme/* blat */nt();endmodule"
  moduleMultiLine = "module\n_2lineName();endmodule"
  moduleMultiLineWithComment = "module//biggle\n_2lineName();endmodule"

  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  def testSingleLineModuleName(self):
    self.mp.parse(self.moduleSingleLine)
    self.assertEqual(self.mp.getModuleName(), 'singleLine')

  def testSingleLineModuleNameWithWhitespace(self):
    self.mp.parse(self.moduleWhiteSpace)
    self.assertEqual(self.mp.getModuleName(), 'whiteSpace')

  def testModuleNotFirstLine(self):
    self.mp.parse(self.moduleLeadingChars)
    self.assertEqual(self.mp.getModuleName(), 'leadingChars')

  def testModuleOpenningLineComment(self):
    self.mp.parse(self.moduleLineComment)
    self.assertEqual(self.mp.getModuleName(), 'lineComment')

  def testModuleOpenCloseComment(self):
    self.mp.parse(self.moduleOpenCloseComment)
    self.assertEqual(self.mp.getModuleName(), 'ocComment')

  def testModuleNameTwoLines(self):
    self.mp.parse(self.moduleMultiLine)
    self.assertEqual(self.mp.getModuleName(), '_2lineName')

  def testModuleNameTwoLinesWithComment(self):
    self.mp.parse(self.moduleMultiLineWithComment)
    self.assertEqual(self.mp.getModuleName(), '_2lineName')


class ModuleNonAnsiPortTests (unittest.TestCase):
  moduleSinglePort = "port blah;"
  modulePortKeyword = "bport blah;\n port    wag ;"
  moduleTwoPorts = "port blah;\n port    wag ;"
  moduleMultiplePorts = "port blah,wag, bag ;"
  moduleMultipleVectorPorts = " port [1:0] blah,wag, bag ;"
  moduleSingleOutput = "output foo;"
  type = ''

  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  def test1Port(self):
    p = self.mp.nonAnsiPorts(self.type, self.changePortType(self.moduleSinglePort))
    self.assertEqual(p, self.changePortType([ IO('port', 'blah') ]))

  def testPortKeyword(self):
    p = self.mp.nonAnsiPorts(self.type, self.changePortType(self.modulePortKeyword))
    self.assertEqual(p, self.changePortType([ IO('port', 'wag') ]))

  def test2Port(self):
    p = self.mp.nonAnsiPorts(self.type, self.changePortType(self.moduleTwoPorts))
    self.assertEqual(p, self.changePortType([ IO('port', 'blah'), IO('port', 'wag') ]))

  def testMultiPort(self):
    p = self.mp.nonAnsiPorts(self.type, self.changePortType(self.moduleMultiplePorts))
    self.assertEqual(p, self.changePortType([ IO('port', 'blah'), IO('port', 'wag'), IO('port', 'bag') ]))

  def testMultiVectorPort(self):
    p = self.mp.nonAnsiPorts(self.type, self.changePortType(self.moduleMultipleVectorPorts))
    self.assertEqual(p, self.changePortType([ IO('port', 'blah', 2), IO('port', 'wag', 2), IO('port', 'bag', 2) ]))

  def changePortType(self, io):
    if isinstance(io, list):
      l = []
      for s in io:
        if isinstance(s, IO):
          l.append(IO(self.type, s.name, s.size))
        else:
          l.append(re.sub('port', self.type, s))
      return l
    else:
      return re.sub('port', self.type, io)

  def setType(self, t):
    self.type = t


class ModuleNonAnsiInputTests(ModuleNonAnsiPortTests):
  def __init__(self, *args, **kwargs):
    super(ModuleNonAnsiInputTests, self).__init__(*args, **kwargs)
    self.setType('input')


class ModuleNonAnsiOutputTests(ModuleNonAnsiPortTests):
  def __init__(self, *args, **kwargs):
    super(ModuleNonAnsiOutputTests, self).__init__(*args, **kwargs)
    self.setType('output')


class ModuleParseTests(unittest.TestCase):
  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  @patch('poser.ModuleParser.nonAnsiPorts')
  def testCallsNonAnsiPorts(self, mock_nonAnsiPorts):
    calls = [ call( 'input', ''), call( 'output', '') ]
    self.mp.parse('')
    mock_nonAnsiPorts.assert_has_calls(calls)

  @patch('poser.ModuleParser.nonAnsiPorts')
  def testCallsNonAnsiPorts(self, mock_nonAnsiPorts):
    calls = [ call( 'input', 'module sketchy jinx endmodule'), call( 'output', 'module sketchy jinx endmodule') ]
    self.mp.parse('blah module sketchy jinx endmodule input bag')
    mock_nonAnsiPorts.assert_has_calls(calls)


if __name__ == "__main__":
  del ModuleNonAnsiPortTests
  unittest.main()
