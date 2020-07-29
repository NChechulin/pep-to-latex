from bs4 import BeautifulSoup
import requests
from mylatex import *
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
        doc.append(Title(title))

    elif child.name == 'div' and child.has_attr('class') and child['class'][0] == 'section':
        title = get_section_title(child)
        children = child.findChildren()

        if child.parent.name == 'article':
            doc.append(Section(title))

            for c in children:
                parse_child(c)
        else:
            doc.append(SubSection(title))

            for c in children:
                parse_child(c)

    elif child.name == 'p':
        doc.append(Text(child.text))

    elif child.name == 'pre' and child.has_attr('class') and child['class'][0] == 'literal-block':
        doc.append(Code(child.text))


if __name__ == '__main__':
    pep_number = input('Input PEP number (e.g 8): ')
    filename = f'pep-{pep_number.zfill(4)}'

    doc = Document(filename + '.tex', filename)

    init_soup(f'https://www.python.org/dev/peps/{filename}/')
    article = soup.find('article')

    for child in article.findChildren(recursive=False):
        parse_child(child)

    with open(filename + '.tex', 'w') as f:
        print(doc.stringify(), file=f)

    print(f'Done! Written data to {filename}.tex')
