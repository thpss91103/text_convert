import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
from PIL import Image, ImageTk

class TextConvertApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("宜特科技轉code程式 v1.1")
        self.iconbitmap("icon.ico")
        self.geometry("1200x720")
        self.code_file = ""
        self.build_ui()

    def build_ui(self):
        tool_bar = tk.Frame(self)
        tool_bar.grid(row=0, column=0, sticky="ew")

        logo_image = Image.open("logo.png").resize((80, 40))
        self.logo_image = ImageTk.PhotoImage(logo_image)
        ttk.Label(tool_bar, image=self.logo_image).pack(side="left")
        self.file_entry = ttk.Entry(tool_bar, width=103)
        self.file_entry.pack(padx=10, pady=20, side="left")
        ttk.Button(tool_bar, text="讀取檔案", command=self.select_file).pack(pady=20, side="left")
        self.company = tk.StringVar(value="選取公司")
        self.company_type = (ttk.Combobox(tool_bar, textvariable=self.company, values=["瑞鼎", "集創", "敦泰"], state="readonly"))
        self.company_type.pack(padx=10, pady=20, side="left")
        ttk.Button(tool_bar, text="開始轉檔", command=self.convert_file).pack(pady=20, side="left")

        self.text_frame = tk.Frame(self)
        self.text_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=20)
        self.text_frame.columnconfigure(0, weight=1, uniform="half")
        self.text_frame.columnconfigure(1, weight=1, uniform="half")
        self.text_frame.rowconfigure(1, weight=1)

        left_frame = tk.Frame(self.text_frame)
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.pack(fill="both", expand=True, side="left", padx=(0, 5))

        ttk.Label(left_frame, text="原始code").grid(row=0, column=0, sticky="w")
        self.left_text_area = scrolledtext.ScrolledText(left_frame, wrap="word")
        self.left_text_area.grid(row=1, column=0, sticky="nsew")

        right_frame = tk.Frame(self.text_frame)
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(1, weight=1)
        right_frame.pack(fill="both", expand=True, side="left", padx=(5, 0))

        ttk.Label(right_frame, text="轉檔code").grid(row=0, column=1, sticky="w")
        self.right_text_area = scrolledtext.ScrolledText(right_frame, wrap="word")
        self.right_text_area.grid(row=1, column=1, sticky="nsew")

        #視窗往下拉也會放大
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        save_bar = tk.Frame(self)
        save_bar.grid(row=2, column=0, sticky="ew")
        save_bar.columnconfigure(0, weight=1)
        save_bar.columnconfigure(2, weight=1)
        ttk.Button(save_bar, text="儲存檔案", command=self.save_file).grid(row=0, column=1, pady=20)
        ttk.Label(save_bar, text="Copyright©2026 DominYang All rights reserved.", font=("Microsoft JhengHei", 7), foreground="gray").place(relx=1.0, rely=0.5, anchor="e", x=-10)


    def select_file(self):
        file_path = filedialog.askopenfilename(
            title = "選擇客戶 TXT 檔",
            filetypes = [("文字檔", "*.txt")]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.code_file = file_path
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            except (OSError, UnicodeDecodeError) as error:
                content = f"無法讀取檔案：{error}"

            self.left_text_area.delete("1.0", tk.END)
            self.left_text_area.insert("1.0", content)

    def save_file(self):
        content = self.right_text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(
            title="儲存 TXT 檔",
            defaultextension=".txt",
            filetypes=[("文字檔", "*.txt")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
        except OSError as error:
            print(f"無法儲存檔案：{error}")

    def after_comment_noconvert(self, company_code, replacement):
        result_lines = []

        for line in company_code.splitlines():
            for keyword, new_text in replacement.items():
                before_hash, hash_mark, after_hash = line.partition("#")

                # 只取代 # 前面的內容
                before_hash = before_hash.replace(keyword, new_text)

                # # 後面的內容保持原樣
                line = before_hash + hash_mark + after_hash

            result_lines.append(line)

        return "\n".join(result_lines)

    def raydiumn_code(self, lines):
        raydiumn_code = ""
        found_line = 0

        for index, line in enumerate(lines, 1):
            if "delay" in line:
                found_line = index

        for index, line in enumerate(lines):
            if "SSD WRITE" in line:
                raydiumn_code = "\n".join(lines[index:found_line])
                break

        replacement = {
            "SSD WRITE": "#SSD WRITE",
            "/": " #",
            "-": " 0x",
            "]=": " 0x",
            "]-": " 0x",
            "]": "",
            "[": "mipi.write 0x39 0x",
            "MIPI_PORT_BOTH": "",
            "IC WRITE": "#IC WRITE",
            "IC Write": "#IC Write",
            "ic write": "#ic write",
            "delay": "delay 100",
            "Delay": "delay 100",
            "200": "",
            "IC RESET": "",
            "120,2,2": "",
        }

        return self.after_comment_noconvert(raydiumn_code, replacement)

    def focaltech_code(self, lines):
        found_line = 0
        focaltech_code = ""
        for index, line in enumerate(lines, 1):
            if "Video Mode Enable" in line:
                found_line = index
                break
        for index, line in enumerate(lines):
            if "LCD initial code Start" in line:
                focaltech_code = "\n".join(lines[index:found_line-1])
                break

        replacement = {
            "/": " #",
            ");": "",
            ",": " ",
            "GEN_WR(": "mipi.write 0x39 ",
            ")": "",
            "delayms_pc(": "delay ",
        }

        return self.after_comment_noconvert(focaltech_code, replacement)

    def chipone_file(self, lines):
        found_line = 0
        chipone_code = ""

        for index, line in enumerate(lines, 1):
            if "Enter Video Mode" in line:
                found_line = index
                break
        for index, line in enumerate(lines):
            if "initial code start" in line:
                chipone_code = "\n".join(lines[index+2:found_line-1])
                break

        replacement = {
            "delay ": "delay",
            " ": " 0x",
            "/": " #",
            "R": "mipi.write 0x39 0x",
            "delay": "delay ",
        }

        return self.after_comment_noconvert(chipone_code, replacement)

    def convert_file(self):
        if not self.code_file:
            messagebox.showwarning("提示", "請載入code！")
            return

        with open(self.code_file, "r", encoding="utf-8") as file:
            code = file.read()

        with open("mipi_setting.TXT", "r", encoding="utf-8") as file1, \
             open("mipi_setting2.TXT", "r", encoding="utf-8") as file2:
            file1_content = file1.read()
            file2_content = file2.read()

        lines = code.splitlines()
        convert_code = ""
        if self.company.get() == "瑞鼎":
            convert_code = self.raydiumn_code(lines)
            final_code = f"{file1_content}\n{convert_code}\n"
        elif self.company.get() == "敦泰":
            convert_code = self.focaltech_code(lines)
            final_code = f"{file1_content}\n{convert_code}\n{file2_content}"
        elif self.company_type.get() == "集創":
            convert_code = self.chipone_file(lines)
            final_code = f"{file1_content}\n{convert_code}\n{file2_content}"
        else:
            messagebox.showwarning("提示", "請選取公司！")
            return
        if not convert_code:
            messagebox.showwarning("提示", "選擇錯公司")
            return




        self.right_text_area.delete("1.0", tk.END)
        self.right_text_area.insert("1.0", final_code)


# ---- 程式執行入口 ----
if __name__ == "__main__":
    TextConvertApp().mainloop()              # 執行視窗
