import importlib.util
import os
import subprocess
import sys
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox

if sys.platform != "win32":
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Platform Error", "This tool only works on Windows.")
    sys.exit(1)


def _ensure_dependencies():
    root = tk.Tk()
    root.withdraw()

    missing_packages = []
    friendly_names = []

    if importlib.util.find_spec("customtkinter") is None:
        missing_packages.append("customtkinter")
        friendly_names.append("CustomTkinter")

    if importlib.util.find_spec("darkdetect") is None:
        missing_packages.append("darkdetect")
        friendly_names.append("DarkDetect")

    if not missing_packages:
        root.destroy()
        return

    plural = len(missing_packages) > 1
    dep_list = ", ".join(friendly_names)
    message = (
        f"This script requires the following package{'s' if plural else ''}:\n\n"
        f"{dep_list}\n\n"
        "Install automatically now? (Requires internet connection)"
    )

    install = messagebox.askyesno(
        "Missing Dependencies" if plural else "Missing Dependency", message
    )

    if not install:
        messagebox.showerror(
            "Dependencies Missing",
            f"Required package{'s' if plural else ''} not installed.\n"
            f"Please run: pip install {' '.join(missing_packages)}",
        )
        root.destroy()
        sys.exit(1)

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--no-cache-dir"]
            + missing_packages,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        messagebox.showerror(
            "Installation Failed",
            f"Failed to install: {', '.join(friendly_names)}\n\n{e}\n\n"
            f"Please install manually:\n"
            f"pip install {' '.join(missing_packages)}",
        )
        root.destroy()
        sys.exit(1)

    messagebox.showinfo(
        "Success",
        f"{'Packages' if plural else 'Package'} installed successfully!\n\nRestarting...",
    )
    root.destroy()
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit(0)


_ensure_dependencies()

import customtkinter as ctk
import darkdetect

ctk.set_appearance_mode("dark")

BG_COLOR = "#005780"
TEXT_COLOR = "#FFFFFF"
SAVED_GAMES_COLOR = "#1C6A8E"
RENAME_COLOR = "#397C9C"
DECOMPRESS_COLOR = "#558FAA"
EDITOR_COLOR = "#71A2B8"
LEGILIMENS_COLOR = "#8EB4C7"
COMPRESS_COLOR = "#AAC7D5"


def get_resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        window_width = 500
        window_height = 768
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.title("GUI Version 2.2 © Henry & Lukas 2025-2026")
        self.configure(fg_color=BG_COLOR)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ctk.CTkLabel(
            self,
            text="HOGWARTS LEGACY SAVE TOOLS",
            font=("Segoe UI", 24, "bold"),
            text_color=TEXT_COLOR,
        ).pack(pady=(30, 30))

        btn_style = {
            "font": ("Segoe UI", 18, "bold"),
            "text_color": TEXT_COLOR,
            "height": 56,
            "corner_radius": 14,
        }

        ctk.CTkButton(
            self,
            text="GO TO SAVED GAMES",
            fg_color=SAVED_GAMES_COLOR,
            hover_color="#165570",
            **btn_style,
            command=self.go_to_saved_games,
        ).pack(pady=10, padx=80, fill="x")

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

    def go_to_saved_games(self):
        saved_games_path = os.path.expandvars(
            r"%LocalAppData%\Hogwarts Legacy\Saved\SaveGames"
        )
        self.log(f"Opening folder: {saved_games_path}")
        if os.path.isdir(saved_games_path):
            try:
                os.startfile(saved_games_path)
            except Exception as e:
                self.log(f"Error opening folder: {e}")
                messagebox.showerror("Error", f"Could not open folder:\n{e}")
        else:
            self.log("Save folder not found!")
            messagebox.showwarning(
                "Folder Not Found",
                "Hogwarts Legacy save folder does not exist.\n"
                "Make sure the game has been launched at least once.",
            )

    def rename_sav(self):
        self.log("Select .sav to rename to .orig")
        path = filedialog.askopenfilename(filetypes=[("Save file", "*.sav")])
        if not path or not path.lower().endswith(".sav"):
            self.log("Cancelled")
            return

        new_path = path[:-4] + ".orig"
        if os.path.exists(new_path):
            if not messagebox.askyesno(
                "Overwrite?", f"{os.path.basename(new_path)} already exists. Overwrite?"
            ):
                self.log("Rename cancelled: file exists")
                return

        try:
            os.rename(path, new_path)
            self.log(f"Renamed to: {os.path.basename(new_path)}")
        except Exception as e:
            self.log(f"Error renaming: {e}")

    def decompress_in_terminal(self):
        self.log("Select .orig file to decompress")
        orig = filedialog.askopenfilename(filetypes=[("Orig save", "*.orig")])
        if not orig or not orig.lower().endswith(".orig"):
            self.log("Cancelled")
            return

        folder = os.path.dirname(orig)
        base = os.path.basename(orig)
        decomp = base[:-5] + ".decomp"

        hlsaves_exe = get_resource_path("hlsaves.exe")
        if not os.path.isfile(hlsaves_exe):
            self.log("ERROR: hlsaves.exe not found in application directory")
            return

        try:
            subprocess.Popen(
                [hlsaves_exe, "-d", base, decomp],
                cwd=folder,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            self.log(f"Decompressing → {decomp}")
        except Exception as e:
            self.log(f"Failed to start decompression: {e}")

    def launch_editor(self):
        html_path = get_resource_path("hlse.html")
        if os.path.isfile(html_path):
            self.log("Opening Hogwarts Legacy Save Game Editor (hlse.html)")
            webbrowser.open(f"file://{os.path.abspath(html_path)}")
        else:
            self.log("ERROR: hlse.html not found in application directory")

    def launch_legilimens(self):
        self.log("Select input file for Legilimens")
        input_file = filedialog.askopenfilename(
            title="Select file for Legilimens", filetypes=[("All files", "*.*")]
        )
        if not input_file:
            self.log("Cancelled")
            return

        folder = os.path.dirname(input_file)
        input_fullpath = os.path.abspath(input_file)
        legilimens_exe = get_resource_path("Legilimens.exe")

        if not os.path.isfile(legilimens_exe):
            self.log("ERROR: Legilimens.exe not found in application directory")
            return

        output_file = "output.txt"
        try:
            subprocess.Popen(
                [legilimens_exe, input_fullpath, "--filters", "ALL", "-o", output_file],
                cwd=folder,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            self.log(f"Running Legilimens → {os.path.join(folder, output_file)}")
        except Exception as e:
            self.log(f"Failed to launch Legilimens: {e}")

    def compress_in_terminal(self):
        self.log("Select .edited file to compress")
        edited = filedialog.askopenfilename(filetypes=[("Edited save", "*.edited")])
        if not edited:
            self.log("Cancelled")
            return

        folder = os.path.dirname(edited)
        base = os.path.basename(edited)
        sav = base.replace(".edited", ".sav")

        hlsaves_exe = get_resource_path("hlsaves.exe")
        if not os.path.isfile(hlsaves_exe):
            self.log("ERROR: hlsaves.exe not found in application directory")
            return

        try:
            subprocess.Popen(
                [hlsaves_exe, "-c", base, sav],
                cwd=folder,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            self.log(f"Compressing → {sav}")
        except Exception as e:
            self.log(f"Failed to start compression: {e}")

    def on_closing(self):
        self.quit()
        self.destroy()
        sys.exit()


if __name__ == "__main__":
    App().mainloop()
