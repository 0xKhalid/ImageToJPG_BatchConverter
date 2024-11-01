"""
@file       ImageToJPG_BatchConverter.py
@author     Khalid Mansoor AlAwadhi <khalid@remal.io>
@date       Initial Release - Fri Nov 1 2024
@brief      A simple Python GUI tool that allows users to select a directory containing images in various formats (including HEIC) 
            and convert them to high-quality JPG format. The tool scans the directory, shows the count of compatible image files, 
            and prompts the user to confirm before converting and saving the images to a specified output directory.
"""
import os
import threading
from tkinter import Tk, Label, Button, Toplevel, filedialog, messagebox
from PIL import Image
import pillow_heif  # Import pillow_heif to handle HEIC files

# Register HEIC format with Pillow
pillow_heif.register_heif_opener()

class ImageConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to JPG Converter")

        # Set window size and center it on the screen
        window_width, window_height = 400, 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = int((screen_width - window_width) / 2)
        position_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
        # Initialize file counters
        self.image_files = []
        
        # Labels and buttons
        self.label = Label(root, text="Select a directory to scan for images")
        self.label.pack(pady=10)
        
        self.scan_button = Button(root, text="Select Directory and Scan", command=self.scan_directory)
        self.scan_button.pack(pady=5)
        
        self.convert_button = Button(root, text="Convert to JPG", state="disabled", command=self.start_conversion_thread)
        self.convert_button.pack(pady=5)
        
        self.output_directory = None
        self.loading_screen = None
        self.loading_label = None

    def scan_directory(self):
        # Directory selection
        selected_directory = filedialog.askdirectory(title="Select a Directory to Scan")
        
        if not selected_directory:
            return  # User canceled directory selection
        
        # Scan for image files
        self.image_files = [os.path.join(selected_directory, f) for f in os.listdir(selected_directory)
                            if f.lower().endswith(('.png', '.bmp', '.tiff', '.webp', '.gif', '.heic'))]
        
        # Display result
        count = len(self.image_files)
        message = f"Found {count} image file(s) in the selected directory."
        messagebox.showinfo("Scan Results", message)
        
        if count > 0:
            # Enable the conversion button if there are files to convert
            self.convert_button.config(state="normal")
        else:
            self.convert_button.config(state="disabled")

    def start_conversion_thread(self):
        # Start the conversion in a separate thread to keep the GUI responsive
        conversion_thread = threading.Thread(target=self.convert_images)
        conversion_thread.start()

    def convert_images(self):
        # Prompt for output directory
        self.output_directory = filedialog.askdirectory(title="Select Output Directory")
        
        if not self.output_directory:
            return  # User canceled output directory selection
        
        # Confirmation before conversion
        confirm = messagebox.askyesno("Confirm Conversion", f"{len(self.image_files)} files will be converted to JPG.\nProceed?")
        
        if not confirm:
            return

        # Create loading screen
        self.loading_screen = Toplevel(self.root)
        self.loading_screen.title("Converting Images")
        self.loading_screen.geometry("300x100")

        # Center the loading screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        loading_screen_x = int((screen_width - 300) / 2)
        loading_screen_y = int((screen_height - 100) / 2)
        self.loading_screen.geometry(f"300x100+{loading_screen_x}+{loading_screen_y}")
        
        self.loading_label = Label(self.loading_screen, text="Starting conversion...", font=("Helvetica", 12))
        self.loading_label.pack(pady=20)
        
        # Convert each image file in a background thread
        total_files = len(self.image_files)
        for index, image_path in enumerate(self.image_files, start=1):
            with Image.open(image_path) as img:
                # Convert to JPG, set quality to the best
                img = img.convert("RGB")  # Convert to RGB if not already in this mode
                output_path = os.path.join(self.output_directory, f"{os.path.splitext(os.path.basename(image_path))[0]}.jpg")
                img.save(output_path, "JPEG", quality=95)  # High quality JPG
            
            # Update loading label with progress
            self.update_loading_screen(index, total_files)

        # Notify completion and close loading screen
        self.loading_screen.destroy()
        messagebox.showinfo("Conversion Complete", f"{total_files} files have been converted and saved to the selected directory.")
        self.convert_button.config(state="disabled")  # Disable the button after conversion

    def update_loading_screen(self, current, total):
        # Update the loading screen text with current progress
        self.loading_label.config(text=f"Converting {current} of {total}")
        self.loading_screen.update_idletasks()  # Update the screen immediately

# Set up and run the GUI
root = Tk()
app = ImageConverterGUI(root)
root.mainloop()
