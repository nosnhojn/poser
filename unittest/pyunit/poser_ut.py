import unittest
from unittest.mock import patch, call
import re

import os.path
import sys
sys.path.append(os.path.abspath('../../bin'))

from poser import ModuleParser, IO, Active


class ModuleNameParseTests (unittest.TestCase):
  moduleSingleLine = "module singleLine();endmodule"
  moduleWhiteSpace = "  module    whiteSpace  ()  ;endmodule"
  moduleLeadingChars = "blah blah blah\nmodule leadingChars();endmodule"
  moduleLineComment = "// module bmodule blah\nmodule lineComment();\n// module bogus\nendmodule"
  moduleOpenCloseComment = "/*\nmodule not\n*/m/**/odule ocC/*blah */omme/* blat */nt();/*\nmodule not\n*/endmodule"
  moduleMultiLine = "module\n_2lineName();endmodule"
  moduleMultiLineWithComment = "module//biggle\n_2lineName();endmodule"
  moduleWireRegLogic = "module wire reg logic logicwireregbiggle();endmodule"

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

  def testWireRegLogicAreScrubbed(self):
    self.mp.parse(self.moduleWireRegLogic)
    self.assertEqual(self.mp.getModuleName(), 'logicwireregbiggle')

class BaseTestClasses:
  class ModulePortTests (unittest.TestCase):
    moduleSinglePort = ''
    modulePortKeyword = ''
    moduleTwoPorts = ''
    moduleMultiplePorts = ''
    moduleMultipleVectorPorts = ''
    moduleSingleOutput = ''
    moduleIrregularSpacing = ''
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
      self.assertEqual(p, self.changePortType([ IO('port', 'blah', '1', '0'), IO('port', 'wag', '1', '0'), IO('port', 'bag', '1', '0') ]))

    def testIrregularlySpacedPort(self):
      p = self.mp.parsePorts(self.type, self.changePortType(self.moduleIrregularSpacing))
      self.assertEqual(p, self.changePortType([ IO('port', 'blah', '1', '0'),
                                                IO('port', 'wag', '1', '0'),
                                                IO('port', 'bag', '1', '0'),
                                                IO('port', 'dang'),
                                                IO('port', 'biggy', 'flaGGs-54', '34'),
                                             ]))

    def changePortType(self, io):
      if isinstance(io, list):
        l = []
        for s in io:
          if isinstance(s, IO):
            l.append(IO(self.type, s.name, s.msb, s.lsb))
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
      self.moduleIrregularSpacing = "module blah();   port[1:0]blah,wag, bag ;port       dang  ; port[flaGGs-54:  34] biggy;endmodule"


  class ModuleAnsiPortTests (ModulePortTests):
    def __init__(self, *args, **kwargs):
      super(BaseTestClasses.ModuleAnsiPortTests, self).__init__(*args, **kwargs)

      self.moduleSinglePort = "module blah (port blah);"
      self.modulePortKeyword = "module blah (bport blah,  port    wag) a ;"
      self.moduleTwoPorts = "module blah (port blah,  port    wag, );"
      self.moduleMultiplePorts = "module blah (port blah,wag, bag )"
      self.moduleMultipleVectorPorts = "module blah ( port [1:0] blah,wag, bag ) ;"
      self.moduleSingleOutput = "module blah (output foo);"
      self.moduleIrregularSpacing = "module blah(port[1:0]blah,wag, bag ,port       dang  , port[flaGGs-54:  34] biggy);endmodule"


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

  def testIOAsString(self):
    self.mp.inputs = [ IO('input', 'a'), IO('input', 'b') ]
    self.mp.outputs = [ IO('output', 'c') ]
    self.assertEqual(self.mp.moduleIOAsString(), 'a, b, c')

  def testSimplePortListAsString(self):
    self.mp.inputs = [ IO('input', 'a'), IO('input', 'b') ]
    self.mp.outputs = [ IO('output', 'c') ]

    _expect  = '  input a;\n'
    _expect += '  input b;\n'
    _expect += '  output c;\n'
    self.assertEqual(self.mp.modulePortsAsString(), _expect)

  def testVectorPortListAsString(self):
    self.mp.inputs = [ IO('input', 'a', 'blah', 'jIb'), IO('input', 'b', '2', '0') ]
    self.mp.outputs = [ IO('output', 'c', '5-1+`WHAT', '31') ]

    _expect  = '  input [blah:jIb] a;\n'
    _expect += '  input [2:0] b;\n'
    _expect += '  output [5-1+`WHAT:31] c;\n'
    self.assertEqual(self.mp.modulePortsAsString(), _expect)

  def testAnsiParametersAsString(self):
    self.mp.parse('blah module name #(some stuff\n, yok=al\n) (); sketchy jinx endmodule input bag')
    self.assertEqual(self.mp.ansiParametersAsString(), 'some stuff , yok=al ')

  def testNonAnsiParametersAsString(self):
    self.mp.parse('blah module name  (); parameter ding = dong; boo-urns; parameter dkf==,,\n=\n=kdk; sketchy jinx endmodule input bag')
    self.assertEqual(self.mp.nonAnsiParametersAsString(), '  parameter ding = dong;\n  parameter dkf==,, = =kdk;\n')

  def testPreambleAsString(self):
    self.mp.parse('goats\nsome stuff\n`include bogus\n`define blah what\n module name();endmodule')
    self.assertEqual(self.mp.preambleAsString(), 'goats\nsome stuff\n`include bogus\n`define blah what\n')

  def testNoPreambleAsString(self):
    self.mp.parse(' module name();input something;endmodule')
    self.assertEqual(self.mp.preambleAsString(), '')

  def testPoserParams(self):
    self.mp.inputs = [ IO('input', 'a'), IO('input', 'b') ]
    self.mp.outputs = [ IO('output', 'c') ]
    self.mp.setTied(Active.hi)
    self.mp.setGridSize(2, 1)

    _expect  = '  parameter poser_tied = 1\'b1;\n'
    _expect += '  parameter poser_width_in = 0+1+1;\n'
    _expect += '  parameter poser_width_out = 0+1;\n'
    _expect += '  parameter poser_grid_width = 2;\n'
    _expect += '  parameter poser_grid_depth = 1;\n'
    self.assertEqual(self.mp.poserParamsAsString(), _expect)

  def testPoserParamsIgnoreClkRst(self):
    self.mp.inputs = [ IO('input', 'a'), IO('input', 'b'), IO('input', 'd') ]
    self.mp.outputs = [ IO('output', 'c') ]
    self.mp.setTied(Active.hi)
    self.mp.setClkName('a')
    self.mp.setRstName('b', Active.lo)
    self.mp.setGridSize(2, 1)

    _expect  = '  parameter poser_tied = 1\'b1;\n'
    _expect += '  parameter poser_width_in = 0+1;\n'
    _expect += '  parameter poser_width_out = 0+1;\n'
    _expect += '  parameter poser_grid_width = 2;\n'
    _expect += '  parameter poser_grid_depth = 1;\n'
    self.assertEqual(self.mp.poserParamsAsString(), _expect)

  def testPoserInputWidthWithVectors(self):
    self.mp.inputs = [ IO('input', 'a', '8', '1'), IO('input', 'b', 'a', 'A') ]
    self.mp.outputs = [ IO('output', 'c') ]
    self.mp.setTied(Active.hi)

    _expect  = '  parameter poser_tied = 1\'b1;\n'
    _expect += '  parameter poser_width_in = 0+8-1+1+a-A+1;\n'
    _expect += '  parameter poser_width_out = 0+1;\n'
    _expect += '  parameter poser_grid_width = 0;\n'
    _expect += '  parameter poser_grid_depth = 0;\n'
    self.assertEqual(self.mp.poserParamsAsString(), _expect)

  def testPoserOutputWidthWithVectors(self):
    self.mp.inputs = [ IO('input', 'c') ]
    self.mp.outputs = [ IO('output', 'a', '8', '1'), IO('input', 'b', 'a', 'A') ]
    self.mp.setTied(Active.hi)

    _expect  = '  parameter poser_tied = 1\'b1;\n'
    _expect += '  parameter poser_width_in = 0+1;\n'
    _expect += '  parameter poser_width_out = 0+8-1+1+a-A+1;\n'
    _expect += '  parameter poser_grid_width = 0;\n'
    _expect += '  parameter poser_grid_depth = 0;\n'
    self.assertEqual(self.mp.poserParamsAsString(), _expect)

  def testPoser1InternalInputs(self):
    self.mp.inputs = [ IO('input', 'c') ]
    self.assertEqual(self.mp.poserInternalInputsAsString(), '  wire [poser_width_in-1:0] poser_inputs;\n  assign poser_inputs = { c };\n')

  def testPoser1InternalInputsIgnoreClkRst(self):
    self.mp.inputs = [ IO('input', 'c'), IO('input', 'clk'), IO('input', 'rst') ]
    self.mp.setClkName('clk')
    self.mp.setRstName('rst', Active.lo)
    self.assertEqual(self.mp.poserInternalInputsAsString(), '  wire [poser_width_in-1:0] poser_inputs;\n  assign poser_inputs = { c };\n')

  def testPoserMultipleInternalInputs(self):
    self.mp.inputs = [ IO('input', 'c') , IO('input', 'd') ]
    self.assertEqual(self.mp.poserInternalInputsAsString(), '  wire [poser_width_in-1:0] poser_inputs;\n  assign poser_inputs = { c,d };\n')

  def testPoser1InternalOutputs(self):
    self.mp.outputs = [ IO('output', 'c') ]
    self.assertEqual(self.mp.poserInternalOutputsAsString(), '  wire [poser_width_out-1:0] poser_outputs;\n  assign \'{ c } = poser_outputs;\n')

  def testPoserMultipleInternalOutputs(self):
    self.mp.outputs = [ IO('output', 'c') , IO('output', 'd') ]
    self.assertEqual(self.mp.poserInternalOutputsAsString(), '  wire [poser_width_out-1:0] poser_outputs;\n  assign \'{ c,d } = poser_outputs;\n')

  def testPoserGridIODepthN(self):
    self.mp.setGridSize(1, 4)
    _expect  = '  wire [poser_grid_width-1:0] poser_grid_output [0:poser_grid_depth-1];\n'
    _expect += '  assign poser_outputs = poser_grid_output[poser_grid_depth-1];\n'
    self.assertEqual(self.mp.poserGridOutputsAsString(), _expect)
    

class ModuleOutput(unittest.TestCase):
  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  def testParseFile(self):
    pass


if __name__ == "__main__":
  unittest.main()
