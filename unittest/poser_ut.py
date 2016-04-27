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

class BaseTestClasses:
  class ModulePortTests (unittest.TestCase):
    moduleSinglePort = ''
    modulePortKeyword = ''
    moduleTwoPorts = ''
    moduleMultiplePorts = ''
    moduleMultipleVectorPorts = ''
    moduleSingleOutput = ''
    type = ''

    def setUp(self):
      self.mp = ModuleParser()

    def tearDown(self):
      pass

    def test1Port(self):
      p = self.mp.parsePorts(self.type, self.changePortType(self.moduleSinglePort))
      self.assertEqual(p, self.changePortType([ IO('port', 'blah') ]))

    def testPortKeyword(self):
      p = self.mp.parsePorts(self.type, self.changePortType(self.modulePortKeyword))
      self.assertEqual(p, self.changePortType([ IO('port', 'wag') ]))

    def test2Port(self):
      p = self.mp.parsePorts(self.type, self.changePortType(self.moduleTwoPorts))
      self.assertEqual(p, self.changePortType([ IO('port', 'blah'), IO('port', 'wag') ]))

    def testMultiPort(self):
      p = self.mp.parsePorts(self.type, self.changePortType(self.moduleMultiplePorts))
      self.assertEqual(p, self.changePortType([ IO('port', 'blah'), IO('port', 'wag'), IO('port', 'bag') ]))

    def testMultiVectorPort(self):
      p = self.mp.parsePorts(self.type, self.changePortType(self.moduleMultipleVectorPorts))
      self.assertEqual(p, self.changePortType([ IO('port', 'blah', '1-0+1'), IO('port', 'wag', '1-0+1'), IO('port', 'bag', '1-0+1') ]))

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


  class ModuleNonAnsiPortTests (ModulePortTests):
    def __init__(self, *args, **kwargs):
      super(BaseTestClasses.ModuleNonAnsiPortTests, self).__init__(*args, **kwargs)

      self.moduleSinglePort = "module blah(); port blah; endmodule"
      self.modulePortKeyword = "module blah(); bport blah; jak beck; port    wag ; a endmodule"
      self.moduleTwoPorts = "module blah(); port blah,  port    wag ; endmodule"
      self.moduleMultiplePorts = "module blah(); port blah,wag, bag ; endmodule"
      self.moduleMultipleVectorPorts = "module blah();  port [1:0] blah,wag, bag ; endmodule"
      self.moduleSingleOutput = "module blah(); output foo; endmodule"


  class ModuleAnsiPortTests (ModulePortTests):
    def __init__(self, *args, **kwargs):
      super(BaseTestClasses.ModuleAnsiPortTests, self).__init__(*args, **kwargs)

      self.moduleSinglePort = "module blah (port blah);"
      self.modulePortKeyword = "module blah (bport blah,  port    wag) a ;"
      self.moduleTwoPorts = "module blah (port blah,  port    wag, );"
      self.moduleMultiplePorts = "module blah (port blah,wag, bag )"
      self.moduleMultipleVectorPorts = "module blah ( port [1:0] blah,wag, bag ) ;"
      self.moduleSingleOutput = "module blah (output foo);"


class ModuleNonAnsiInputTests(BaseTestClasses.ModuleNonAnsiPortTests):
  def __init__(self, *args, **kwargs):
    super(ModuleNonAnsiInputTests, self).__init__(*args, **kwargs)
    self.setType('input')


class ModuleNonAnsiOutputTests(BaseTestClasses.ModuleNonAnsiPortTests):
  def __init__(self, *args, **kwargs):
    super(ModuleNonAnsiOutputTests, self).__init__(*args, **kwargs)
    self.setType('output')


class ModuleAnsiInputTests(BaseTestClasses.ModuleAnsiPortTests):
  def __init__(self, *args, **kwargs):
    super(ModuleAnsiInputTests, self).__init__(*args, **kwargs)
    self.setType('input')


class ModuleAnsiOutputTests(BaseTestClasses.ModuleAnsiPortTests):
  def __init__(self, *args, **kwargs):
    super(ModuleAnsiOutputTests, self).__init__(*args, **kwargs)
    self.setType('output')


class ModuleParseTests(unittest.TestCase):
  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  @patch('poser.ModuleParser.scrubModule', return_value='module blah endmodule')
  def testParseCallsScrub(self, mock_scrubModule):
    str = 'module grass(); shlub a dub dub endmodule'
    self.mp.parse(str)
    mock_scrubModule.assert_called_with(str)

  @patch('poser.ModuleParser.getModuleNameFromString', return_value='module blah endmodule')
  def testParseCallsGetModuleNameFromString(self, mock_getModuleNameFromString):
    str = 'module grass(); shlub a dub dub endmodule'
    self.mp.parse(str)
    mock_getModuleNameFromString.assert_called_with(str)

  @patch('poser.ModuleParser.parsePorts')
  def testParseCallsPorts(self, mock_nonAnsiPorts):
    calls = [ call( 'input', 'module name(); sketchy jinx endmodule'), call( 'output', 'module name(); sketchy jinx endmodule') ]
    self.mp.parse('blah module name(); sketchy jinx endmodule input bag')
    mock_nonAnsiPorts.assert_has_calls(calls)


class ModuleOutput(unittest.TestCase):
  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  def testParseFile(self):
    pass


if __name__ == "__main__":
  unittest.main()
