import importlib.util
import os
import subprocess
import sys
import webbrowser

import tkinter as tk
from tkinter import filedialog, messagebox


def _install_customtkinter():
    root = tk.Tk()
    root.withdraw()

    if importlib.util.find_spec("customtkinter") is not None:
        return True

    install = messagebox.askyesno(
        "Missing Dependency",
        "This script requires customtkinter.\n\n"
        "Install it now? (Requires internet connection)",
    )

    if not install:
        messagebox.showerror(
            "Dependency Missing", "customtkinter is required to run this script."
        )
        root.destroy()
        sys.exit(1)

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--no-cache-dir", "customtkinter"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        messagebox.showinfo(
            "Success", "customtkinter installed successfully!\n\nRestarting script..."
        )
        root.destroy()
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit(0)

    except Exception as e:
        messagebox.showerror(
            "Installation Failed",
            "Failed to install customtkinter:\n\n"
            + str(e)
            + "\n\n"
            + "Please install manually in terminal:\n"
            + "pip install customtkinter",
        )
        root.destroy()
        sys.exit(1)


_install_customtkinter()
import customtkinter as ctk

ctk.set_appearance_mode("dark")

BG_COLOR = "#005780"
TEXT_COLOR = "#FFFFFF"
RENAME_COLOR = "#397C9C"
DECOMPRESS_COLOR = "#558FAA"
EDITOR_COLOR = "#71A2B8"
LEGILIMENS_COLOR = "#8EB4C7"
COMPRESS_COLOR = "#AAC7D5"


def get_resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys.executable
    else:
        base_path = __file__
    return os.path.join(os.path.dirname(os.path.abspath(base_path)), relative_path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hogwarts Legacy Save Tools GUI 2.1")
        self.geometry("500x768")
        self.configure(fg_color=BG_COLOR)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ctk.CTkLabel(
            self,
            text="HOGWARTS LEGACY SAVE TOOLS",
            font=("Segoe UI", 24, "bold"),
            text_color=TEXT_COLOR,
        ).pack(pady=(50, 30))

        ctk.CTkLabel(
            self,
            text="© Henry & Lukas 2025-2026",
            font=("Segoe UI", 12),
            text_color="#A8A8A8",
        ).pack(pady=(0, 20))

        btn_style = {
            "font": ("Segoe UI", 18, "bold"),
            "text_color": TEXT_COLOR,
            "height": 56,
            "corner_radius": 14,
        }

        ctk.CTkButton(
            self,
            text="RENAME",
            fg_color=RENAME_COLOR,
            hover_color="#2E637D",
            **btn_style,
            command=self.rename_sav,
        ).pack(pady=10, padx=80, fill="x")

        ctk.CTkButton(
            self,
            text="DECOMPRESS",
            fg_color=DECOMPRESS_COLOR,
            hover_color="#44728C",
            **btn_style,
            command=self.decompress_in_terminal,
        ).pack(pady=10, padx=80, fill="x")

        ctk.CTkButton(
            self,
            text="LAUNCH THE EDITOR",
            fg_color=EDITOR_COLOR,
            hover_color="#5B8294",
            **btn_style,
            command=self.launch_editor,
        ).pack(pady=10, padx=80, fill="x")

        ctk.CTkButton(
            self,
            text="LAUNCH LEGILIMENS",
            fg_color=LEGILIMENS_COLOR,
            hover_color="#7190A0",
            **btn_style,
            command=self.launch_legilimens,
        ).pack(pady=10, padx=80, fill="x")

        ctk.CTkButton(
            self,
            text="COMPRESS",
            fg_color=COMPRESS_COLOR,
            hover_color="#889FA8",
            **btn_style,
            command=self.compress_in_terminal,
        ).pack(pady=10, padx=80, fill="x")

        self.logbox = ctk.CTkTextbox(
            self,
            height=160,
            font=("Consolas", 11),
            text_color="#FFFFFF",
            fg_color="#003350",
        )
        self.logbox.pack(pady=25, padx=60, fill="both", expand=True)
        self.log("Ready")

    def log(self, msg):
        self.logbox.insert("end", msg + "\n")
        self.logbox.see("end")

    def rename_sav(self):
        self.log("Select .sav to rename to .orig")
        path = filedialog.askopenfilename(filetypes=[("Save file", "*.sav")])
        if not path or not path.lower().endswith(".sav"):
            self.log("Cancelled")
            return
        new = path[:-4] + ".orig"
        try:
            os.rename(path, new)
            self.log(f"Renamed to {os.path.basename(new)}")
        except Exception as e:
            self.log(f"Error: {e}")

    def decompress_in_terminal(self):
        self.log("Select .orig file")
        orig = filedialog.askopenfilename(filetypes=[("Orig save", "*.orig")])
        if not orig or not orig.lower().endswith(".orig"):
            self.log("Cancelled")
            return
        folder = os.path.dirname(orig)
        base = os.path.basename(orig)
        decomp = base[:-5] + ".decomp"
        cmd = f'cd "{folder}"; .\\hlsaves.exe -d "{base}" "{decomp}"; pause'
        subprocess.Popen(
            ["powershell", "-NoExit", "-Command", cmd],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
        self.log(f"Creating {decomp}")

    def launch_editor(self):
        html = get_resource_path("hlse.html")
        if os.path.isfile(html):
            self.log("Opening editor")
            webbrowser.open(f"file://{os.path.abspath(html)}")
        else:
            self.log("hlse.html not found")

    def launch_legilimens(self):
        self.log("Select input file for Legilimens")
        input_file = filedialog.askopenfilename(
            title="Select file for Legilimens", filetypes=[("All files", "*.*")]
        )
        if not input_file:
            self.log("Cancelled")
            return

        input_fullpath = os.path.abspath(input_file)
        legilimens_exe = get_resource_path("Legilimens.exe")

        if not os.path.isfile(legilimens_exe):
            self.log("Legilimens.exe not found")
            return

        cmd = f"{legilimens_exe} {input_fullpath} --filters ALL -o output.txt; pause"

        subprocess.Popen(
            ["powershell", "-NoExit", "-Command", cmd],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
        self.log(f"Running Legilimens on {os.path.basename(input_file)} → output.txt")

    def compress_in_terminal(self):
        self.log("Select .edited file")
        edited = filedialog.askopenfilename(filetypes=[("Edited save", "*.edited")])
        if not edited:
            self.log("Cancelled")
            return
        folder = os.path.dirname(edited)
        base = os.path.basename(edited)
        sav = base.replace(".edited", ".sav")
        cmd = f'cd "{folder}"; .\\hlsaves.exe -c "{base}" "{sav}"; pause'
        subprocess.Popen(
            ["powershell", "-NoExit", "-Command", cmd],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
        self.log(f"Creating {sav}")

    def on_closing(self):
        self.destroy()
        self.quit()
        sys.exit()


if __name__ == "__main__":
    App().mainloop()
