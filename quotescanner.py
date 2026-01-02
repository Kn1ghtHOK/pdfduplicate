import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import PyPDF2
import difflib
import os

class DuplicateFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate Finder")
        self.root.geometry("820x780")
        self.root.configure(bg="#ffffff")

        self.paragraphs = []
        self.file_path = ""

        # --- MODERN STYLING ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Green.Horizontal.TProgressbar", troughcolor='#f0f0f0', background='#34c759', thickness=12)
        self.style.configure("TFrame", background="#ffffff")
        self.style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#1d1d1f")

        main_frame = ttk.Frame(root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_label = ttk.Label(main_frame, text="Duplicate Finder", style="Header.TLabel")
        header_label.pack(pady=(0, 25))

        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=5)

        self.btn_open = ttk.Button(file_frame, text="Select PDF", command=self.open_pdf)
        self.btn_open.pack(side=tk.LEFT, padx=(0, 15))

        self.lbl_status = ttk.Label(file_frame, text="No file selected", foreground="#86868b")
        self.lbl_status.pack(side=tk.LEFT)

        settings_frame = ttk.LabelFrame(main_frame, text=" Settings ", padding="20")
        settings_frame.pack(fill=tk.X, pady=20)

        ttk.Label(settings_frame, text="Similarity Threshold (Typo Sensitivity):").pack(anchor="w")
        self.similarity_slider = tk.Scale(
            settings_frame, from_=0.5, to=1.0, resolution=0.01, 
            orient=tk.HORIZONTAL, bg="#ffffff", bd=0, 
            highlightthickness=0, length=500, activebackground="#34c759",
            troughcolor="#e5e5e7"
        )
        self.similarity_slider.set(0.85)
        self.similarity_slider.pack(fill=tk.X, pady=10)

        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, mode='determinate', style="Green.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=(10, 25))

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        # Button text updated as requested
        self.btn_scan = tk.Button(
            btn_frame, text="Scan for Duplicates", command=self.run_scan, 
            state=tk.DISABLED, bg="#e5e5e7", fg="#a1a1a1", 
            relief="flat", font=("Segoe UI", 10, "bold"), 
            width=22, pady=8, cursor="hand2"
        )
        self.btn_scan.pack(side=tk.LEFT, padx=(0, 15))

        self.btn_reset = ttk.Button(btn_frame, text="Reset", command=self.reset_app)
        self.btn_reset.pack(side=tk.LEFT, padx=(0, 15))

        self.btn_export = ttk.Button(btn_frame, text="Export to .txt", command=self.export_results)
        self.btn_export.pack(side=tk.LEFT)

        ttk.Label(main_frame, text="Results Output", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 5))
        self.text_area = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, font=("Consolas", 11), 
            bg="#fbfbfd", relief="flat", borderwidth=1, highlightthickness=1,
            highlightbackground="#d2d2d7"
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.file_path = file_path
            filename = os.path.basename(file_path)
            self.lbl_status.config(text=f"Selected: {filename}", foreground="#0071e3")
            try:
                raw_text = ""
                with open(self.file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text: raw_text += text + "\n"
                
                # Split by double newline to identify full paragraphs/quotes
                blocks = raw_text.split('\n\n')
                
                # UPDATED: Filter for minimum 3 words
                self.paragraphs = [p.replace('\n', ' ').strip() for p in blocks if len(p.split()) >= 3]
                
                self.btn_scan.config(state=tk.NORMAL, bg="#34c759", fg="white")
                self.insert_log(f"Ready. {len(self.paragraphs)} valid text blocks detected.\n")
            except Exception as e:
                self.insert_log(f"Error: {e}\n")

    def reset_app(self):
        self.paragraphs = []
        self.file_path = ""
        self.lbl_status.config(text="No file selected", foreground="#86868b")
        self.text_area.delete('1.0', tk.END)
        self.progress['value'] = 0
        self.btn_scan.config(state=tk.DISABLED, bg="#e5e5e7", fg="#a1a1a1")
        self.insert_log("Reset complete.\n")

    def export_results(self):
        results = self.text_area.get("1.0", tk.END).strip()
        if not results: return
        file_to_save = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="duplicates.txt")
        if file_to_save:
            with open(file_to_save, 'w', encoding='utf-8') as f:
                f.write(results)
            self.insert_log(f"Saved to {os.path.basename(file_to_save)}\n")

    def run_scan(self):
        if not self.paragraphs: return
        threshold = self.similarity_slider.get()
        self.text_area.delete('1.0', tk.END)
        self.insert_log(f"Scanning for duplicates (Min 3 words)...\n" + "—"*30 + "\n")

        exacts, potentials, seen_indices = [], [], set()
        total = len(self.paragraphs)

        for i in range(total):
            self.progress['value'] = (i / total) * 100
            if i % 5 == 0: self.root.update_idletasks()

            if i in seen_indices: continue
            for j in range(i + 1, total):
                if j in seen_indices: continue
                
                ratio = difflib.SequenceMatcher(None, self.paragraphs[i], self.paragraphs[j]).ratio()
                
                if ratio == 1.0:
                    exacts.append(self.paragraphs[i])
                    seen_indices.add(j)
                elif ratio >= threshold:
                    potentials.append((self.paragraphs[i], self.paragraphs[j], ratio))

        self.progress['value'] = 100
        if exacts:
            self.insert_log("\n[EXACT DUPLICATES]\n")
            for q in set(exacts): self.insert_log(f"• {q}\n")
        if potentials:
            self.insert_log("\n[POTENTIAL NEAR-MATCHES]\n")
            for q1, q2, score in potentials:
                self.insert_log(f"({int(score*100)}% Match)\n  A: {q1}\n  B: {q2}\n\n")
        if not exacts and not potentials: self.insert_log("\nNo duplicates found!")

    def insert_log(self, message):
        self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFinder(root)
    root.mainloop()