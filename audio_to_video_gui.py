#!/usr/bin/env python3
"""
Audio to Video Converter GUI - A graphical interface for converting audio files to video files.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
from audio_to_video import AudioToVideoConverter


class AudioToVideoGUI:
    """Graphical user interface for the audio to video converter."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Audio to Video Converter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize converter
        self.converter = AudioToVideoConverter()
        self.audio_files = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Audio to Video Converter", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Audio Files", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # Add files button
        add_button = ttk.Button(file_frame, text="Add Audio Files", command=self.add_audio_files)
        add_button.grid(row=0, column=0, padx=(0, 10))
        
        # Clear files button
        clear_button = ttk.Button(file_frame, text="Clear All", command=self.clear_files)
        clear_button.grid(row=0, column=2)
        
        # File list
        self.file_listbox = tk.Listbox(file_frame, height=6)
        self.file_listbox.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Scrollbar for file list
        file_scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        file_scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        # Conversion options section
        options_frame = ttk.LabelFrame(main_frame, text="Conversion Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Output filename
        ttk.Label(options_frame, text="Output Filename:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.output_filename = tk.StringVar(value="")
        output_entry = ttk.Entry(options_frame, textvariable=self.output_filename, width=30)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Label(options_frame, text="(leave empty for auto-generated names)").grid(row=0, column=2, sticky=tk.W)
        
        # Resolution
        ttk.Label(options_frame, text="Resolution:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.resolution_width = tk.StringVar(value="1920")
        self.resolution_height = tk.StringVar(value="1080")
        width_entry = ttk.Entry(options_frame, textvariable=self.resolution_width, width=8)
        width_entry.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        ttk.Label(options_frame, text="x").grid(row=1, column=1, sticky=tk.W, padx=(70, 0), pady=(10, 0))
        height_entry = ttk.Entry(options_frame, textvariable=self.resolution_height, width=8)
        height_entry.grid(row=1, column=1, sticky=tk.W, padx=(90, 0), pady=(10, 0))
        
        # FPS
        ttk.Label(options_frame, text="FPS:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.fps_var = tk.StringVar(value="30")
        fps_entry = ttk.Entry(options_frame, textvariable=self.fps_var, width=8)
        fps_entry.grid(row=2, column=1, sticky=tk.W, pady=(10, 0))
        
        # Background color
        ttk.Label(options_frame, text="Background Color:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.color_r = tk.StringVar(value="0")
        self.color_g = tk.StringVar(value="0")
        self.color_b = tk.StringVar(value="0")
        
        color_frame = ttk.Frame(options_frame)
        color_frame.grid(row=3, column=1, sticky=tk.W, pady=(10, 0))
        
        ttk.Entry(color_frame, textvariable=self.color_r, width=4).grid(row=0, column=0, padx=(0, 5))
        ttk.Label(color_frame, text="R").grid(row=0, column=1, padx=(0, 10))
        ttk.Entry(color_frame, textvariable=self.color_g, width=4).grid(row=0, column=2, padx=(0, 5))
        ttk.Label(color_frame, text="G").grid(row=0, column=3, padx=(0, 10))
        ttk.Entry(color_frame, textvariable=self.color_b, width=4).grid(row=0, column=4, padx=(0, 5))
        ttk.Label(color_frame, text="B").grid(row=0, column=5)
        
        # Color preview
        self.color_preview = tk.Canvas(color_frame, width=30, height=20, bg='black')
        self.color_preview.grid(row=0, column=6, padx=(10, 0))
        
        # Update color preview when values change
        for var in [self.color_r, self.color_g, self.color_b]:
            var.trace('w', self.update_color_preview)
        
        # Output directory
        ttk.Label(options_frame, text="Output Directory:").grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.output_dir = tk.StringVar(value="output")
        dir_entry = ttk.Entry(options_frame, textvariable=self.output_dir, width=30)
        dir_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        browse_button = ttk.Button(options_frame, text="Browse", command=self.browse_output_dir)
        browse_button.grid(row=4, column=2, pady=(10, 0))
        
        # Convert button
        convert_button = ttk.Button(main_frame, text="Convert to Video", command=self.convert_audio_to_video, style="Accent.TButton")
        convert_button.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # Progress and log section
        log_frame = ttk.LabelFrame(main_frame, text="Progress & Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(log_frame, variable=self.progress_var, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(log_frame, textvariable=self.status_var)
        status_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
    
    def add_audio_files(self):
        """Add audio files to the list."""
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio files", "*.mov *.mp3 *.wav *.aac *.m4a *.flac *.ogg *.wma"),
                ("All files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.audio_files:
                self.audio_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
        
        self.update_status(f"Added {len(files)} audio file(s)")
    
    def clear_files(self):
        """Clear all audio files from the list."""
        self.audio_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_status("Cleared all audio files")
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
    
    def update_color_preview(self, *args):
        """Update the color preview canvas."""
        try:
            r = int(self.color_r.get())
            g = int(self.color_g.get())
            b = int(self.color_b.get())
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.color_preview.configure(bg=color)
        except ValueError:
            pass
    
    def update_status(self, message):
        """Update status message and log."""
        self.status_var.set(message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def convert_audio_to_video(self):
        """Start the audio to video conversion process in a separate thread."""
        if not self.audio_files:
            messagebox.showwarning("Warning", "Please add audio files first!")
            return
        
        # Validate inputs
        try:
            width = int(self.resolution_width.get())
            height = int(self.resolution_height.get())
            fps = int(self.fps_var.get())
            r = int(self.color_r.get())
            g = int(self.color_g.get())
            b = int(self.color_b.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for resolution, FPS, and color values!")
            return
        
        # Disable convert button during processing
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Convert to Video":
                widget.configure(state="disabled")
        
        # Start progress bar
        self.progress_bar.start()
        
        # Start conversion in separate thread
        thread = threading.Thread(target=self._convert_thread, args=(width, height, fps, (r, g, b)))
        thread.daemon = True
        thread.start()
    
    def _convert_thread(self, width, height, fps, color):
        """Thread function for audio to video conversion."""
        try:
            self.update_status("Starting audio to video conversion...")
            
            # Create converter with custom output directory
            converter = AudioToVideoConverter(output_dir=self.output_dir.get())
            
            # Convert files
            if len(self.audio_files) == 1:
                # Single file conversion
                result = converter.convert_audio_to_video(
                    audio_path=self.audio_files[0],
                    output_name=self.output_filename.get() if self.output_filename.get() else None,
                    resolution=(width, height),
                    fps=fps,
                    color=color
                )
                
                # Stop progress bar
                self.progress_bar.stop()
                
                if result:
                    self.update_status(f"✅ Audio to video conversion completed successfully!")
                    self.update_status(f"📁 Output file: {result}")
                    messagebox.showinfo("Success", f"Audio converted to video successfully!\nOutput: {result}")
                else:
                    self.update_status("❌ Audio to video conversion failed!")
                    messagebox.showerror("Error", "Audio to video conversion failed! Check the log for details.")
            else:
                # Batch conversion
                results = converter.batch_convert(
                    audio_paths=self.audio_files,
                    resolution=(width, height),
                    fps=fps,
                    color=color
                )
                
                # Stop progress bar
                self.progress_bar.stop()
                
                if results:
                    self.update_status(f"✅ Successfully converted {len(results)} files:")
                    for result in results:
                        self.update_status(f"  📁 {result}")
                    messagebox.showinfo("Success", f"Successfully converted {len(results)} audio files to video!")
                else:
                    self.update_status("❌ No files were converted successfully!")
                    messagebox.showerror("Error", "Audio to video conversion failed! Check the log for details.")
        
        except Exception as e:
            self.progress_bar.stop()
            self.update_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            # Re-enable convert button
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Button) and widget.cget("text") == "Convert to Video":
                    widget.configure(state="normal")


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = AudioToVideoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main() 