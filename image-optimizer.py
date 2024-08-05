import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, StringVar, Radiobutton, Checkbutton, BooleanVar, IntVar, DISABLED, NORMAL, ttk
from PIL import Image

def resize_image(input_path, output_path, max_size):
    """Resize the image to fit within max_size while maintaining aspect ratio, and save it."""
    with Image.open(input_path) as img:
        img.thumbnail(max_size, Image.LANCZOS)
        img.save(output_path, quality=85, optimize=True)

def resize_images_in_folder(input_folder, output_folder, max_size, replace=False, delete_input=False, rename=False, rename_text=""):
    """Resize all images in the input folder and save them to the output folder."""
    if not os.path.exists(input_folder):
        messagebox.showerror("Input Error", f"Input folder '{input_folder}' does not exist.")
        return
    if not replace and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    total_files = len(files)

    progress_bar['value'] = 0
    progress_bar['maximum'] = total_files
    progress_label['text'] = f"Processing 0 of {total_files} images..."

    for idx, filename in enumerate(files):
        input_path = os.path.join(input_folder, filename)
        output_path = input_path if replace else os.path.join(output_folder, filename)

        if rename:
            base, ext = os.path.splitext(output_path)
            output_path = base + rename_text + ext

        resize_image(input_path, output_path, max_size)

        if delete_input and not replace:
            os.remove(input_path)

        progress_bar['value'] = idx + 1
        progress_label['text'] = f"Processing {idx + 1} of {total_files} images..."
        root.update_idletasks()

    messagebox.showinfo("Success", "Images resized successfully!")

def select_input_folder():
    """Open a dialog to select the input folder."""
    folder = filedialog.askdirectory()
    if folder:
        input_folder_entry.delete(0, 'end')
        input_folder_entry.insert(0, folder)

def select_output_folder():
    """Open a dialog to select the output folder."""
    folder = filedialog.askdirectory()
    if folder:
        output_folder_entry.delete(0, 'end')
        output_folder_entry.insert(0, folder)

def get_auto_size():
    """Return an optimal maximum size for web images."""
    return (1200, 1200)  # Example max size for web optimization

def start_resizing():
    """Get folder paths and start resizing images."""
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    auto_size = auto_size_var.get()

    if auto_size == 'auto':
        max_size = get_auto_size()
    else:
        try:
            width = int(width_entry.get()) if width_entry.get() else None
            height = int(height_entry.get()) if height_entry.get() else None
            if width and height:
                max_size = (width, height)
            elif width:
                max_size = (width, int(width * 1.5))  # Example ratio
            elif height:
                max_size = (int(height * 1.5), height)  # Example ratio
            else:
                messagebox.showerror("Input Error", "Width and height must be integers.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Width and height must be integers.")
            return

    replace = replace_delete_var.get() == 'replace'
    delete_input = replace_delete_var.get() == 'delete'
    rename = rename_var.get()
    rename_text = rename_entry.get() if rename else ""

    resize_images_in_folder(input_folder, output_folder, max_size, replace, delete_input, rename, rename_text)

def on_replace_delete_change():
    """Enable or disable the output folder selection based on the replace option."""
    if replace_delete_var.get() == 'replace':
        output_folder_entry.config(state=DISABLED)
        output_folder_button.config(state=DISABLED)
    else:
        output_folder_entry.config(state=NORMAL)
        output_folder_button.config(state=NORMAL)

def on_rename_change():
    """Show or hide the rename entry based on the rename option."""
    if rename_var.get():
        rename_label.grid()
        rename_entry.grid()
    else:
        rename_label.grid_remove()
        rename_entry.grid_remove()

# Create the main window
root = Tk()
root.title("Image Resizer")

# Set window size
root.geometry("800x600")

# Create and place GUI elements
Label(root, text="Input Folder:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
input_folder_entry = Entry(root, width=50)
input_folder_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_input_folder).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
output_folder_entry = Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=10)
output_folder_button = Button(root, text="Browse", command=select_output_folder)
output_folder_button.grid(row=1, column=2, padx=10, pady=10)

Label(root, text="Resize Option:").grid(row=2, column=0, padx=10, pady=10, sticky='e')

auto_size_var = StringVar(value='manual')
Radiobutton(root, text="Auto", variable=auto_size_var, value='auto').grid(row=2, column=1, padx=10, pady=10, sticky='w')
Radiobutton(root, text="Manual", variable=auto_size_var, value='manual').grid(row=2, column=1, padx=10, pady=10, sticky='e')

Label(root, text="Width:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
width_entry = Entry(root, width=10)
width_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

Label(root, text="Height:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
height_entry = Entry(root, width=10)
height_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')

replace_delete_var = StringVar(value='none')
Label(root, text="Output Options:").grid(row=5, column=0, padx=10, pady=10, sticky='e')
Radiobutton(root, text="Replace", variable=replace_delete_var, value='replace', command=on_replace_delete_change).grid(row=5, column=1, padx=10, pady=10, sticky='w')
Radiobutton(root, text="Delete Input", variable=replace_delete_var, value='delete', command=on_replace_delete_change).grid(row=6, column=1, padx=10, pady=10, sticky='w')

rename_var = BooleanVar()
Checkbutton(root, text="Rename Output", variable=rename_var, command=on_rename_change).grid(row=7, column=1, padx=10, pady=10, sticky='w')

rename_label = Label(root, text="Rename Suffix:")
rename_label.grid(row=8, column=0, padx=10, pady=10, sticky='e')
rename_entry = Entry(root, width=10)
rename_entry.grid(row=8, column=1, padx=10, pady=10, sticky='w')

rename_label.grid_remove()
rename_entry.grid_remove()

Button(root, text="Start Resizing", command=start_resizing).grid(row=9, column=0, columnspan=3, pady=20)

progress_label = Label(root, text="")
progress_label.grid(row=10, column=0, columnspan=3)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=11, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
