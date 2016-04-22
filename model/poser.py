from enum import Enum
import random
import math
import functools

_rn = [ 1, 1, 1, 0, 1 ]

class BaseCell:
  def __init__(self):
    pass

  def clk(self):
    pass


class Rand(BaseCell):
  def clk(self):
    BaseCell.clk(self)
    _rn[4] = _rn[4] ^ _rn[1] % 2
    _rn[3] = _rn[3] ^ _rn[0] % 2
    _rn[2] = _rn[2] ^ _rn[4] % 2
    _rn[1] = _rn[1] ^ _rn[3] % 2
    _rn[0] = _rn[0] ^ _rn[2] % 2

    return       _rn[0] \
           + 2 * _rn[1] \
           + 4 * _rn[2] \
           + 8 * _rn[3] \
           + 16 * _rn[4]

class OutputType(Enum):
  async = 0
  sync = 1

class CellType(Enum):
  _and = 0
  _or = 1
  _xor = 2
  _xnor = 2
  _nand = 3
  _nor = 4

  @staticmethod
  def randOpType():
    n = random.randint(0,99)
    if n < 3:
      return CellType._and
    elif n < 6:
      return CellType._or
    elif n < 9:
      return CellType._nand
    elif n < 12:
      return CellType._nor
    elif n < 15:
      return CellType._xnor
    else:
      return CellType._xor

class Mux(BaseCell):
  def __init__(self):
    self.inputs = []

  def driveInputs(self, inputs):
    self.inputs = inputs

  def inputSelect(self):
    select = 0
    selWidth = int.bit_length(len(self.inputs)-1)
    for i in range(selWidth):
      if self.inputs[i] == True:
        select += 2**i

    if select > len(self.inputs)-1:
      select = len(self.inputs)-1

    return select

  def asyncOutput(self):
    return self.inputs[self.inputSelect()]

  def output(self):
    return self.asyncOutput()


class Cell(BaseCell):
  def __init__(self):
    BaseCell.__init__(self)
    self.inputs = [ ]
    self._syncOutput = False
    self._outputType = OutputType.async
    self.operator = CellType._and
    self.history = []

  def driveInputs(self, inputs):
    self._isStable = (self.inputs == inputs)
    self.inputs = inputs

  def asyncOutput(self):
    if self.operator == CellType._and:
      return functools.reduce(lambda x, y: bool(x & y), self.inputs)
    elif self.operator == CellType._or:
      return functools.reduce(lambda x, y: bool(x | y), self.inputs)
    elif self.operator == CellType._xor:
      return functools.reduce(lambda x, y: bool(x ^ y), self.inputs)
    elif self.operator == CellType._xnor:
      return functools.reduce(lambda x, y: bool(~(x ^ y)), self.inputs)
    elif self.operator == CellType._nand:
      return functools.reduce(lambda x, y: bool(~(x & y)), self.inputs)
    elif self.operator == CellType._nor:
      return functools.reduce(lambda x, y: bool(~(x | y)), self.inputs)

  def syncOutput(self):
    return self._syncOutput

  def output(self):
    o = None
    if self._outputType == OutputType.async:
      o = self.asyncOutput()
    else:
      o = self.syncOutput()

    self.history.append(o)
    return o

  def cellHistory(self):
    return self.history

  def cellHistoryFixed(self):
    numTrue = len([ x for x in self.history if x == True ])
    if numTrue == 0 or numTrue == len(self.history):
      return True

  def clk(self):
    BaseCell.clk(self)
    self._syncOutput = self.asyncOutput()

  def isStable(self):
    return self._isStable

  def setOperator(self, o):
    self.operator = o

  def setOutputType(self, ot):
    self._outputType = ot

  def getOutputType(self):
    return self._outputType

class Module(BaseCell):
  def __init__(self):
    self.cells = []
    self.connectivityMatrix = []
    self.tied = []
    self._inputs = []
    self.widthIn = 0
    self.widthOut = 0
    self.outputMux = None

  def setGridWidths(self, wIn, wOut):
    self.widthIn = wIn
    self.widthOut = wOut

    if self.widthIn > self.widthOut:
      self.outputMux = Mux()

  def gridWidth(self):
    if self.widthIn > self.widthOut:
      return self.widthIn
    else:
      return self.widthOut

  def gridDepth(self):
    return len(self.cells)

  def createGrid(self, widthIn, widthOut, depth):
    self.setGridWidths(widthIn, widthOut)
    cm = [ i for i in range(self.gridWidth()) ]
    for dIdx in range(depth):
      self.cells.append([ Cell() for wIdx in range(self.gridWidth()) ])
      self.tied.append(False)
      random.shuffle(cm)
      self.connectivityMatrix.append(cm)

  def setNumFlops(self, n):
    cnt = 0
    idx = 0
    if n > 0:
      probability = int (n/(self.gridDepth() * self.gridWidth()) * 100)
      while cnt < n:
        dIdx = int(idx/self.gridWidth())
        wIdx = idx%self.gridWidth()
        if self.cells[dIdx][wIdx].getOutputType() == OutputType.async:
          amIaFlop = random.randint(0,99) < probability
          if amIaFlop:
            self.cells[dIdx][wIdx].setOutputType(OutputType.sync)
            cnt += 1
        idx += 1
        if idx >= self.gridWidth() * self.gridDepth():
          idx = 0

  def getNumFlops(self):
    numFlops = 0
    for i in range(self.gridDepth()):
      numFlops += len([ x for x in self.cells[i] if x.getOutputType() == OutputType.sync ])
    return numFlops

  def driveInputs(self, inputs):
    self._inputs = inputs
    self.resolve()

  def gridOutput(self):
    return [ c.output() for c in self.cells[self.gridDepth()-1] ]

  def flopOutputsForRow(self, n):
    flopOutputs = []
    for dIdx in range(self.gridDepth()):
      if self.cells[dIdx][n].getOutputType == OutputType.async:
        flopOutputs.append(self.cells[dIdx][n].output())
    return flopOutputs

  def resolve(self):
    for dIdx in range(self.gridDepth()):
      for wIdx in range(self.gridWidth()):
        if dIdx == 0:
          if wIdx == 0:
            self.cells[0][0].driveInputs([
                                           self._inputs[0],
                                           self.tied[0],
                                        ] + self.flopOutputsForRow(0))
          else:
            self.cells[dIdx][wIdx].driveInputs([
                                                 self._inputs[wIdx],
                                                 self.cells[dIdx][wIdx-1].output(),
                                              ] + self.flopOutputsForRow(wIdx))
        else:
          if wIdx == 0:
            self.cells[dIdx][wIdx].driveInputs([
                                                 self.cells[dIdx-1][self.connectivityMatrix[dIdx][wIdx]].output(),
                                                 self.cells[dIdx-1][self.gridWidth()-1].output(),
                                              ])
          else:
            self.cells[dIdx][wIdx].driveInputs([
                                                 self.cells[dIdx-1][self.connectivityMatrix[dIdx][wIdx]].output(),
                                                 self.cells[dIdx][wIdx-1].output(),
                                              ])

    if self.outputMux:
      if self.widthOut == 1:
        self.outputMux.driveInputs(self.gridOutput())
      else:
        self.outputMux.driveInputs(self.gridOutput()[:(self.widthIn - self.widthOut)])

  def clk(self):
    for dIdx in range(self.gridDepth()):
      for wIdx in range(self.gridWidth()):
        self.cells[dIdx][wIdx].clk()
    self.resolve()

  def tieCell0(self, t):
    self.tied = t

  def sampleOutputs(self):
    if self.gridWidth() == self.widthOut:
      return self.gridOutput()
    else:
      if self.widthOut == 1:
        return [ self.outputMux.output() ]
      else:
        return [ self.outputMux.output() ] + self.gridOutput()[-(self.widthOut - 1):]

  def randomizeGates(self):
    for dIdx in range(self.gridDepth()):
      for wIdx in range(self.gridWidth()):
        if dIdx < self.gridDepth() - 2:
          self.cells[dIdx][wIdx].setOperator(CellType.randOpType())
        else:
          self.cells[dIdx][wIdx].setOperator(CellType._xor)

  def moduleHasFixedCells(self):
    for dIdx in range(self.gridDepth()):
      for wIdx in range(self.gridWidth()):
        if self.cells[dIdx][wIdx].cellHistoryFixed():
          return True

    return False
