import unittest
from poser import Cell, Rand, Module, OutputType, CellType, Mux
import random 


class CellTests (unittest.TestCase):
  def setUp(self):
    self.c = Cell()

  def tearDown(self):
    pass

  def testAsyncOutputFalseWhenBothInputsFalse(self):
    self.c.driveInputs([False, False])
    self.assertFalse(self.c.asyncOutput())

  def testAsyncOutputFalseWhenOneInputFalse(self):
    self.c.driveInputs([True, False])
    self.assertFalse(self.c.asyncOutput())

  def testAsyncOutputTrueWhenBothInputsTrue(self):
    self.c.driveInputs([True, True])
    self.assertTrue(self.c.asyncOutput())

  def testSyncOutputResetsToFalse(self):
    self.assertFalse(self.c.syncOutput())

  def testSyncOutputFalseWhenBothInputsFalse(self):
    self.c.driveInputs([False, False])
    self.c.clk()
    self.assertFalse(self.c.syncOutput())

  def testSyncOutputTrueWhenBothInputsTrue(self):
    self.c.driveInputs([True, True])
    self.c.clk()
    self.assertTrue(self.c.syncOutput())

  def testSyncOutputUpdatesWith2ndClk(self):
    self.c.driveInputs([True, True])
    self.c.clk()
    self.c.driveInputs([False, False])
    self.c.clk()
    self.assertFalse(self.c.syncOutput())

  def testSyncOutputHolds(self):
    self.c.driveInputs([True, True])
    self.c.clk()
    self.c.clk()
    self.assertTrue(self.c.syncOutput())

  def testAsyncStableWhenFalse(self):
    self.c.driveInputs([False, False])
    self.c.driveInputs([False, False])
    self.assertTrue(self.c.isStable())

  def testAsyncStableWhenBothTrue(self):
    self.c.driveInputs([True, True])
    self.c.driveInputs([True, True])
    self.assertTrue(self.c.isStable())

  def testAsyncStableWhenBothFalse(self):
    self.c.driveInputs([False, False])
    self.c.driveInputs([False, False])
    self.assertTrue(self.c.isStable())
 
  def testAsyncNotStableWhenAChanges(self):
    self.c.driveInputs([True, True])
    self.c.driveInputs([False, True])
    self.assertFalse(self.c.isStable())
 
  def testAsyncNotStableWhenBChanges(self):
    self.c.driveInputs([True, True])
    self.c.clk()
    self.c.driveInputs([True, False])
    self.c.clk()
    self.assertFalse(self.c.isStable())

  def testCellCanBeOr(self):
    self.c.setOperator(CellType._or)
    self.c.driveInputs([False, True])
    self.assertTrue(self.c.asyncOutput())

  def testCellCanBeXor(self):
    self.c.setOperator(CellType._xor)
    self.c.driveInputs([True, True])
    self.assertFalse(self.c.asyncOutput())
    self.c.driveInputs([False, False])
    self.assertFalse(self.c.asyncOutput())
    self.c.driveInputs([False, True])
    self.assertTrue(self.c.asyncOutput())

  def testSetForAsyncOutput(self):
    self.c.setOutputType(OutputType.async)
    self.c.driveInputs([True, True])
    self.assertTrue(self.c.output())

  def testSetForSyncOutput(self):
    self.c.setOutputType(OutputType.sync)
    self.c.driveInputs([True, True])
    self.assertFalse(self.c.output())
    self.c.clk()
    self.assertTrue(self.c.output())

  def testGetOutputType(self):
    self.c.setOutputType(OutputType.sync)
    self.assertTrue(self.c.getOutputType() == OutputType.sync)

  def testCellHistory(self):
    self.c.setOutputType(OutputType.sync)
    self.c.driveInputs([True, True])
    for i in range(50):
      if i == 49:
        self.c.driveInputs([False, False])
      self.c.clk()
      self.c.output()
    self.assertEqual(len(self.c.cellHistory()), 50)
    self.assertEqual(self.c.cellHistory(), [True] * 49 + [False])

  def testCellHistoryFixed(self):
    self.c.setOutputType(OutputType.sync)
    self.c.driveInputs([True, True])
    for i in range(50):
      self.c.clk()
      self.c.output()
    self.assertTrue(self.c.cellHistoryFixed())

  def testCellHistoryNotFixed(self):
    self.c.setOutputType(OutputType.sync)
    self.c.driveInputs([True, True])
    self.c.clk()
    self.c.output()
    self.c.driveInputs([False, True])
    self.c.clk()
    self.c.output()
    self.assertFalse(self.c.cellHistoryFixed())

  def testNoCellHistoryForAsync(self):
    self.c.setOutputType(OutputType.async)
    self.c.driveInputs([True, True])
    self.c.output()
    self.c.driveInputs([False, True])
    self.c.output()
    self.assertFalse(self.c.cellHistoryFixed())

    


class ModuleTests (unittest.TestCase):
  def setUp(self):
    self.m = Module()

  def tearDown(self):
    pass

  def depth(self):
    return len(self.m.cells)

  def width(self):
    return len(self.m.cells[0])

  def createGridAndTieCell0Input(self, wIn, wOut, width, depth=1, initValForCell0 = False):
    self.m.createGrid(wIn, wOut, width, depth)
    self.m.tieCell0([initValForCell0])

  def testInit4x1(self):
    self.createGridAndTieCell0Input(4, 4, 4, 1)

    self.assertTrue(self.depth() == 1)
    self.assertTrue(self.width() == 4)

  def testInitNxN(self):
    self.createGridAndTieCell0Input(7, 7, 7, 6)

    self.assertTrue(self.depth() == 6)
    self.assertTrue(self.width() == 7)

  def test2x1AndTiedLow(self):
    self.createGridAndTieCell0Input(2, 2, 2, 1)

    self.m.driveInputs([True, True])

    self.assertEqual(self.m.sampleOutputs(), [False, False])

  def test2x1AndTiedHigh(self):
    self.createGridAndTieCell0Input(2, 2, 2, 1, True)

    self.m.driveInputs([True, True])

    self.assertEqual(self.m.sampleOutputs(), [True, True])

  def test3x1AndTiedHigh(self):
    self.createGridAndTieCell0Input(3, 3, 3, 1, True)

    self.m.driveInputs([True, True, False])

    self.assertEqual(self.m.sampleOutputs(), [True, True, False])

  def test2x2AndTiedHigh(self):
    self.createGridAndTieCell0Input(2, 2, 2, 2, True)

    self.m.driveInputs([True, True])
    self.assertEqual(self.m.sampleOutputs(), [True, True])

    self.m.driveInputs([True, False])
    self.assertEqual(self.m.sampleOutputs(), [False, False])

  def test3x2AndTiedHigh(self):
    self.createGridAndTieCell0Input(3, 3, 3, 2, True)

    self.m.driveInputs([True, True, True])
    self.assertEqual(self.m.sampleOutputs(), [True, True, True])

    self.m.driveInputs([True, False, True])
    self.assertEqual(self.m.sampleOutputs(), [False, False, False])

  def testFixNumberOfFlopsTo0(self):
    self.createGridAndTieCell0Input(25, 25, 25, 14, True)
    self.m.setNumFlops(0)

    self.assertTrue(self.m.getNumFlops() == 0)

  def testFixNumberOfFlopsToLtWidth(self):
    self.createGridAndTieCell0Input(25, 25, 25, 14, True)
    self.m.setNumFlops(17)

    self.assertTrue(self.m.getNumFlops() == 17)

  def testFixNumberOfFlopsToGtWidth(self):
    self.createGridAndTieCell0Input(25, 25, 25, 14, True)
    self.m.setNumFlops(28)

    self.assertTrue(self.m.getNumFlops() == 28)

  def testFixNumberOfFlopsToMax(self):
    self.createGridAndTieCell0Input(25, 25, 25, 14, True)
    self.m.setNumFlops(25 * 14)

    self.assertTrue(self.m.getNumFlops() == (25 * 14))

  def test2x1FloppedAndTiedHigh(self):
    self.createGridAndTieCell0Input(2, 2, 2, 1, True)
    self.m.setNumFlops(2)

    self.m.driveInputs([True, True])

    self.m.clk()
    self.assertEqual(self.m.sampleOutputs(), [True, False])

    self.m.clk()
    self.assertEqual(self.m.sampleOutputs(), [True, True])

  def testOutputMuxOnlyExistsWhenOutputSmallerThanInputWidth(self):
    self.createGridAndTieCell0Input(2, 2, 2)
    self.assertEqual(self.m.outputMux, None)

  def testOutputMuxForMoreInputsThanOutputs(self):
    self.createGridAndTieCell0Input(2, 1, 2)
    self.assertNotEqual(self.m.outputMux, None)

  def testOutputSizeFor2Inputs1Output(self):
    self.createGridAndTieCell0Input(2, 1, 2)
    self.m.driveInputs([True, True])
    self.assertEqual(len(self.m.sampleOutputs()), 1)

  def testOutputFor2Inputs1Output(self):
    self.createGridAndTieCell0Input(2, 1, 2, 1, True)
 
    self.m.driveInputs([True, True])
 
    self.assertEqual(self.m.sampleOutputs(), [ True ])
 
  def testOutputFor3Inputs2Output(self):
    self.createGridAndTieCell0Input(3, 2, 3, 1, True)
 
    self.m.driveInputs([True, True, False])
 
    self.assertEqual(self.m.sampleOutputs(), [ True, False ])
 
  def testOutputFor4Inputs3Output(self):
    self.createGridAndTieCell0Input(4, 3, 4, 1, True)
 
    self.m.driveInputs([True, True, True, False])
 
    self.assertEqual(self.m.sampleOutputs(), [ True, True, False ])
 
  def testOutputFor5Inputs4Output(self):
    self.createGridAndTieCell0Input(5, 4, 5, 1, True)
 
    self.m.driveInputs([True, True, True, False, False])
 
    self.assertEqual(self.m.sampleOutputs(), [ True, True, False, False ])
 
  def testOutputFor8Inputs5Output(self):
    self.createGridAndTieCell0Input(8, 5, 8, 1, True)
 
    self.m.driveInputs([True] * 6 + [False, False])
 
    self.assertEqual(self.m.sampleOutputs(), [ True, True, True, False, False ])

  def testModuleHasFixedCells(self):
    self.createGridAndTieCell0Input(2, 2, 2)
    self.m.setNumFlops(2)
    self.m.driveInputs([True] * 2)
    self.m.clk()
    self.m.sampleOutputs()
    self.m.clk()
    self.m.sampleOutputs()
    self.assertTrue(self.m.moduleHasFixedCells())

  def testModuleHasNoFixedCells(self):
    self.createGridAndTieCell0Input(2, 2, 2, 1, True)
    self.m.cells[0][1].setOutputType(OutputType.sync)
    self.m.driveInputs([True] * 2)
    self.m.clk()
    self.m.sampleOutputs()
    self.m.driveInputs([False] * 2)
    self.m.clk()
    self.m.sampleOutputs()
    self.assertFalse(self.m.moduleHasFixedCells())

  def testOutputHistory(self):
    self.createGridAndTieCell0Input(2, 2, 2, 1, True)

    self.m.driveInputs([True, True])
    self.m.sampleOutputs()
    self.m.sampleOutputs()
    self.m.sampleOutputs()
    self.assertEqual(len(self.m.outputHistory()), 3)
    self.assertEqual(self.m.outputHistory(), [ [True, True], [True, True], [True, True] ])
    self.assertTrue(self.m.outputsFixed())

  def testOutputsNotFixed(self):
    self.createGridAndTieCell0Input(2, 2, 2, 1, True)
 
    self.m.driveInputs([True, True])
    self.m.sampleOutputs()
    self.m.driveInputs([False, False])
    self.m.sampleOutputs()
    self.assertFalse(self.m.outputsFixed())
 
  def testOutputFor1Input2Outputs(self):
    self.createGridAndTieCell0Input(1, 2, 2, 1, True)
 
    self.m.driveInputs([True])
 
    self.assertEqual(self.m.sampleOutputs(), [ True, True ])
 
  def testOutputFor2Input4Outputs(self):
    self.createGridAndTieCell0Input(2, 4, 4, 1, True)
 
    self.m.driveInputs([True, True])
 
    self.assertEqual(self.m.sampleOutputs(), [ True, True ] * 2)
 
  def testOutputForLargerGridWidth(self):
    self.createGridAndTieCell0Input(2, 4, 6, 1, True)
 
    self.m.driveInputs([True, True])
 
    self.assertEqual(self.m.sampleOutputs(), [ True, True ] * 2)



class MuxTests (unittest.TestCase):
  def setUp(self):
    self.m = Mux()

  def tearDown(self):
    pass

  def testInputSelect2InputSelect0(self):
    self.m.driveInputs([False, True])
    self.assertEqual(self.m.inputSelect(), 0)

  def testInputSelect2InputSelect1(self):
    self.m.driveInputs([True, True])
    self.assertEqual(self.m.inputSelect(), 1)

  def testInputSelect3InputSelect0(self):
    self.m.driveInputs([False, False, True])
    self.assertEqual(self.m.inputSelect(), 0)

  def testInputSelect3InputSelect1(self):
    self.m.driveInputs([True, False, True])
    self.assertEqual(self.m.inputSelect(), 1)

  def testInputSelect3InputSelect2(self):
    self.m.driveInputs([False, True, True])
    self.assertEqual(self.m.inputSelect(), 2)

  def testInputSelect3InputSelectOverflow(self):
    self.m.driveInputs([True, True, True])
    self.assertEqual(self.m.inputSelect(), 2)

  def testInputSelect4InputSelect3(self):
    self.m.driveInputs([True, True, True, False])
    self.assertEqual(self.m.inputSelect(), 3)

  def test2InputSelect0(self):
    self.m.driveInputs([False, False])
    self.assertFalse(self.m.asyncOutput())
 
  def test2InputSelect1(self):
    self.m.driveInputs([True, True])
    self.assertTrue(self.m.asyncOutput())
 
  def test4InputSelect3(self):
    self.m.driveInputs([True, True, True, False])
    self.assertFalse(self.m.asyncOutput())


if __name__ == "__main__":
  unittest.main()
