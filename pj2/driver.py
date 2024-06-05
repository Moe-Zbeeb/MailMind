import tkinter as tk
from tkinter import filedialog, messagebox
from main import Main
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Information Extractor")
        self.create_widgets()

    def create_widgets(self):
        # Input Directory
        self.input_label = tk.Label(self.root, text="Input Directory:")
        self.input_label.grid(row=0, column=0, padx=10, pady=5)
        self.input_entry = tk.Entry(self.root, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=5)
        self.input_button = tk.Button(self.root, text="Browse", command=self.browse_input)
        self.input_button.grid(row=0, column=2, padx=10, pady=5)

        # Output File
        self.output_label = tk.Label(self.root, text="Output CSV File:")
        self.output_label.grid(row=1, column=0, padx=10, pady=5)
        self.output_entry = tk.Entry(self.root, width=50)
        self.output_entry.grid(row=1, column=1, padx=10, pady=5)
        self.output_button = tk.Button(self.root, text="Browse", command=self.browse_output)
        self.output_button.grid(row=1, column=2, padx=10, pady=5)

        # Label Entity
        self.label_label = tk.Label(self.root, text="Label Entity:")
        self.label_label.grid(row=2, column=0, padx=10, pady=5)
        self.label_entry = tk.Entry(self.root, width=50)
        self.label_entry.grid(row=2, column=1, padx=10, pady=5)

        # Run Button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_extractor)
        self.run_button.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

    def browse_input(self):
        input_dir = filedialog.askdirectory()
        if input_dir:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_dir)

    def browse_output(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if output_file:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_file)

    def run_extractor(self):
        input_dir = self.input_entry.get()
        output_file = self.output_entry.get()
        label = self.label_entry.get()

        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showerror("Error", "Please select a valid input directory.")
            return

        if not output_file or os.path.isdir(output_file):
            messagebox.showerror("Error", "Please select a valid output file.")
            return

        if not label:
            messagebox.showerror("Error", "Please enter a label entity.")
            return

        try:
            extractor = Main(input_dir, output_file, label)
            extractor.extract()
            messagebox.showinfo("Success", "Extraction completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
