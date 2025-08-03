#!/usr/bin/env python3
"""
Video Merger GUI - A graphical interface for merging videos.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
from video_merger import VideoMerger


class VideoMergerGUI:
    """Graphical user interface for the video merger."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Video Merger")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize video merger
        self.merger = VideoMerger()
        self.video_files = []
        
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
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Video Merger", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Video Files", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # Add files button
        add_button = ttk.Button(file_frame, text="Add Videos", command=self.add_videos)
        add_button.grid(row=0, column=0, padx=(0, 10))
        
        # Clear files button
        clear_button = ttk.Button(file_frame, text="Clear All", command=self.clear_videos)
        clear_button.grid(row=0, column=2)
        
        # File list
        self.file_listbox = tk.Listbox(file_frame, height=6)
        self.file_listbox.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Scrollbar for file list
        file_scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        file_scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Merge Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Output filename
        ttk.Label(options_frame, text="Output Filename:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.output_filename = tk.StringVar(value="merged_video.mp4")
        output_entry = ttk.Entry(options_frame, textvariable=self.output_filename, width=30)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Method selection
        ttk.Label(options_frame, text="Merge Method:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.method_var = tk.StringVar(value="concatenate")
        method_combo = ttk.Combobox(options_frame, textvariable=self.method_var, 
                                   values=["concatenate", "overlay"], state="readonly", width=15)
        method_combo.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        # Method description
        method_desc = ttk.Label(options_frame, text="concatenate: Join videos sequentially | overlay: Picture-in-picture style")
        method_desc.grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Output directory
        ttk.Label(options_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.output_dir = tk.StringVar(value="output")
        dir_entry = ttk.Entry(options_frame, textvariable=self.output_dir, width=30)
        dir_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        browse_button = ttk.Button(options_frame, text="Browse", command=self.browse_output_dir)
        browse_button.grid(row=2, column=2, pady=(10, 0))
        
        # Merge button
        merge_button = ttk.Button(main_frame, text="Merge Videos", command=self.merge_videos, style="Accent.TButton")
        merge_button.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # Progress and log section
        log_frame = ttk.LabelFrame(main_frame, text="Progress & Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(log_frame, variable=self.progress_var, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(log_frame, textvariable=self.status_var)
        status_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
    
    def add_videos(self):
        """Add video files to the list."""
        files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
                ("All files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.video_files:
                self.video_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
        
        self.update_status(f"Added {len(files)} video file(s)")
    
    def clear_videos(self):
        """Clear all video files from the list."""
        self.video_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_status("Cleared all video files")
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
    
    def update_status(self, message):
        """Update status message and log."""
        self.status_var.set(message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def merge_videos(self):
        """Start the video merging process in a separate thread."""
        if not self.video_files:
            messagebox.showwarning("Warning", "Please add video files first!")
            return
        
        # Disable merge button during processing
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Merge Videos":
                widget.configure(state="disabled")
        
        # Start progress bar
        self.progress_bar.start()
        
        # Start merging in separate thread
        thread = threading.Thread(target=self._merge_videos_thread)
        thread.daemon = True
        thread.start()
    
    def _merge_videos_thread(self):
        """Thread function for merging videos."""
        try:
            self.update_status("Starting video merge process...")
            
            # Create merger with custom output directory
            merger = VideoMerger(output_dir=self.output_dir.get())
            
            # Merge videos
            result = merger.merge_videos(
                self.video_files,
                self.output_filename.get(),
                self.method_var.get()
            )
            
            # Stop progress bar
            self.progress_bar.stop()
            
            if result:
                self.update_status(f"✅ Video merging completed successfully!")
                self.update_status(f"📁 Output file: {result}")
                messagebox.showinfo("Success", f"Videos merged successfully!\nOutput: {result}")
            else:
                self.update_status("❌ Video merging failed!")
                messagebox.showerror("Error", "Video merging failed! Check the log for details.")
        
        except Exception as e:
            self.progress_bar.stop()
            self.update_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            # Re-enable merge button
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Button) and widget.cget("text") == "Merge Videos":
                    widget.configure(state="normal")


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = VideoMergerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main() 