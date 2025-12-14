import customtkinter as ctk
import subprocess
import os
import sys
import webbrowser
from tkinter import filedialog

try:
    import customtkinter
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter", "--quiet"])
    import customtkinter as ctk

ctk.set_appearance_mode("dark")

BG_COLOR         = "#005780"
TEXT_COLOR       = "#FFFFFF"
RENAME_COLOR     = "#397C9C"
DECOMPRESS_COLOR = "#558FAA"
EDITOR_COLOR     = "#71A2B8"
COMPRESS_COLOR   = "#8EB4C7"

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys.executable
    else:
        base_path = __file__
    return os.path.join(os.path.dirname(os.path.abspath(base_path)), relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hogwarts Legacy Save Tools GUI")
        self.geometry("500x680")
        self.configure(fg_color=BG_COLOR)
        self.resizable(False, False)

        ctk.CTkLabel(self,
                     text="HOGWARTS LEGACY\nSAVE TOOLS",
                     font=("Segoe UI", 30, "bold"),
                     text_color=TEXT_COLOR).pack(pady=(50, 40))

        btn_style = {
            "font": ("Segoe UI", 18, "bold"),
            "text_color": TEXT_COLOR,
            "height": 64,
            "corner_radius": 14
        }

        ctk.CTkButton(self, text="RENAME",
                      fg_color=RENAME_COLOR, hover_color="#2e5f7a",
                      **btn_style, command=self.rename_sav
                      ).pack(pady=12, padx=80, fill="x")

        ctk.CTkButton(self, text="DECOMPRESS",
                      fg_color=DECOMPRESS_COLOR, hover_color="#427a8c",
                      **btn_style, command=self.decompress_in_terminal
                      ).pack(pady=12, padx=80, fill="x")

        ctk.CTkButton(self, text="LAUNCH THE EDITOR",
                      fg_color=EDITOR_COLOR, hover_color="#5a8aa0",
                      **btn_style, command=self.launch_editor
                      ).pack(pady=12, padx=80, fill="x")

        ctk.CTkButton(self, text="COMPRESS",
                      fg_color=COMPRESS_COLOR, hover_color="#7698a8",
                      **btn_style, command=self.compress_in_terminal
                      ).pack(pady=12, padx=80, fill="x")

        self.logbox = ctk.CTkTextbox(self, height=140,
                                    font=("Consolas", 11),
                                    text_color="#FFFFFF",
                                    fg_color="#003350")
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
        subprocess.Popen(['powershell', '-NoExit', '-Command', cmd],
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.log(f"Creating {decomp}")

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
        subprocess.Popen(['powershell', '-NoExit', '-Command', cmd],
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.log(f"Creating {sav}")

    def launch_editor(self):
        html = get_resource_path("hlse.html")
        if os.path.isfile(html):
            self.log("Opening editor")
            webbrowser.open(f"file://{os.path.abspath(html)}")
        else:
            self.log("hlse.html not found")

if __name__ == "__main__":
    App().mainloop()
