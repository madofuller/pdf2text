import streamlit as st
import os
import time
import platform
from tempfile import TemporaryDirectory
from pathlib import Path
import pdf2image
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from tempfile import TemporaryDirectory

from io import StringIO



#title widget
title = st.title("Select folder of PDFs to convert to raw text")


PDF_File = st.file_uploader("Choose an image", type=["pdf"])
button = st.button("Confirm")
flag_file_processed = False

if button and PDF_File is not None:

	if PDF_File.type == "application/pdf":
		images = pdf2image.convert_from_bytes(PDF_File.read())
		output_text = ''
		for page_enumeration, page in enumerate(images, start=1):
			filename = f"page_{page_enumeration:03}.jpg"
			page.save(filename, "JPEG")
			with st.spinner('Extracting Text from given Image'):
				image_file = (filename)
				im = Image.open(image_file)
				text = pytesseract.image_to_string(im)
			output_text = output_text + '\n' + text

		# save output text to file and show
		#st.text_area(output_text)
		#transcribed_file = open(PDF_File.name[:-4] + '.txt', "w")
		#transcribed_file.write(output_text)
		#transcribed_file.close()
		flag_file_processed = True

	if flag_file_processed:
		st.download_button("Download transcibed", output_text)