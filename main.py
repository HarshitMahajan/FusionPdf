import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, END
from PyPDF2 import PdfFileReader, PdfFileWriter

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")

        self.pdf_files = []

        list_frame = tk.Frame(root)
        list_frame.pack(pady=20)

        self.scrollbar = Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = Listbox(list_frame, width=50, height=10, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add PDF", command=self.add_pdf)
        add_button.grid(row=0, column=0, padx=10)

        remove_button = tk.Button(button_frame, text="Remove Selected", command=self.remove_pdf)
        remove_button.grid(row=0, column=1, padx=10)

        move_up_button = tk.Button(button_frame, text="Move Up", command=self.move_up)
        move_up_button.grid(row=0, column=2, padx=10)

        move_down_button = tk.Button(button_frame, text="Move Down", command=self.move_down)
        move_down_button.grid(row=0, column=3, padx=10)

        merge_button = tk.Button(button_frame, text="Merge PDFs", command=self.merge_pdfs)
        merge_button.grid(row=0, column=4, padx=10)

    def add_pdf(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            if file.endswith('.pdf'):
                self.pdf_files.append(file)
                self.listbox.insert(END, file)

    def remove_pdf(self):
        selected = self.listbox.curselection()
        for index in reversed(selected):
            del self.pdf_files[index]
            self.listbox.delete(index)

    def move_up(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        for index in selected:
            if index > 0:
                self.pdf_files[index], self.pdf_files[index-1] = self.pdf_files[index-1], self.pdf_files[index]
                self.listbox.insert(index-1, self.listbox.get(index))
                self.listbox.delete(index+1)
                self.listbox.select_set(index-1)

    def move_down(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        for index in reversed(selected):
            if index < self.listbox.size() - 1:
                self.pdf_files[index], self.pdf_files[index+1] = self.pdf_files[index+1], self.pdf_files[index]
                self.listbox.insert(index+2, self.listbox.get(index))
                self.listbox.delete(index)
                self.listbox.select_set(index+1)

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showerror("Error", "No PDF files selected!")
            return

        merged_pdf = PdfFileWriter()
        for pdf_file in self.pdf_files:
            pdf_reader = PdfFileReader(open(pdf_file, "rb"))
            for page in range(pdf_reader.getNumPages()):
                merged_pdf.addPage(pdf_reader.getPage(page))

        output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_filename:
            with open(output_filename, "wb") as outfile:
                merged_pdf.write(outfile)
            messagebox.showinfo("Success", "PDFs merged successfully!")
            self.pdf_files.clear()
            self.listbox.delete(0, END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
