import zipfile
import xml.dom.minidom
import xml.etree.ElementTree
import pandas

def parse_atlas_output(docx):
    document = zipfile.ZipFile(docx)
    
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'
    
    tree = xml.etree.ElementTree.XML(document.read('word/document.xml'))
    document.close()
    
    code = ""
    code_series = []
    segment_series = []
    for paraElement in tree.iter(PARA):
        texts = [node.text
                 for node in paraElement.iter(TEXT)
                 if node.text]
        if texts and texts[0] in("○","●"):
            code = texts[2].strip()
        elif texts and code != "":
            segment = ''.join(texts)
            ss = segment.split(' ')
            if not ((len(ss) >= 2 and ss[1] in('Quotations:','Codes:')) or len(ss[0].split(':')) == 2):
                code_series.append(code)
                segment_series.append(segment)
    code_segment_df = pandas.DataFrame({"code": code_series, "segment": segment_series})
    return(code_segment_df)
