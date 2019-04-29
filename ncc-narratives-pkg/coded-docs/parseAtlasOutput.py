import zipfile
import xml.dom.minidom
import xml.etree.ElementTree

def parse_atlas_output(docx):
    document = zipfile.ZipFile(docx)
    
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
            segment = ''.join(texts)
            if not (segment.split(' ')[1] == 'Quotations:' or len(segment.split(' ')[0].split(':')) == 2):
                codedSegments.append(segment)
    print(data)
    return(data)

parse_atlas_output('/home/bsecor/ncc-narratives/data/docx/C.2 Q16 S+C ALL CREATED CODES.docx')
