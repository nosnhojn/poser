import re

class IO:
  def __init__(self, type, name, size = '1'):
    self.type = re.sub('^\s*(.*)\s*$', '\\1', type)
    self.name = re.sub('\s*', '', name)
    self.size = re.sub('\s*', '', size)

  def __eq__(self, other):
    return self.type == other.type and \
           self.name == other.name and \
           self.size == other.size

  def __str__(self):
    return 'type:%s name:%s size:%s' % (self.type, self.name, self.size)


class ModuleParser:
  def __init__(self):
    self.moduleName = ''
    self.inputs = []
    self.outputs = []



  def parse(self, fileStr):
    moduleText = self.scrubModule(fileStr)

    # module name
    self.moduleName = self.getModuleNameFromString(moduleText)

    # non-ANSI
    self.inputs = self.parsePorts('input', moduleText)
    self.outputs = self.parsePorts('output', moduleText)

  def scrubModule(self, str):
    # full line comments
    ret = re.sub(r'//.*\n', ' ', str)

    # remove the \n
    ret = re.sub(r'\n', ' ', ret)

    # remove the /* */ comments
    ret = re.sub(r'/\*.*?\*/', '', ret)

    # module -> endmodule inclusive
    ret = re.sub(r'.*(\bmodule\b.*\bendmodule\b).*', '\\1', ret)

    return ret

  def getModuleNameFromString(self, str):
    matchObj = re.search(r'^module\s*(\w+)\b', str)
    return matchObj.group(1)
    
  def getVectorSizeFromString(self, str):
    vector = re.search(r'\[(.*):(.*)\]', str)
    if vector:
      size = '%s-%s+1' % (vector.group(1), vector.group(2))
    else:
      size = '1'

    return size

  def getTypeFromString(self, str):
    return re.sub(r'\s*\[.*', '', str)

  def getNamesFromString(self, str):
    return re.split(',', str)
 
  def portsIter(self, type, str):
    # (type ([])) (name, other names, etc);
    return re.finditer( r'(\b%s\b(?:\s*\[.*\])?)\s*(\w+((?:\s*,\s*(?!input|output)\w+\s*)*))\s*' % type, str)

  def parsePorts(self, type, str):
    ports = []
    _ports = self.portsIter(type, str)
    for _p in _ports:
      _type = self.getTypeFromString(_p.group(1))
      _size = self.getVectorSizeFromString(_p.group(1))
      _name = self.getNamesFromString(_p.group(2))
      for _n in _name:
        ports.append(IO(_type, _n, _size))

    return ports

  def getModuleName(self):
    return self.moduleName

  def getInputs(self):
    return self.inputs

  def getOutputs(self):
    return self.outputs
