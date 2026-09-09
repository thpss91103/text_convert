import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from PIL import Image, ImageTk

class TextConvertApp(tk.Tk):

    def __init__(windows):
        super().__init__()
        windows.title("宜特科技轉code程式")
        windows.iconbitmap("icon.ico")
        windows.geometry("1200x720")
        windows.code_file = ""
        #windows.configure(background="white")
        windows.build_ui()

    def build_ui(windows):
        tool_bar = tk.Frame(windows)
        tool_bar.grid(row=0, column=0, sticky="ew")

        logo_image = Image.open("logo.png").resize((80, 40))
        windows.logo_image = ImageTk.PhotoImage(logo_image)
        ttk.Label(tool_bar, image=windows.logo_image).pack(side="left")
        windows.file_entry = ttk.Entry(tool_bar, width=103)
        windows.file_entry.pack(padx=10, pady=20, side="left")
        ttk.Button(tool_bar, text="讀取檔案", command=windows.select_file).pack(pady=20, side="left")
        windows.company = tk.StringVar(value="選取公司")
        windows.company_type = (ttk.Combobox(tool_bar, textvariable=windows.company, values=["瑞鼎", "集創", "敦泰"], state="readonly"))
        windows.company_type.pack(padx=10, pady=20, side="left")
        ttk.Button(tool_bar, text="儲存檔案", command=windows.save_file).pack(pady=20, side="left")

        windows.text_frame = tk.Frame(windows)
        windows.text_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=20)
        windows.text_frame.columnconfigure(0, weight=1, uniform="half")
        windows.text_frame.columnconfigure(1, weight=1, uniform="half")
        windows.text_frame.rowconfigure(1, weight=1)

        left_frame = tk.Frame(windows.text_frame)
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.pack(fill="both", expand=True, side="left", padx=(0, 5))

        ttk.Label(left_frame, text="原始code").grid(row=0, column=0, sticky="w")
        windows.left_text_area = scrolledtext.ScrolledText(left_frame, wrap="word")
        windows.left_text_area.grid(row=1, column=0, sticky="nsew")

        right_frame = tk.Frame(windows.text_frame)
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(1, weight=1)
        right_frame.pack(fill="both", expand=True, side="left", padx=(5, 0))

        ttk.Label(right_frame, text="轉檔code").grid(row=0, column=1, sticky="w")
        windows.right_text_area = scrolledtext.ScrolledText(right_frame, wrap="word")
        windows.right_text_area.grid(row=1, column=1, sticky="nsew")

        #視窗往下拉也會放大
        windows.rowconfigure(1, weight=1)
        windows.columnconfigure(0, weight=1)

        actionbar = tk.Frame(windows)
        actionbar.grid(row=2, column=0, sticky="ew")
        ttk.Button(actionbar, text="開始轉檔", command=windows.convert_file).pack(pady=20)



    def select_file(windows):
        file_path = filedialog.askopenfilename(
            title = "選擇客戶 TXT 檔",
            filetypes = [("文字檔", "*.txt")]
        )
        if file_path:
            windows.file_entry.delete(0, tk.END)
            windows.file_entry.insert(0, file_path)
            windows.code_file = file_path
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            except (OSError, UnicodeDecodeError) as error:
                content = f"無法讀取檔案：{error}"

            windows.left_text_area.delete("1.0", tk.END)
            windows.left_text_area.insert("1.0", content)

    def save_file(windows):
        content = windows.right_text_area.get("1.0", tk.END)
        print(content)
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

    def convert_file(windows):
        with open(windows.code_file, "r", encoding="utf-8") as file:
            code = file.read()
        print(windows.company.get())
        print(code)

# ---- 程式執行入口 ----
if __name__ == "__main__":
    TextConvertApp().mainloop()              # 執行視窗
