class Document:

  def __init__(self, filename, title):
    self.filename = filename
    self.contents = []


class Title:
  def __init__(self, title_str):
    self.title_str = title_str
  
  def stringify(self):
    """
    \begin{minipage}{\textwidth}%
    \centering%
    \begin{Large}%
    \textbf{PEP 8 {-}{-} Style Guide for Python Code}%
    \end{Large}%
    \end{minipage}%
    """
    textbf = Command('textbf', self.title_str)
    Large = BeginEndCommand('Large', inside_commands=[textbf])
    minipage = BeginEndCommand('minipage', inside_commands=[Large], attribute='textwidth') 
    return minipage.stringify()

class Text:
  
  def __init__(self, content):
    self.content = str(content)
  
  def stringify(self):
    text = self.content
    # Do some stuff with text
    text = text.replace('%', '{%}')
    return text

class Command:
  
  def __init__(self, command, argument=''):
    self.command = command
    self.argument = argument
  
  def stringify(self):
    return f"""\\{self.command}{'{' + self.argument + '}' if self.argument != '' else ''}"""

class BeginEndCommand:

  def __init__(self, command, inside_commands, parameters=[], attribute=''):
    self.command = command
    self.parameters = parameters
    self.attribute = attribute
    self.inside_commands = inside_commands

  def stringify_parameters(self):
    if self.parameters == []:
      return ''
    
    s = str(self.parameters)
    s = s.replace("'", "").replace('"', '')
    return s

  def stringify_attribute(self):
    if self.attribute == '':
      return ''
    else:
      return '{' + Command(self.attribute).stringify() + '}'
  
  def stringify(self):
    begin = f"""\\begin{'{' + self.command + '}'}{self.stringify_parameters()}{self.stringify_attribute()}"""
    body = '\n\n'.join([command.stringify() for command in self.inside_commands])
    end = f"""\\end{'{' + self.command + '}'}"""

    return '\n'.join([begin, body, end])