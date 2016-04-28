import re

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


class ModuleParser:
  def __init__(self):
    self.moduleName = ''
    self.ansiParams = ''
    self.nonAnsiParams = ''
    self.inputs = []
    self.outputs = []
    self.preamble = ''

  def nonAnsiParametersAsString(self):
    _params = [ ('  %s\n' % x) for x in self.nonAnsiParams ]
    return "".join(_params)

  def ansiParametersAsString(self):
    return self.ansiParams

  def preambleAsString(self):
    return self.preamble

  def moduleAsString(self):
    #_module  = self.preambleAsString()
    _module  = 'module %s' % self.moduleName
    if self.ansiParams:
      _module  += ' #(%s)' % self.ansiParams
    _module += '(%s);\n' % self.moduleIOAsString()
    if self.nonAnsiParams:
      _module  += self.nonAnsiParametersAsString()
    _module += self.modulePortsAsString()
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
    #self.preamble = re.match(r'(.*)(?=\bmodule\b)', ret)
    #self.preamble = re.match(r'(.*?)(?=module)', ret, re.M)
    self.preamble = re.sub(r'\bmodule\b.*', '', ret, re.M)

    # remove the \n
    ret = re.sub(r'\n', ' ', ret)

    # module -> endmodule inclusive
    ret = re.sub(r'.*(\bmodule\b.*\bendmodule\b).*', '\\1', ret)

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