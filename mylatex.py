class Document:

    def __init__(self, filename, title):
        self.filename = filename
        self.contents = []

    def append(self, content):
        self.contents.append(content)

    def stringify(self):
        data = ''

        packages = [
            ['fontenc', ['T1']],
            ['tikz', []],
            ['textcomp', []],
            ['listings', []],
            ['inputenc', ['utf8']],
            ['babel', ['english', 'russian']],
            ['amssymb', []],
            ['amsmath', []],
            ['hyperref', []],
            ['fancyvrb', []]
        ]

        data += Command('documentclass', argument="article",
                        parameters='').stringify() + '\n'

        for package in packages:
            data += Command('usepackage',
                            argument=package[0], parameters=package[1]).stringify() + '\n'

        self.contents.insert(0, Command('begin', 'document'))
        self.append(Command('end', 'document'))

        for i in self.contents:
            data += i.stringify() + '\n'
        return data


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
        centering = Command('centering')
        Large = BeginEndCommand('Large', inside_commands=[textbf])
        minipage = BeginEndCommand('minipage', inside_commands=[
                                   centering, Large], attribute='textwidth')
        return minipage.stringify()


class Section:
    def __init__(self, section_name):
        self.section_name = section_name

    def stringify(self):
        return Command('section', argument=self.section_name).stringify()


class SubSection:
    def __init__(self, subsection_name):
        self.subsection_name = subsection_name

    def stringify(self):
        return Command('subsection', argument=self.subsection_name).stringify()


class SubSubSection:
    def __init__(self, subsubsection_name):
        self.subsubsection_name = subsubsection_name

    def stringify(self):
        return Command('subsubsection', argument=self.subsubsection_name).stringify()


class Link:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def stringify(self):
        return Command('hyperref', argument=self.url, parameters=[self.title]).stringify()


class Math:
    def __init__(self, math_str, centered):
        self.math_command = math_str
        self.centered = centered

    def stringify(self):
        res = self.math_command
        res = "$" + res + "$"
        if self.centered:
            res = "$" + res + "$"
        return res


class UnorderedList:
    def __init__(self, items=[]):
        self.items = items

    def add_item(self, item):
        self.items.append(item)

    def stringify(self):
        inside_commands = []
        for item in self.items:
            inside_commands.append(Command("item"))
            inside_commands.append(Text(item.stringify()))
        return BeginEndCommand(command="itemize", inside_commands=inside_commands).stringify()


class Code():
    def __init__(self, code):
        self.code = code

    def stringify(self):
        verbatim = BeginEndCommand(
            "Verbatim", [UnformattedText(self.code)], parameters=['samepage=true'])
        return verbatim.stringify()


class Text:
    def __init__(self, content):
        self.content = str(content)

    def stringify(self):
        text = self.content
        text = text.replace('^', '$\hat{\phantom{.}}$')
        text = text.replace('\\', r'\textbackslash ')
        text = text.replace('%', r'\%')
        text = text.replace('_', r'\_')
        text = text.replace('#', r'\#')
        return text


class UnformattedText:
    def __init__(self, content):
        self.content = content

    def stringify(self):
        return str(self.content)


class Command:

    def __init__(self, command, argument='', parameters=[]):
        self.command = command
        self.argument = argument
        self.parameters = parameters

    def stringify(self):
        return f"""\\{self.command}{str(self.parameters).replace("'", "").replace('"', '') if self.parameters != [] else ''}{'{' + self.argument + '}' if self.argument != '' else ''}"""


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

    def append(self, command):
        self.inside_commands.append(command)

    def stringify_attribute(self):
        if self.attribute == '':
            return ''
        else:
            return '{' + Command(self.attribute).stringify() + '}'

    def stringify(self):
        begin = f"""\\begin{'{' + self.command + '}'}{self.stringify_parameters()}{self.stringify_attribute()}"""
        body = '\n\n'.join([command.stringify()
                            for command in self.inside_commands])
        end = f"""\\end{'{' + self.command + '}'}"""

        return '\n'.join([begin, body, end])
