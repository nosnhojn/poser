import unittest
from unittest.mock import patch, call
import re

import os.path
import sys

sys.path.append(os.path.abspath('../bin'))
from poser import ModuleParser, IO


class ModuleOutput(unittest.TestCase):
  def setUp(self):
    self.mp = ModuleParser()

  def tearDown(self):
    pass

  def fileAsString(self, file):
    f = open(file, 'r')
    _file = f.read()
    f.close()
    return _file

  def testSimpleNonAnsiPorts(self):
    self.mp.parse(self.fileAsString('./test-files/module0.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('./test-files/module0-gold.v'))

  def testSimpleAnsiPorts(self):
    self.mp.parse(self.fileAsString('./test-files/module1.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('./test-files/module1-gold.v'))

  def testNonAnsiVectorPorts(self):
    self.mp.parse(self.fileAsString('./test-files/module2.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('./test-files/module2-gold.v'))

  def testAnsiVectorPorts(self):
    self.mp.parse(self.fileAsString('./test-files/module3.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('./test-files/module3-gold.v'))

  def testAnsiParameters(self):
    self.mp.parse(self.fileAsString('./test-files/module4.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('./test-files/module4-gold.v'))

  def testNonAnsiParameters(self):
    self.mp.parse(self.fileAsString('./test-files/module5.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('./test-files/module5-gold.v'))

  def testModuleHeaderIsCopied(self):
    self.mp.parse(self.fileAsString('./test-files/module6.v'))
    self.assertEqual(self.mp.moduleAsString(), self.fileAsString('./test-files/module6-gold.v'))


if __name__ == "__main__":
  unittest.main()
