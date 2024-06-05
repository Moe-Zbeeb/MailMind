import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from main import Main
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Powered By MailMind")
        self.root.geometry("800x600")  # Changed to a larger initial size
        self.create_widgets()

    def create_widgets(self):
        # Create a Canvas with a white background
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Load the image using Pillow
        image_path = "/home/moe/Desktop/asfahani_group_holding_logo.jpeg"  # Replace with your image path
        self.logo_image = Image.open(image_path)
        self.logo_image = self.logo_image.resize((200, 200), Image.LANCZOS)  # Resize image if needed
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Display the image using place to center it
        self.logo_label = tk.Label(self.root, image=self.logo_photo, bg="white")
        self.logo_label.place(relx=0.5, rely=0.15, anchor="center")

        # Input Directory
        self.input_label = tk.Label(self.root, text="Input Directory", bg="white")
        self.input_entry = tk.Entry(self.root, width=30)
        self.input_button = tk.Button(self.root, text="Browse", command=self.browse_input)

        self.input_label.place(relx=0.33, rely=0.4, anchor="e")
        self.input_entry.place(relx=0.5, rely=0.4, anchor="c")
        self.input_button.place(relx=0.68, rely=0.4, anchor="w")

        # Output File
        self.output_label = tk.Label(self.root, text="Output CSV File", bg="white")
        self.output_entry = tk.Entry(self.root, width=30)
        self.output_button = tk.Button(self.root, text="Browse", command=self.browse_output)

        self.output_label.place(relx=0.33, rely=0.5, anchor="e")
        self.output_entry.place(relx=0.5, rely=0.5, anchor="c")
        self.output_button.place(relx=0.68, rely=0.5, anchor="w")

        # Label Entity
        self.label_label = tk.Label(self.root, text="Label Entity", bg="white")
        self.label_entry = tk.Entry(self.root, width=30)

        self.label_label.place(relx=0.33, rely=0.6, anchor="e")
        self.label_entry.place(relx=0.5, rely=0.6, anchor="c")

        # Run Button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_extractor)
        self.run_button.place(relx=0.5, rely=0.7, anchor="c")

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
