import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

class VirusScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alpha Shield - Antivirus Tool")
        self.root.geometry("650x550")
        
        # Scanner Settings
        self.target_exts = ['.exe', '.dll', '.bat', '.cmd', '.vbs', '.js', '.py']
        self.malware_hashes = ["5e884898da28047151d0e56f8dc62927"] # Example Signatures
        self.infected_files = []

        # Sabse pehle Agreement dikhao
        self.show_agreement()

    def show_agreement(self):
        self.agreement_win = tk.Toplevel(self.root)
        self.agreement_win.title("Terms & Conditions")
        self.agreement_win.geometry("500x400")
        self.agreement_win.grab_set() # User ko main window pe jane se rokta hai

        tk.Label(self.agreement_win, text="End User License Agreement", font=("Arial", 12, "bold")).pack(pady=10)

        # Agreement Text
        agreement_text = """
Dhyan se padhein:

1. Yeh application sirf scanning aur education purpose ke liye hai.
2. Agar is application ko use karte waqt aapka computer, PC ya koi 
   bhi data/app harmful (nuksan) hota hai, toh isme hamari koi 
   bhi galti ya zimmedari nahi hogi.
3. User apni marzi se files delete karne ki permission deta hai.
4. Admin access zaroori hai poore system ki scanning ke liye.

Kya aap in sharton se sehmat hain?
        """
        
        text_area = scrolledtext.ScrolledText(self.agreement_win, width=55, height=12)
        text_area.insert(tk.INSERT, agreement_text)
        text_area.config(state='disabled')
        text_area.pack(pady=10)

        btn_frame = tk.Frame(self.agreement_win)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agree & Start", bg="green", fg="white", 
                  command=self.accept_agreement, width=15).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Decline", bg="red", fg="white", 
                  command=self.root.quit, width=15).pack(side=tk.LEFT, padx=10)

    def accept_agreement(self):
        self.agreement_win.destroy()
        self.setup_main_ui()

    def setup_main_ui(self):
        # UI Elements
        tk.Label(self.root, text="Alpha Shield - Real Time Scanner", font=("Arial", 16, "bold"), fg="#2c3e50").pack(pady=15)
        
        self.status_var = tk.StringVar(value="Status: Ready for Scanning")
        tk.Label(self.root, textvariable=self.status_var, font=("Arial", 10)).pack()

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progress.pack(pady=10)

        self.log_area = scrolledtext.ScrolledText(self.root, width=75, height=15, bg="#f4f4f4")
        self.log_area.pack(pady=10, padx=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.btn_scan = tk.Button(btn_frame, text="Select Folder & Scan", bg="#3498db", fg="white", 
                                  command=self.start_scan_process, width=20, height=2)
        self.btn_scan.pack(side=tk.LEFT, padx=5)

        self.btn_clean = tk.Button(btn_frame, text="Clean Threats", bg="#e74c3c", fg="white", 
                                   command=self.clean_detected, width=20, height=2, state="disabled")
        self.btn_clean.pack(side=tk.LEFT, padx=5)

    def log(self, msg):
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def start_scan_process(self):
        path = filedialog.askdirectory()
        if not path: return

        self.infected_files = []
        self.btn_scan.config(state="disabled")
        self.log(f"[INFO] Scan shuru ho raha hai: {path}")
        
        # Real-time scanning logic
        all_files = []
        for r, d, f in os.walk(path):
            for file in f:
                if any(file.lower().endswith(ext) for ext in self.target_exts):
                    all_files.append(os.path.join(r, file))

        self.progress['maximum'] = len(all_files) if all_files else 1
        
        for i, file_path in enumerate(all_files):
            self.progress['value'] = i + 1
            self.status_var.set(f"Scanning: {os.path.basename(file_path)}")
            
            if self.is_virus(file_path):
                self.log(f"[!!!] VIRUS DETECTED: {file_path}")
                self.infected_files.append(file_path)
            self.root.update_idletasks()

        self.finish_scan()

    def is_virus(self, file_path):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                file_hash = hashlib.md5(content).hexdigest()
                return file_hash in self.malware_hashes
        except: return False

    def finish_scan(self):
        self.btn_scan.config(state="normal")
        self.status_var.set("Status: Scan Complete")
        if self.infected_files:
            self.btn_clean.config(state="normal")
            messagebox.showwarning("Threats Found", f"{len(self.infected_files)} khatarnak files mili hain!")
        else:
            messagebox.showinfo("System Safe", "Koi virus nahi mila.")

    def clean_detected(self):
        if messagebox.askyesno("Confirm Delete", "Kya aap in virus files ko delete karna chahte hain?"):
            for f in self.infected_files:
                try:
                    os.remove(f)
                    self.log(f"[CLEANED] Deleted: {f}")
                except Exception as e:
                    self.log(f"[ERROR] Could not delete {f}: {e}")
            self.btn_clean.config(state="disabled")
            messagebox.showinfo("Done", "System ab saaf hai.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirusScannerApp(root)
    root.mainloop()