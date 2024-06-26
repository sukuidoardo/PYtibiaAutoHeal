import time
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageGrab
import pyautogui
from threading import Thread
from pynput import mouse

class PixelMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Monitor")
        self.pixel_config = []
        self.monitoring = False
        self.selecting_pixel = False

        self.create_ui()

    def create_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=20)

        self.add_pixel_button = tk.Button(self.main_frame, text="Add Pixel", command=self.add_pixel_entry)
        self.add_pixel_button.grid(row=0, column=0, pady=10)

        self.start_monitoring_button = tk.Button(self.main_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_monitoring_button.grid(row=0, column=1, pady=10)

        self.stop_monitoring_button = tk.Button(self.main_frame, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_monitoring_button.grid(row=0, column=2, pady=10)

        self.pixel_entries_frame = tk.Frame(self.main_frame)
        self.pixel_entries_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.root.bind("<Return>", self.complete_pixel_selection)

    def add_pixel_entry(self):
        row = len(self.pixel_config)

        coord_label = tk.Label(self.pixel_entries_frame, text=f"Pixel {row + 1} (x, y):")
        coord_label.grid(row=row, column=0)

        x_entry = tk.Entry(self.pixel_entries_frame, width=5)
        x_entry.grid(row=row, column=1)

        y_entry = tk.Entry(self.pixel_entries_frame, width=5)
        y_entry.grid(row=row, column=2)

        select_button = tk.Button(self.pixel_entries_frame, text="Select", command=lambda: self.prompt_pixel_selection(x_entry, y_entry))
        select_button.grid(row=row, column=3)

        key_label = tk.Label(self.pixel_entries_frame, text="Key:")
        key_label.grid(row=row, column=4)

        key_entry = ttk.Combobox(self.pixel_entries_frame, values=[chr(i) for i in range(97, 123)] + [f"f{i}" for i in range(1, 13)])
        key_entry.grid(row=row, column=5)

        priority_label = tk.Label(self.pixel_entries_frame, text="Priority:")
        priority_label.grid(row=row, column=6)

        priority_entry = tk.Entry(self.pixel_entries_frame, width=5)
        priority_entry.grid(row=row, column=7)

        always_check_var = tk.IntVar()
        always_check_check = tk.Checkbutton(self.pixel_entries_frame, text="Always Check", variable=always_check_var)
        always_check_check.grid(row=row, column=8)

        pause_button = tk.Button(self.pixel_entries_frame, text="Pause", command=lambda: self.pause_pixel(row))
        pause_button.grid(row=row, column=9)

        remove_button = tk.Button(self.pixel_entries_frame, text="Remove", command=lambda: self.remove_pixel(row))
        remove_button.grid(row=row, column=10)

        self.pixel_config.append({
            "row": row,
            "x_entry": x_entry,
            "y_entry": y_entry,
            "key_entry": key_entry,
            "priority_entry": priority_entry,
            "always_check_var": always_check_var,
            "paused": False,
            "pause_button": pause_button,
            "original_color": None
        })

    def prompt_pixel_selection(self, x_entry, y_entry):
        if not self.selecting_pixel:
            self.selecting_pixel = True
            messagebox.showinfo("Instructions", "Move the mouse to the pixel you want to select and press Enter.")
            self.status_label = tk.Label(self.root, text="Move the mouse to the pixel you want to select and press Enter.")
            self.status_label.pack(pady=20)
            self.x_entry = x_entry
            self.y_entry = y_entry

    def complete_pixel_selection(self, event=None):
        if self.selecting_pixel:
            x, y = pyautogui.position()
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
            self.x_entry.insert(0, str(x))
            self.y_entry.insert(0, str(y))
            self.set_original_color(len(self.pixel_config) - 1, (x, y))
            self.selecting_pixel = False
            self.status_label.config(text=f"Pixel selected at ({x}, {y})")

    def set_original_color(self, index, location):
        self.pixel_config[index]["original_color"] = self.get_color_at(location)

    def start_monitoring(self):
        self.pixel_data = []
        for config in self.pixel_config:
            x = int(config["x_entry"].get())
            y = int(config["y_entry"].get())
            key = config["key_entry"].get()
            priority = int(config["priority_entry"].get())
            always_check = bool(config["always_check_var"].get())
            original_color = config["original_color"]
            self.pixel_data.append({"x": x, "y": y, "key": key, "priority": priority, "always_check": always_check, "original_color": original_color, "paused": config["paused"]})

        self.monitoring = True
        self.monitoring_thread = Thread(target=self.monitor_pixels)
        self.monitoring_thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        if hasattr(self, 'monitoring_thread'):
            self.monitoring_thread.join()

    def monitor_pixels(self):
        while self.monitoring:
            highest_priority = float('inf')
            key_to_press = None

            for data in self.pixel_data:
                if data["paused"]:
                    continue

                current_color = self.get_color_at((data["x"], data["y"]))
                if self.is_color_change(current_color, data["original_color"]):
                    if data["always_check"]:
                        pyautogui.press(data["key"])
                    elif data["priority"] < highest_priority:
                        highest_priority = data["priority"]
                        key_to_press = data["key"]

            if key_to_press:
                pyautogui.press(key_to_press)

            time.sleep(0.5)

    def get_color_at(self, location):
        screenshot = ImageGrab.grab()
        return screenshot.getpixel(location)

    def is_color_change(self, current_color, original_color):
        return current_color != original_color

    def pause_pixel(self, row):
        for config in self.pixel_config:
            if config["row"] == row:
                config["paused"] = not config["paused"]
                if config["paused"]:
                    config["pause_button"].config(text="Resume")
                else:
                    config["pause_button"].config(text="Pause")

    def remove_pixel(self, row):
        for config in self.pixel_config:
            if config["row"] == row:
                for widget in self.pixel_entries_frame.grid_slaves(row=row):
                    widget.grid_forget()
                self.pixel_config.remove(config)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelMonitorApp(root)
    root.mainloop()
