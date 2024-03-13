import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

root = tk.Tk()
root.title('PDF Merger')

label = tk.Label(root, text="Select PDF files to merge")
label.pack()

select_button = tk.Button(root, text="Select Files", command=lambda: select_files())
merge_button = tk.Button(root, text="Merge PDFs", command=lambda: merge_pdfs())
select_button.pack()
merge_button.pack()


def select_files():
    global pdf_files
    pdf_files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if not pdf_files:
        messagebox.showwarning("Warning", "No file selected.")
    else:
        messagebox.showinfo("Success", "Files selected successfully.")


def merge_pdfs():
    if not pdf_files:
        messagebox.showwarning("Warning", "Please select PDF files to merge.")
        return

    merger = PyPDF2.PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)

    output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_filename:
        messagebox.showwarning("Warning", "No output file selected.")
        return

    merger.write(output_filename)
    merger.close()
    messagebox.showinfo("Success", "PDFs merged successfully.")

root.mainloop()


