import unittest
from poser import Rand, Module, OutputType
import random 


class ModuleTests (unittest.TestCase):
  def setUp(self):
    self.cycles = 100
    self.m = Module()

  def tearDown(self):
    pass

  def depth(self):
    return len(self.m.cells)

  def width(self):
    return len(self.m.cells[0])

  def createGridAndTieCell0Input(self, inWidth, outWidth, gridWidth, d, v = False):
    self.m.createGrid(inWidth, outWidth, gridWidth, d)
    self.m.tieCell0([v])

  def gatesPruned(self, inWidth, outWidth, gridWidth, depth, flops):
    self.createGridAndTieCell0Input(inWidth, outWidth, gridWidth, depth, True)
    self.m.setNumFlops(flops)
    self.m.randomizeGates()

    for i in range(self.cycles):
      a = []
      for i in range(inWidth):
        a.append(random.getrandbits(1))

      self.m.driveInputs(a)
      self.m.clk()
      self.m.sampleOutputs()

    return self.m.outputsFixed() or self.m.moduleHasFixedCells()


@unittest.skip('')
class EqualIOTests(ModuleTests):
  def testNoPrunedGatesEqualIOWidth0(self):
    self.assertFalse(self.gatesPruned(5, 5, 5, 17, 3))

  def testNoPrunedGatesEqualIOWidth1(self):
    self.assertFalse(self.gatesPruned(25, 25, 25, 17, 18))

  def testNoPrunedGatesEqualIOWidth2(self):
    self.assertFalse(self.gatesPruned(55, 55, 55, 37, 321))

  def testNoPrunedGatesEqualIOWidth3(self):
    self.assertFalse(self.gatesPruned(705, 705, 705, 3, 41))

  def testNoPrunedGatesEqualIOWidth4(self):
    self.assertFalse(self.gatesPruned(10, 10, 10, 81, 41))

  def testNoPrunedGatesEqualIOWidth5(self):
    self.assertFalse(self.gatesPruned(5, 5, 5, 3, 0))

@unittest.skip('')
class LargerInputTests(ModuleTests):
  def testNoPrunedGatesLargerInputWidth0(self):
    self.assertFalse(self.gatesPruned(5, 4, 5, 17, 3))

  def testNoPrunedGatesLargerInputWidth1(self):
    self.assertFalse(self.gatesPruned(25, 21, 25, 17, 18))

  def testNoPrunedGatesLargerInputWidth2(self):
    self.assertFalse(self.gatesPruned(55, 32, 55, 37, 321))

  def testNoPrunedGatesLargerInputWidth3(self):
    self.assertFalse(self.gatesPruned(705, 700, 705, 3, 41))

  def testNoPrunedGatesLargerInputWidth4(self):
    self.assertFalse(self.gatesPruned(10, 1, 10, 81, 41))

  def testNoPrunedGatesLargerInputWidth5(self):
    self.assertFalse(self.gatesPruned(10, 1, 10, 41, 0))


@unittest.skip('')
class SmallerInputTests(ModuleTests):
  def testNoPrunedGatesSmallerInputWidth0(self):
    self.assertFalse(self.gatesPruned(4, 5, 5, 17, 3))

  def testNoPrunedGatesSmallerInputWidth1(self):
    self.assertFalse(self.gatesPruned(21, 25, 25, 17, 18))

  def testNoPrunedGatesSmallerInputWidth2(self):
    self.assertFalse(self.gatesPruned(32, 55, 55, 37, 321))

  def testNoPrunedGatesSmallerInputWidth3(self):
    self.assertFalse(self.gatesPruned(700, 705, 705, 3, 41))

  def testNoPrunedGatesSmallerInputWidth4(self):
    self.assertFalse(self.gatesPruned(1, 10, 10, 81, 41))

  def testNoPrunedGatesSmallerInputWidth5(self):
    self.assertFalse(self.gatesPruned(1, 10, 10, 41, 0))

class LargerGridTests(ModuleTests):
  def testNoPrunedLargeGrid0(self):
    self.assertFalse(self.gatesPruned(4, 5, 75, 37, 3))

  def testNoPrunedLargeGrid1(self):
    self.assertFalse(self.gatesPruned(21, 25, 145, 17, 18))

  def testNoPrunedLargeGrid2(self):
    self.assertFalse(self.gatesPruned(32, 55, 165, 37, 321))

  def testNoPrunedLargeGrid3(self):
    self.assertFalse(self.gatesPruned(700, 705, 805, 3, 241))

  def testNoPrunedLargeGrid4(self):
    self.assertFalse(self.gatesPruned(7, 10, 99, 81, 41))

  def testNoPrunedLargeGrid5(self):
    self.assertFalse(self.gatesPruned(6, 10, 55, 141, 0))



if __name__ == "__main__":
  unittest.main()
