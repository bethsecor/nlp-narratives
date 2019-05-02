from narratives.coded.parse import parse_atlas_output
from narratives.coded.convert import convert_doc2docx
from glob import glob

for doc in glob('./data/*.doc'):
    convert_doc2docx(doc, './data/')
    parse_atlas_output(doc + "x")

