import unittest
from unittest.mock import patch, call
import re

import os.path
import sys

sys.path.append(os.path.abspath('../../bin'))
from poser import ModuleParser, IO, Active


class ModuleIOBaseTests(unittest.TestCase):
  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  def fileAsString(self, file):
    f = open(file, 'r')
    _file = f.read()
    f.close()
    return _file


class ModuleIOTests(ModuleIOBaseTests):
  def testSimpleNonAnsiPorts(self):
    self.mp.parse(self.fileAsString('../test-files/module0.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/module0-gold.v'))

  def testSimpleAnsiPorts(self):
    self.mp.parse(self.fileAsString('../test-files/module1.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/module1-gold.v'))

  def testNonAnsiVectorPorts(self):
    self.mp.parse(self.fileAsString('../test-files/module2.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/module2-gold.v'))

  def testAnsiVectorPorts(self):
    self.mp.parse(self.fileAsString('../test-files/module3.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/module3-gold.v'))

  def testAnsiParameters(self):
    self.mp.parse(self.fileAsString('../test-files/module4.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/module4-gold.v'))

  def testNonAnsiParameters(self):
    self.mp.parse(self.fileAsString('../test-files/module5.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/module5-gold.v'))

  def testModuleHeaderIsCopied(self):
    self.mp.parse(self.fileAsString('../test-files/module6.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/module6-gold.v'))




class ModuleArrayTests(ModuleIOBaseTests):
  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  def testModule2x1Grid(self):
    self.maxDiff = None
    self.mp.setGridSize(2, 1)
    self.mp.setClkName('clk_')
    self.mp.setRstName('rst_', Active.lo)
    self.mp.setTied(Active.hi)
    self.mp.setNumFlops(2)
    self.mp.parse(self.fileAsString('../test-files/poser-module0.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/poser-module0-gold.v'))

  def testModule2x2GridMultipleIO(self):
    self.maxDiff = None
    self.mp.setGridSize(2, 2)
    self.mp.setClkName('clk_')
    self.mp.setRstName('rst_', Active.lo)
    self.mp.setTied(Active.hi)
    self.mp.setNumFlops(4)
    self.mp.parse(self.fileAsString('../test-files/poser-module1.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/poser-module1-gold.v'))

  def testModule9x5GridMultipleIO(self):
    self.maxDiff = None
    self.mp.setGridSize(5, 9)
    self.mp.setClkName('clk_')
    self.mp.setRstName('rst_', Active.lo)
    self.mp.setTied(Active.hi)
    self.mp.setNumFlops(45)
    self.mp.parse(self.fileAsString('../test-files/poser-module4.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/poser-module4-gold.v'))

  def testModule9x5AsyncGrid(self):
    self.maxDiff = None
    self.mp.setGridSize(2, 1)
    self.mp.setClkName('clk_')
    self.mp.setRstName('rst_', Active.lo)
    self.mp.setTied(Active.hi)
    self.mp.parse(self.fileAsString('../test-files/poser-module3.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/poser-module3-gold.v'))

  def testModule3x1GridMultipleIO(self):
    self.maxDiff = None
    self.mp.setGridSize(3, 1)
    self.mp.setClkName('clk_')
    self.mp.setRstName('rst_', Active.lo)
    self.mp.setTied(Active.hi)
    self.mp.parse(self.fileAsString('../test-files/poser-module2.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/poser-module2-gold.v'))

  def testModule2x1GridMultipleIO(self):
    self.maxDiff = None
    self.mp.setGridSize(2, 1)
    self.mp.setClkName('clk_')
    self.mp.setRstName('rst_', Active.lo)
    self.mp.setTied(Active.hi)
    self.mp.parse(self.fileAsString('../test-files/poser-module5.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('../test-files/poser-module5-gold.v'))




if __name__ == "__main__":
  unittest.main()
