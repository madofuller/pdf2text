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


imagem_referencia = st.file_uploader("Choose an image", type=["pdf"])
button = st.button("Confirm")

if button and imagem_referencia is not None:

	if imagem_referencia.type == "application/pdf":
		images = pdf2image.convert_from_bytes(imagem_referencia.read())
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
		st.text_area(output_text)
