import streamlit as st
import os
import pdf2image
from pdf2image import convert_from_path
from PIL import Image
import pytesseract



#title widget
title = st.title("Select scanned PDF to convert to raw text")


PDF_File = st.file_uploader("Choose PDF file", type=["pdf"])
text_file_name = 'unnamed_file'
button = st.button("Convert")
flag_file_processed = False

if button and PDF_File is not None:

	if PDF_File.type == "application/pdf":
		images = pdf2image.convert_from_bytes(PDF_File.read())
		output_text = ''
		for page_enumeration, page in enumerate(images, start=1):
			filename = f"page_{page_enumeration:03}.jpg"
			page.save(filename, "JPEG")
			with st.spinner(f'Extracting text from given PDF: page_{page_enumeration:03}'):
				image_file = (filename)
				im = Image.open(image_file)
				text = pytesseract.image_to_string(im)
			output_text = output_text + text + '\n'

		flag_file_processed = True
		text_file_name = PDF_File.name[:-4] + '.txt'

	if flag_file_processed:
		st.download_button("Download transcibed", output_text, file_name=text_file_name)