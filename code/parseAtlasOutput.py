import zipfile
import xml.dom.minidom
import xml.etree.ElementTree

document = zipfile.ZipFile('/home/bsecor/ncc-narratives/narratives/docx/C.2 Q16 S+C ALL CREATED CODES.docx')

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

tree = xml.etree.ElementTree.XML(document.read('word/document.xml'))
document.close()

code = ""
data = {}
codes = []
for paraElement in tree.iter(PARA):
    texts = [node.text
             for node in paraElement.iter(TEXT)
             if node.text]
    if texts and texts[0] in("○","●"):
        if code != "": data[code] = codedSegments
        code = texts[1].strip()
        codedSegments = []
        codes.append(texts[1])
    elif texts and code != "":
        codedSegments.append(''.join(texts))

print(data.keys())
print(data)
