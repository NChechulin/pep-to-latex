from bs4 import BeautifulSoup
import requests
from pylatex import *
from pylatex.utils import *
from pdflatex import PDFLaTeX
import os

soup = None
doc = None


def add_section(section_name):
    global doc
    doc.create(Section(section_name, numbering=False))

def add_subsection(subsection_name):
    global doc
    doc.append(Subsection(subsection_name))

def init_soup(url):
    global soup
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')


def get_sections():
    global soup
    return soup.findAll('div', {'class': 'section'})


def get_section_title(section_div):
    a_tag = section_div.find('a', {'class': 'toc-backref'})
    return a_tag.text

def parse_child(child):
    global doc
    """
    header
    table
    ul + li
    a
    div
    h1, h2, h3, ....
    p
    div class=section
    pre (code)
    """

    if child.name == 'header':
        title = child.find('h1').text
        with doc.create(MiniPage(align='c')):
            doc.append(LargeText(bold(title)))
    elif child.name == 'div' and child.has_attr('class') and child['class'][0] == 'section':
        title = get_section_title(child)
        children = child.findChildren()

        if child.parent.name == 'article':
            with doc.create(Section(title)):
                for c in children:
                    parse_child(c)

        else:
            with doc.create(Subsection(title)):
                for c in children:
                    parse_child(c)
    elif child.name == 'p':
        doc.append(child.text)
    elif child.name == 'pre' and child.has_attr('class') and child['class'][0] == 'literal-block':
        doc.append(dumps_list([r'\begin{lstlisting}[language=Python]'], escape=False))
        doc.append('import numpy as np')
        doc.append(dumps_list([r'\end{lstlisting}'], escape=False))
        
            


if __name__ == '__main__':
    filename = 'pep8'

    doc = Document(filename)
    doc.preamble.append(Command('usepackage', 'listings'))

    init_soup('https://www.python.org/dev/peps/pep-0008/')
    article = soup.find('article')

    for child in article.findChildren(recursive=False):
        parse_child(child)

    doc.generate_tex()
    print('Finished generating TEX!')

    with open(filename + '.tex', 'r') as file:
        data = file.read()
        data = data.replace('%\n', '\n')
        file.close()
    with open(filename + '.tex', 'w') as file:
        file.write(data)
        file.close()


    pdfl = PDFLaTeX.from_texfile(filename + '.tex')
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    print('Finished generating PDF!')