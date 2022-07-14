from tkinter import filedialog, ttk
from ttkthemes import ThemedTk
from tkinter.ttk import *
from tkinter import *
import tkinter.filedialog as fd
import os
import time
import platform
from tempfile import TemporaryDirectory
from pathlib import Path
from tqdm import tqdm
 
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

global folder_source
global file_source
global folder_bool

#tkinter window
win = ThemedTk(theme='yaru')

#tkinter window size
win.geometry("700x700")

file_source = StringVar()
file_source.set("Nothing")

folder_source = StringVar()

folder_source.set("Nothing")

output_folder_path = StringVar()
output_folder_path.set("Nothing")

def open_file():
   global file_source
   file = fd.askopenfilenames(parent=win, title='Choose a File')
   print(type(file))
   print(f"fsource= {file_source.get()}")
   file_source.set(file[0])
   print(f"updating folder source to {file}")
   file_name = file_source.get().split('/')[-1][:-4]
   print(f"file name: {file_name}")

def open_folder():
   global folder_source
   folder = filedialog.askdirectory(parent=win, title='Choose a Folder')
   print(type(folder))
   print(f"fsource= {folder_source.get()}")
   folder_source.set(folder)
   print(f"updating folder source to {folder}")

def create_folder():
   global output_folder_path
   output = fd.askdirectory(parent=win, title='Ouput files in this folder')
   print(type(output))
   print(f"fsource= {output_folder_path.get()}")
   output_folder_path.set(output)
   print(f"updating output folder to {output}")


#Label widget
Label = Label(win, text="Select folder of PDFs to convert to raw text", font=('Aerial 11'))
Label.pack(pady=30)

#Checkbox
folder_bool = BooleanVar()
ttk.Checkbutton(win, text='Run Folder',variable=folder_bool, onvalue=True, offvalue=False).pack()



#Button Widget
ttk.Button(win, text="Select a Folder", command=open_folder).pack(padx=15, pady=20)

ttk.Label(win, textvariable=folder_source, font=('Aerial 11')).pack(pady=20)




#Button Widget
ttk.Button(win, text="Select a File", command=open_file).pack(padx=15, pady=20)

ttk.Label(win, textvariable=file_source, font=('Aerial 11')).pack(pady=20)



def Converter():

	def tool(PDF_file, text_file):
	    image_file_list = []
	    with TemporaryDirectory() as tempdir:

	        
	        if platform.system() == "Windows":
	            pdf_pages = convert_from_path(
	                PDF_file, 500, poppler_path=path_to_poppler_exe
	            )
	        else:
	            pdf_pages = convert_from_path(PDF_file, 500)

	        for page_enumeration, page in enumerate(pdf_pages, start=1):


	            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"

	            page.save(filename, "JPEG")
	            image_file_list.append(filename)

	        with open(text_file, "a") as output_file:

	            for image_file in image_file_list:

	                opened_image = Image.open(image_file)

	                text = str(pytesseract.image_to_string(opened_image))

	                text = text.replace("-\n", "")


	                output_file.write(text)

	     
	if __name__ == "__main__":
		#global folder_source
		global file_source
		global folder_bool
		global output_folder_path

		if output_folder_path.get() == "Nothing":
			return

		if platform.system() == "Windows":
		    pytesseract.pytesseract.tesseract_cmd = (
		        r"C:/Users/matthf8/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
		    )

		    path_to_poppler_exe = Path(r"C:\Users\matthf8\Projects\poppler-22.04.0\Library\bin")
		     
		    out_directory = Path(r"~\Desktop").expanduser()
		else:
		    out_directory = Path("~").expanduser()    
		 

		if folder_bool.get():
			print(f'Running folder for {folder_source.get()}')

			file_list = [file_name for file_name in os.listdir(folder_source.get()) if ".pdf" in file_name]
			pbar = tqdm(file_list)

			for file_name in pbar:
				PDF_file = Path(rF"{folder_source.get()}/{file_name}")
				text_file = Path(rf"{output_folder_path.get()}/{file_name[:-4]}_interpreted.txt")

				pbar.set_description(f"Converting {file_name}")

				tool(PDF_file, text_file)

		else:
			print(f"Running file for {file_source.get()}")	

			file_name = Path(rf"{output_folder_path.get()}/{file_source.get().split('/')[-1][:-4]}_interpreted.txt")
			pbar = tqdm(file_name)

			pbar.set_description(f"Converting {file_name}")

			tool(file_source.get(), file_name)

		return
		PDF_file = Path(rf"{folder_source}/{file_name}.pdf")
		 
		
#Button Widget
ttk.Button(win, text="Where to Save?", command=create_folder).pack(padx=15, pady=20)

ttk.Label(win, textvariable=output_folder_path, font=('Aerial 11')).pack(pady=20)
		
		

B=ttk.Button(win, text="Convert PDFs to raw text", command=Converter)	
B.pack(padx=15, pady=20)


 


    
win.mainloop()