import unittest
from poser import Rand, Module, OutputType
import random 


class ModuleTests (unittest.TestCase):
  def setUp(self):
    self.cycles = 30
    self.m = Module()

  def tearDown(self):
    pass

  def depth(self):
    return len(self.m.cells)

  def width(self):
    return len(self.m.cells[0])

  def createGridAndTieCell0Input(self, inWidth, outWidth, d, v = False):
    self.m.createGrid(inWidth, outWidth, d)
    self.m.tieCell0([v])

  def testNoPrunedGatesEqualIOWidth0(self):
    self.assertTrue(self.noGatesPruned(5, 5, 17, 3))

  def testNoPrunedGatesEqualIOWidth1(self):
    self.assertTrue(self.noGatesPruned(25, 25, 17, 18))

  def testNoPrunedGatesEqualIOWidth2(self):
    self.assertTrue(self.noGatesPruned(55, 55, 37, 321))

  def testNoPrunedGatesEqualIOWidth3(self):
    self.assertTrue(self.noGatesPruned(705, 705, 3, 41))

  def testNoPrunedGatesEqualIOWidth4(self):
    self.assertTrue(self.noGatesPruned(10, 10, 81, 41))


  def testNoPrunedGatesLargerInputWidth0(self):
    self.assertTrue(self.noGatesPruned(5, 4, 17, 3))

  def testNoPrunedGatesLargerInputWidth1(self):
    self.assertTrue(self.noGatesPruned(25, 21, 17, 18))

  def testNoPrunedGatesLargerInputWidth2(self):
    self.assertTrue(self.noGatesPruned(55, 32, 37, 321))

  def testNoPrunedGatesLargerInputWidth3(self):
    self.assertTrue(self.noGatesPruned(705, 700, 3, 41))

  def testNoPrunedGatesLargerInputWidth4(self):
    self.assertTrue(self.noGatesPruned(10, 1, 81, 41))


  def noGatesPruned(self, inWidth, outWidth, depth, flops):
    outputs = []
    self.createGridAndTieCell0Input(inWidth, outWidth, depth, True)
    self.m.setNumFlops(flops)
    self.m.randomizeGates()

    for i in range(self.cycles):
      a = []
      for i in range(inWidth):
        a.append(random.getrandbits(1))

      self.m.driveInputs(a)
      self.m.clk()
      outputs.append(self.m.sampleOutputs())

    numChoked = 0
    for i in range(outWidth):
      column = [int(x[i]) for x in outputs ]
      bah = ''
      if sum(column) == 0:
        numChoked += 1
      if sum(column) == self.cycles:
        numChoked += 1

    return numChoked == 0


if __name__ == "__main__":
  unittest.main()
