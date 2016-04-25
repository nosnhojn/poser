import unittest

import os.path
import sys
sys.path.append(os.path.abspath('../bin'))

from poser import ModuleParser


class ModuleNameParseTests (unittest.TestCase):
  moduleSingleLine = "module singleLine();"
  moduleWhiteSpace = "  module    whiteSpace  ()  ;"
  moduleLeadingChars = "blah blah blah\nmodule leadingChars();"
  moduleLineComment = "// module bmodule blah\nmodule lineComment();\n// module bogus\n"
  moduleOpenCloseComment = "m/**/odule ocC/*blah */omme/* blat */nt();"
  moduleMultiLine = "module\n_2lineName();"
  moduleMultiLineWithComment = "module//biggle\n_2lineName();"

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


class ModuleParseTests (unittest.TestCase):
  moduleSingleInput = "input blah;"
  moduleInputKeyword = "binput blah;\n input    wag ;"
  moduleTwoInputs = "input blah;\n input    wag ;"
  moduleMultipleInputs = "input blah,wag, bag ;"
  moduleMultipleVectorInputs = " input [1:2] blah,wag, bag ;"
  moduleSingleOutput = "output foo;"

  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  def test1Input(self):
    self.mp.parse(self.moduleSingleInput)
    self.assertEqual(self.mp.getInputs(), [ 'input blah;' ])

  def testInputKeyword(self):
    self.mp.parse(self.moduleInputKeyword)
    self.assertEqual(self.mp.getInputs(), [ 'input wag;' ])

  def test2Input(self):
    self.mp.parse(self.moduleTwoInputs)
    self.assertEqual(self.mp.getInputs(), [ 'input blah;', 'input wag;' ])

  def testMultiInput(self):
    self.mp.parse(self.moduleMultipleInputs)
    self.assertEqual(self.mp.getInputs(), [ 'input blah;', 'input wag;', 'input bag;' ])

  def testMultiVectorInput(self):
    self.mp.parse(self.moduleMultipleVectorInputs)
    self.assertEqual(self.mp.getInputs(), [ 'input [1:2] blah;', 'input [1:2] wag;', 'input [1:2] bag;' ])

  def test1Output(self):
    self.mp.parse(self.moduleSingleOutput)
    self.assertEqual(self.mp.getOutputs(), [ 'output foo;' ])


if __name__ == "__main__":
  unittest.main()
