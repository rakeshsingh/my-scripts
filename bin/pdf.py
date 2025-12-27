from pypdf import PdfReader

from my_scripts.logger import setup_logger

file_name = "/home/mitthoo/Downloads/sample-local-pdf.pdf"
logger = setup_logger()
logger.info(f"workfing on: {file_name}")
reader = PdfReader(file_name)
for page in reader.pages:
    logger.info(page.extract_text())
