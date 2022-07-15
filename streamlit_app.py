import streamlit as st
import os
import pdf2image
from pdf2image import convert_from_path
from PIL import Image
from time import sleep
import pytesseract
from io import StringIO
from stqdm import stqdm


#title widget
title = st.title("Select scanned PDF to convert to raw text")


PDF_File = st.file_uploader("Choose PDF file", type=["pdf"])
button = st.button("Convert", )
flag_file_processed = False

if button and PDF_File is not None:

	if PDF_File.type == "application/pdf":
		images = pdf2image.convert_from_bytes(PDF_File.read())
		output_text = ''
		for page_enumeration, page in enumerate(images, start=1):
			filename = f"page_{page_enumeration:03}.jpg"
			page.save(filename, "JPEG")
			my_bar = st.progress(0)
			for my_bar in stqdm(range(50), desc="This is a slow task", mininterval=1):
				sleep(0.5)
				image_file = (filename)
				im = Image.open(image_file)
				text = pytesseract.image_to_string(im)
			output_text = output_text + '\n' + text

		flag_file_processed = True

	if flag_file_processed:
		st.download_button("Download transcibed", output_text)