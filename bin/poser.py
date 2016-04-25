import re

class ModuleParser:
  def __init__(self):
    self.moduleName = ''
    self.inputs = []
    self.outputs = []

  def parse(self, fileStr):
    # full line comments
    fileStr = re.sub(r'//.*\n', ' ', fileStr)

    # remove the \n
    fileStr = re.sub(r'\n', ' ', fileStr)

    # remove the /* */ comments
    fileStr = re.sub(r'/\*.*?\*/', '', fileStr)

    # module -> endmodule inclusive
    matchObj = re.search(r'.*(\bmodule\b.*\bendmodule\b).*', fileStr)
    fileStr = matchObj.group(1)

    # module name
    matchObj = re.search(r'^module\s*(\w+)\b', fileStr)
    self.moduleName = matchObj.group(1)

    # non-ANSI
    self.inputs = self.nonAnsiPorts('input', fileStr)
    self.outputs = self.nonAnsiPorts('output', fileStr)

 
  def nonAnsiPorts(self, type, str):
    ports = []
    _ports = re.finditer(r'(\b%s\b(?:\s*\[.*\])?)\s*(\w+)((?:\s*,\s*\w+\s*)*)\s*;' % type, str)
    for _p in _ports:
      ports.append('%s %s;' % (_p.group(1), _p.group(2)))
      if _p.group(3):
        others = re.sub(' ', '', _p.group(3))
        others = re.split(',', others)
        for o in others:
          if o != '':
            ports.append('%s %s;' % (_p.group(1), o))

    return ports

  def getModuleName(self):
    return self.moduleName

  def getInputs(self):
    return self.inputs

  def getOutputs(self):
    return self.outputs
