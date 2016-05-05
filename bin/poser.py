import re
import random
import argparse

class IO:
  def __init__(self, type, name, msb = '', lsb = ''):
    self.type = re.sub('^\s*(.*)\s*$', '\\1', type)
    self.name = re.sub('\s*', '', name)
    self.msb = re.sub('\s*', '', msb)
    self.lsb = re.sub('\s*', '', lsb)

  def __eq__(self, other):
    return self.type == other.type and \
           self.name == other.name and \
           self.msb == other.msb and \
           self.lsb == other.lsb

  def __str__(self):
    return 'type:%s name:%s msb:%s lsb:%s' % (self.type, self.name, self.msb, self.lsb)


class Active:
  lo = 0
  hi = 1


class ModuleParser:
  def __init__(self):
    self.moduleName = ''
    self.ansiParams = ''
    self.nonAnsiParams = ''
    self.inputs = []
    self.outputs = []
    self.preamble = []
    self.gridWidth = 0
    self.gridDepth = 0
    self.clkName = ''
    self.rstName = ''
    self.cellTypes = []

  def setGridSize(self, width, depth):
    self.gridWidth = width
    self.gridDepth = depth
    self.cellTypes = [ x[:] for x in [['0']*self.gridWidth]*self.gridDepth ]

  def likelihood(self):
    # n = random.randint(0,999)
    n = random.randint(0,999)
    if n < 1:
      return True
    else:
      return False

  def setNumFlops(self, n):
    _cnt = 0
    wIdx = 0
    dIdx = 0
    _n = n
    if _n > self.gridWidth * self.gridDepth:
      _n = self.gridWidth * self.gridDepth
    while _cnt < _n:
      if self.cellTypes[dIdx][wIdx] == '0' and self.likelihood():
        self.cellTypes[dIdx][wIdx] = '1'
        _cnt += 1
      wIdx += 1
      if wIdx >= self.gridWidth:
        wIdx = 0
        dIdx += 1
        if dIdx >= self.gridDepth:
          dIdx = 0

  def setClkName(self, name):
    self.clkName = name

  def setRstName(self, name, active):
    self.rstName = name

  def setTied(self, active):
    pass

  def poserParamsAsString(self):
    str  = '  parameter poser_tied = 1\'b1;\n'
    str += '  parameter poser_width_in = %s;\n' % self.getIOWidth(self.inputs)
    str += '  parameter poser_width_out = %s;\n' % self.getIOWidth(self.outputs)
    str += '  parameter poser_grid_width = %s;\n' % self.gridWidth
    str += '  parameter poser_grid_depth = %s;\n' % self.gridDepth
    str += '  parameter [poser_grid_width-1:0] cellTypes [0:poser_grid_depth-1] = \'{ %s };\n' % self.cellTypeArrayAsString()

    return str

  def cellTypeArrayAsString(self):
    str = []
    for i in range(self.gridDepth):
      str.append('%s\'b' % (self.gridWidth) + ''.join(self.cellTypes[i]))

    return ','.join(str)

  def poserGridAsString(self):
    return '''
  wire poser_clk;
  assign poser_clk = %s;
  wire poser_rst;
  assign poser_rst = %s;
  for (genvar D = 0; D < poser_grid_depth; D++) begin
    for (genvar W = 0; W < poser_grid_width; W++) begin
      if (D == 0) begin
        if (W == 0) begin
          poserCell #(.cellType(cellTypes[D][W]), .activeRst(0)) pc (.clk(poser_clk),
                                                                     .rst(poser_rst),
                                                                     .i(^{ poser_tied ,
                                                                           poser_inputs[W%%poser_width_in] }),
                                                                     .o(poser_grid_output[D][W]));
        end else begin
          poserCell #(.cellType(cellTypes[D][W]), .activeRst(0)) pc (.clk(poser_clk),
                                                                     .rst(poser_rst),
                                                                     .i(^{ poser_grid_output[D][W-1],
                                                                           poser_inputs[W%%poser_width_in] }),
                                                                     .o(poser_grid_output[D][W]));
        end
      end else begin
        if (W == 0) begin
          poserCell #(.cellType(cellTypes[D][W]), .activeRst(0)) pc (.clk(poser_clk),
                                                                     .rst(poser_rst),
                                                                     .i(^{ poser_grid_output[D-1][W],
                                                                           poser_grid_output[D-1][poser_grid_depth-1] }),
                                                                     .o(poser_grid_output[D][W]));
        end else begin
          poserCell #(.cellType(cellTypes[D][W]), .activeRst(0)) pc (.clk(poser_clk),
                                                                     .rst(poser_rst),
                                                                     .i(^{ poser_grid_output[D-1][W],
                                                                           poser_grid_output[D][W-1] }),
                                                                     .o(poser_grid_output[D][W]));
        end
      end
    end
  end
  generate
    if (poser_width_out == 1) begin
      poserMux #(.poser_mux_width_in(poser_grid_width)) pm (.i(poser_grid_output[poser_grid_depth-1]),
                                                            .o(poser_outputs));
    end
    else if (poser_grid_width == poser_width_out) begin
      assign poser_outputs = poser_grid_output[poser_grid_depth-1];
    end
    else if (poser_grid_width > poser_width_out) begin
      wire [poser_grid_width-1:0] poser_grid_output_last;
      assign poser_grid_output_last = poser_grid_output[poser_grid_depth-1];
      poserMux #(.poser_mux_width_in((poser_grid_width - poser_width_out) + 1)) pm (.i(poser_grid_output_last[poser_grid_width-1:poser_width_out-1]),
                                                                                   .o(poser_outputs[poser_width_out-1]));
      assign poser_outputs[poser_width_out-2:0] = poser_grid_output_last[poser_width_out-2:0];
    end
  endgenerate\n''' % (self.clkName, self.rstName)

  def poserGridOutputsAsString(self):
    str  = '  wire [poser_grid_width-1:0] poser_grid_output [0:poser_grid_depth-1];\n'
    return str

  def poserInternalInputsAsString(self):
    return '  wire [poser_width_in-1:0] poser_inputs;\n  assign poser_inputs = { %s };\n' % ",".join([ i.name for i in self.inputs if i.name != self.clkName and i.name != self.rstName ])

  def poserInternalOutputsAsString(self):
    return '  wire [poser_width_out-1:0] poser_outputs;\n  assign { %s } = poser_outputs;\n' % ",".join([ i.name for i in self.outputs ])

  def getIOWidth(self, io):
    _io_width = '0'
    for _io in io:
      if _io.name != self.clkName and _io.name != self.rstName:
        if _io.msb != '':
          _io_width += '+%s-%s+1' % (_io.msb, _io.lsb)
        else:
          _io_width += '+1'
    return _io_width

  def nonAnsiParametersAsString(self):
    _params = [ ('  %s\n' % x) for x in self.nonAnsiParams ]
    return "".join(_params)

  def ansiParametersAsString(self):
    return self.ansiParams

  def preambleAsString(self):
    _preamble = ''
    for _p in self.preamble:
      if re.search('\S', _p):
        _preamble = '%s%s\n' % (_preamble, _p)

    return _preamble

  def moduleAsString(self):
    _module  = self.preambleAsString()
    _module += 'module %s' % self.moduleName

    if self.ansiParams:
      _module  += ' #(%s)' % self.ansiParams

    _module += '(%s);\n' % self.moduleIOAsString()

    if self.nonAnsiParams:
      _module  += self.nonAnsiParametersAsString()

    _module += self.modulePortsAsString()

    if self.gridDepth * self.gridWidth > 0:
      _module += self.poserParamsAsString()
      _module += self.poserInternalInputsAsString()
      _module += self.poserInternalOutputsAsString()
      _module += self.poserGridOutputsAsString()
      _module += self.poserGridAsString()

    _module += 'endmodule\n'

    return _module

  def moduleIOAsString(self):
    _io = [ x.name for x in self.inputs + self.outputs ]
    return ', '.join(_io)

  def modulePortsAsString(self):
    _ports = ''
    for _p in self.inputs + self.outputs:
      if _p.msb == '':
        _ports += '  %s %s;\n' % (_p.type, _p.name)
      else:
        _ports += '  %s [%s:%s] %s;\n' % (_p.type, _p.msb, _p.lsb, _p.name)

    return _ports

  def parse(self, fileStr):
    moduleText = self.scrubModule(fileStr)

    # module name
    self.moduleName = self.getModuleNameFromString(moduleText)

    # ansi style parameters
    self.ansiParams = self.getAnsiParamsFromString(moduleText)

    # non ansi style parameters
    self.nonAnsiParams = self.getNonAnsiParamsFromString(moduleText)

    # non-ANSI
    self.inputs = self.parsePorts('input', moduleText)
    self.outputs = self.parsePorts('output', moduleText)

  def scrubModule(self, str):
    # full line comments
    ret = re.sub(r'//.*\n', ' ', str)

    # remove the /* */ comments
    ret = re.sub(r'/\*[^(\*/)]*\*/', '', ret)

    # extract the preamble
    self.preamble = re.split('\n', ret)
    for i in range(len(self.preamble)):
      if re.match('\s*module\s+', self.preamble[i]):
        self.preamble = self.preamble[:i]
        break

    # remove the \n
    ret = re.sub(r'\n', ' ', ret)

    # module -> endmodule inclusive
    ret = re.sub(r'.*(\bmodule\b.*\bendmodule\b).*', '\\1', ret)

    # scrub reg, wire and logic from everywhere (so they don't appear in the output types)
    ret = re.sub(r'\breg\b', '', ret)
    ret = re.sub(r'\bwire\b', '', ret)
    ret = re.sub(r'\blogic\b', '', ret)

    return ret

  def getModuleNameFromString(self, str):
    matchObj = re.search(r'^module\s+(\w+)\b', str)
    return matchObj.group(1)

  def getAnsiParamsFromString(self, str):
    matchObj = re.search(r'^module\s+\w+\s*#\((.*?)\)', str)
    if matchObj:
      return matchObj.group(1)
    else:
      return ''

  def getNonAnsiParamsFromString(self, str):
    return re.findall(r'(\bparameter\b.*?;)', str)
    
  def getVectorMsbLsbFromString(self, str):
    vector = re.search(r'\[(.*):(.*)\]', str)
    if vector:
      _MsbLsb = (vector.group(1), vector.group(2))
    else:
      _MsbLsb = ['', '']

    return _MsbLsb

  def getTypeFromString(self, str):
    return re.sub(r'\s*\[.*', '', str)

  def getNamesFromString(self, str):
    return re.split(',', str)
 
  def portsIter(self, type, str):
    # (type ([])) (name, other names, etc);
    return re.finditer( r'(\b%s\b(?:\s*\[.*?\])?)\s*(\w+((?:\s*,\s*(?!input|output)\w+\s*)*))\s*' % type, str)

  def parsePorts(self, type, str):
    ports = []
    _ports = self.portsIter(type, str)
    for _p in _ports:
      _type = self.getTypeFromString(_p.group(1))
      [ _msb, _lsb ] = self.getVectorMsbLsbFromString(_p.group(1))
      _name = self.getNamesFromString(_p.group(2))
      for _n in _name:
        ports.append(IO(_type, _n, _msb, _lsb))

    return ports

  def getModuleName(self):
    return self.moduleName

  def getInputs(self):
    return self.inputs

  def getOutputs(self):
    return self.outputs


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Create a verilog module based on flop and size estimates.')
  parser.add_argument('-f', '--flops', type=int, required=True, help='estimated number of flops.')
  parser.add_argument('-s', '--size', choices=['xs', 's', 'm', 'l', 'xl', 'xxl', 'xxxl' ], required=True, help='relative size estimate.')
  parser.add_argument('-v', '--verilog', metavar='FILE', required=True, help='path to the verilog file with an existing module definition.')
  parser.add_argument('-i', '--inputs', type=int, metavar='INPUT_PINS', required=True, help='Total umber of input pins.')
  parser.add_argument('-o', '--outputs', type=int, metavar='OUTPUT_PINS', required=True, help='Total number of output pins.')

  args = parser.parse_args()

  f = open(args.verilog, 'r')
  _file = f.read()

  mp = ModuleParser()
  mp.parse(_file)

  if args.inputs > args.outputs:
    _xsWidth = args.inputs
  else:
    _xsWidth = args.outputs

  depthFactor = 5

  if args.size == 'xs':
    mp.setGridSize(_xsWidth, depthFactor)
  elif args.size == 's':
    mp.setGridSize(2 * _xsWidth, 3*depthFactor)
  elif args.size == 'm':
    mp.setGridSize(4 * _xsWidth, 6*depthFactor)
  elif args.size == 'l':
    mp.setGridSize(6 * _xsWidth, 9*depthFactor)
  elif args.size == 'xl':
    mp.setGridSize(10 * _xsWidth, 12*depthFactor)
  elif args.size == 'xxl':
    mp.setGridSize(20 * _xsWidth, 15*depthFactor)
  elif args.size == 'xxxl':
    mp.setGridSize(40 * _xsWidth, 18*depthFactor)

  while args.flops > (mp.gridWidth * mp.gridDepth)/2:
    mp.setGridSize(mp.gridWidth*2, mp.gridDepth)

  mp.setNumFlops(args.flops)

  print(mp.moduleAsString())

  f.close()
