import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

file_name ='/Users/raksingh/Downloads/SAMPLE/sample.pdf'
fd = open(file_name, "rb")
# doc = PDFDocument(fd)
viewer = SimplePDFViewer(fd)

#extract content here
viewer.navigate(1)
viewer.render()
for string in viewer.canvas.strings:
    print(string)
