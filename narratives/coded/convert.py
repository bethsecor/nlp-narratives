import subprocess

def convert_doc2docx(doc, destination):
    subprocess.call(['/opt/libreoffice6.1/program/soffice', '--headless', '--convert-to', 'docx', doc, "--outdir", destination])

