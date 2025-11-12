"""
GUI Module
Futuristic terminal-style interface for Jarvis.
"""
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
from typing import Optional, Callable


class JarvisGUI:
    """Futuristic terminal GUI for Jarvis."""
    
    def __init__(
        self,
        width: int = 700,
        height: int = 500,
        bg_color: str = "#000000",
        text_color: str = "#00ff41",
        font_family: str = "Courier",
        font_size: int = 12,
        transparency: float = 0.95
    ):
        """
        Initialize GUI.
        
        Args:
            width: Window width
            height: Window height
            bg_color: Background color
            text_color: Text color
            font_family: Font family
            font_size: Font size
            transparency: Window transparency (0.0 to 1.0)
        """
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_family = font_family
        self.font_size = font_size
        self.transparency = transparency
        
        self.root: Optional[tk.Tk] = None
        self.text_widget: Optional[scrolledtext.ScrolledText] = None
        self.status_label: Optional[tk.Label] = None
        self.is_visible = False
        self.typing_speed = 0.03  # Seconds per character
        self.on_close_callback: Optional[Callable] = None
        
    def show(self) -> None:
        """Show the GUI window."""
        if self.is_visible:
            return
        
        # Create window in main thread
        self.root = tk.Tk()
        self.root.title("JARVIS")
        
        # Window configuration
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg=self.bg_color)
        
        # Remove window decorations (borderless)
        self.root.overrideredirect(True)
        
        # Set transparency
        self.root.attributes("-alpha", self.transparency)
        
        # Always on top
        self.root.attributes("-topmost", True)
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = tk.Label(
            header_frame,
            text="J.A.R.V.I.S.",
            font=(self.font_family, self.font_size + 4, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Just A Rather Very Intelligent System",
            font=(self.font_family, self.font_size - 2),
            fg=self.text_color,
            bg=self.bg_color
        )
        subtitle_label.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_button = tk.Button(
            header_frame,
            text="✕",
            font=(self.font_family, self.font_size),
            fg=self.text_color,
            bg=self.bg_color,
            activebackground="#1a1a1a",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            command=self.hide,
            cursor="hand2"
        )
        close_button.pack(side=tk.RIGHT)
        
        # Separator
        separator = tk.Frame(self.root, bg=self.text_color, height=2)
        separator.pack(fill=tk.X, padx=10)
        
        # Audio waveform visualization
        self.waveform_canvas = tk.Canvas(
            self.root,
            bg=self.bg_color,
            height=100,
            highlightthickness=0
        )
        self.waveform_canvas.pack(fill=tk.X, padx=10, pady=10)
        self.waveform_bars = self._create_waveform()
        self.is_speaking_anim = False
        self.anim_frame = 0
        
        # Status indicator
        self.status_label = tk.Label(
            self.root,
            text="● INITIALIZING",
            font=(self.font_family, self.font_size),
            fg=self.text_color,
            bg=self.bg_color,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Text display area
        self.text_widget = scrolledtext.ScrolledText(
            self.root,
            font=(self.font_family, self.font_size),
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Make draggable
        self._make_draggable()
        
        self.is_visible = True
        print("🖥️  GUI window opened - you can now speak!")
        
        # Start GUI loop
        self.root.mainloop()
    
    def _make_draggable(self) -> None:
        """Make window draggable."""
        self.root.bind("<Button-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._on_drag)
    
    def _start_drag(self, event):
        """Start dragging window."""
        self.root._drag_start_x = event.x
        self.root._drag_start_y = event.y
    
    def _on_drag(self, event):
        """Handle window dragging."""
        x = self.root.winfo_x() + event.x - self.root._drag_start_x
        y = self.root.winfo_y() + event.y - self.root._drag_start_y
        self.root.geometry(f"+{x}+{y}")
    
    def hide(self) -> None:
        """Hide the GUI window."""
        if self.root and self.is_visible:
            self.is_visible = False
            self.root.quit()
            self.root.destroy()
            self.root = None
            
            # Call close callback
            if self.on_close_callback:
                self.on_close_callback()
    
    def set_status(self, status: str, color: Optional[str] = None) -> None:
        """
        Update status indicator.
        
        Args:
            status: Status text (e.g., "LISTENING", "THINKING", "SPEAKING")
            color: Optional color override
        """
        if not self.status_label:
            return
        
        status_colors = {
            "LISTENING": "#00ff41",  # Green
            "THINKING": "#ffaa00",   # Orange
            "SPEAKING": "#00aaff",   # Blue
            "READY": "#00ff41",      # Green
            "ERROR": "#ff0000"       # Red
        }
        
        color = color or status_colors.get(status, self.text_color)
        
        self.status_label.config(text=f"● {status}", fg=color)
        
        # Control face animation based on status
        if status == "SPEAKING":
            self.start_speaking_animation()
        else:
            self.stop_speaking_animation()
        
        self.root.update()
    
    def clear_text(self) -> None:
        """Clear text display."""
        if self.text_widget:
            self.text_widget.delete(1.0, tk.END)
    
    def add_text(self, text: str, prefix: str = "") -> None:
        """
        Add text immediately (no animation).
        
        Args:
            text: Text to add
            prefix: Prefix (e.g., "USER: ", "JARVIS: ")
        """
        if not self.text_widget:
            return
        
        full_text = f"{prefix}{text}\n\n"
        self.text_widget.insert(tk.END, full_text)
        self.text_widget.see(tk.END)
        self.root.update()
    
    def type_text(self, text: str, prefix: str = "") -> None:
        """
        Type text with animation.
        
        Args:
            text: Text to type
            prefix: Prefix (e.g., "JARVIS: ")
        """
        if not self.text_widget:
            return
        
        # Add prefix
        if prefix:
            self.text_widget.insert(tk.END, prefix)
            self.text_widget.see(tk.END)
            self.root.update()
        
        # Type each character
        for char in text:
            if not self.is_visible:
                break
            self.text_widget.insert(tk.END, char)
            self.text_widget.see(tk.END)
            self.root.update()
            time.sleep(self.typing_speed)
        
        # Add newlines
        self.text_widget.insert(tk.END, "\n\n")
        self.text_widget.see(tk.END)
        self.root.update()
    
    def set_close_callback(self, callback: Callable) -> None:
        """Set callback function when window closes."""
        self.on_close_callback = callback
    
    def _create_waveform(self) -> list:
        """Create audio waveform bars."""
        import random
        
        bars = []
        num_bars = 50  # Number of vertical bars
        bar_width = 8
        spacing = 2
        total_width = num_bars * (bar_width + spacing)
        start_x = (700 - total_width) // 2  # Center the waveform
        
        center_y = 50  # Middle of the canvas
        
        for i in range(num_bars):
            x = start_x + i * (bar_width + spacing)
            # Create bars with varying initial heights
            height = random.randint(5, 15)
            
            bar = self.waveform_canvas.create_rectangle(
                x, center_y - height,
                x + bar_width, center_y + height,
                fill=self.text_color,
                outline=''
            )
            bars.append(bar)
        
        return bars
    
    def start_speaking_animation(self) -> None:
        """Start waveform animation for speaking."""
        self.is_speaking_anim = True
        self._animate_waveform()
    
    def stop_speaking_animation(self) -> None:
        """Stop waveform animation."""
        self.is_speaking_anim = False
        # Reset bars to minimal height
        self._reset_waveform()
    
    def _reset_waveform(self) -> None:
        """Reset waveform bars to idle state."""
        if not self.waveform_bars or not self.root:
            return
        
        center_y = 50
        num_bars = len(self.waveform_bars)
        bar_width = 8
        spacing = 2
        total_width = num_bars * (bar_width + spacing)
        start_x = (700 - total_width) // 2
        
        for i, bar in enumerate(self.waveform_bars):
            x = start_x + i * (bar_width + spacing)
            height = 3  # Minimal height when idle
            self.waveform_canvas.coords(
                bar,
                x, center_y - height,
                x + bar_width, center_y + height
            )
    
    def _animate_waveform(self) -> None:
        """Animate audio waveform bars while speaking."""
        if not self.is_speaking_anim or not self.root:
            return
        
        import random
        import math
        
        self.anim_frame = (self.anim_frame + 1) % 60
        
        center_y = 50
        num_bars = len(self.waveform_bars)
        bar_width = 8
        spacing = 2
        total_width = num_bars * (bar_width + spacing)
        start_x = (700 - total_width) // 2
        
        for i, bar in enumerate(self.waveform_bars):
            x = start_x + i * (bar_width + spacing)
            
            # Create wave pattern - higher in the middle, lower on edges
            distance_from_center = abs(i - num_bars // 2)
            base_multiplier = 1.0 - (distance_from_center / (num_bars // 2)) * 0.4
            
            # Add random variation for natural audio effect
            wave = math.sin((self.anim_frame + i * 3) * 0.2) * 0.5 + 0.5
            random_factor = random.uniform(0.7, 1.3)
            
            # Calculate bar height
            height = int((15 + wave * 25) * base_multiplier * random_factor)
            height = max(5, min(height, 45))  # Clamp between 5 and 45
            
            # Update bar position
            self.waveform_canvas.coords(
                bar,
                x, center_y - height,
                x + bar_width, center_y + height
            )
        
        # Continue animation
        if self.is_speaking_anim:
            self.root.after(50, self._animate_waveform)


def run_gui_test():
    """Test the GUI."""
    gui = JarvisGUI()
    
    # Create window
    thread = threading.Thread(target=gui.show, daemon=True)
    thread.start()
    
    time.sleep(1)  # Wait for window to open
    
    # Test different statuses
    gui.set_status("READY")
    time.sleep(1)
    
    gui.set_status("LISTENING")
    gui.add_text("Hey Jarvis, what's the time?", "USER: ")
    time.sleep(2)
    
    gui.set_status("THINKING")
    time.sleep(1)
    
    gui.set_status("SPEAKING")
    gui.type_text("The current time is 3:42 PM, sir.", "JARVIS: ")
    time.sleep(2)
    
    gui.set_status("READY")
    
    # Keep window open
    time.sleep(5)
    gui.hide()


if __name__ == "__main__":
    run_gui_test()

