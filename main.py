from bs4 import BeautifulSoup
import requests
from pylatex import Document, Section, Subsection, Command

soup = None


def add_section(doc, section_name):
    with doc.create(Section(section_name)):
        doc.append('this is section {0}'.format(section_name))


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


if __name__ == '__main__':
    init_soup('https://www.python.org/dev/peps/pep-0008/')
    sections = get_sections()

    print(len(sections))

    # doc = Document('basic')
    # add_section(doc, 'first one')

    # doc.generate_pdf(clean_tex=True)
    # doc.generate_tex()