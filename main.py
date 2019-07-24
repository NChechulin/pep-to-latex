from bs4 import BeautifulSoup
import requests
from pylatex import Document, Section, Subsection, Command

soup = None
doc = None

def add_section(section_name):
    global doc
    with doc.create(Section(section_name)):
        doc.append(f'this is section {section_name}')


# def fill_document(doc):
#     with doc.create(Section('A section')):
#         doc.append('Some regular text and some ')
#         doc.append(italic('italic text. '))

#         with doc.create(Subsection('A subsection')):
#             doc.append('Also some crazy characters: $&#{}')

def init_soup(url):
    global soup
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')

def get_sections():
    global soup
    return soup.findAll('div', {'class': 'section'})

def get_section_title(section_div):
    a_tag = section_div.find('a', {'class' : 'toc-backref'})
    return a_tag.text

if __name__ == '__main__':
    doc = Document('basic')


    init_soup('https://www.python.org/dev/peps/pep-0008/')
    sections = get_sections()

    print(len(sections))

    for sec in sections:
        add_section(get_section_title(sec))

    doc.generate_pdf(clean_tex=True)
    doc.generate_tex()

    # doc = Document('basic')
    # add_section(doc, 'first one')

    