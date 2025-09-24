import tkinter as tk
from tkinter import ttk
import requests
from html import unescape  # MyMemory có thể trả về HTML entities (&quot; ...)

MIRRORS = [
    "https://translate.argosopentech.com/translate",
    "https://libretranslate.de/translate",
]

class TextTranslatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Text Translator")
        self.create_widgets()

    def create_widgets(self):
        label1 = tk.Label(self.root, text="Enter text to translate:")
        self.entry = tk.Entry(self.root, width=50)

        label2 = tk.Label(self.root, text="Choose source language:")
        self.source_lang = ttk.Combobox(self.root, values=["en", "es", "fr", "vi", "ja", "zh"], width=8)
        self.source_lang.set("en")

        label3 = tk.Label(self.root, text="Choose target language:")
        self.target_lang = ttk.Combobox(self.root, values=["en", "es", "fr", "vi", "ja", "zh"], width=8)
        self.target_lang.set("vi")

        translate_button = tk.Button(self.root, text="Translate", command=self.translate_text)

        self.result_label = tk.Label(self.root, text="Translated text will appear here.",
                                     wraplength=520, justify="left")

        label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.source_lang.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        label3.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.target_lang.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        translate_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    def translate_text(self):
        text_to_translate = self.entry.get().strip()
        if not text_to_translate:
            self.result_label.config(text="Please enter text.")
            return

        src = self.source_lang.get()
        tgt = self.target_lang.get()

        # 1) Thử MyMemory (miễn phí, không cần key)
        try:
            mm_url = "https://api.mymemory.translated.net/get"
            params = {"q": text_to_translate, "langpair": f"{src}|{tgt}"}
            r = requests.get(mm_url, params=params, timeout=15)
            r.raise_for_status()
            js = r.json()
            translated = js["responseData"]["translatedText"]
            # Giải mã HTML entities (ví dụ &quot;)
            translated = unescape(translated)
            self.result_label.config(text=translated)
            return
        except Exception as e:
            # Nếu MyMemory lỗi, thử LibreTranslate mirrors
            last_err = e

        # 2) Fallback LibreTranslate (có thể bị chặn mạng)
        for url in MIRRORS:
            try:
                payload = {"q": text_to_translate, "source": src, "target": tgt, "format": "text"}
                headers = {"accept": "application/json",
                           "Content-Type": "application/x-www-form-urlencoded"}
                resp = requests.post(url, data=payload, headers=headers, timeout=15)
                resp.raise_for_status()
                js = resp.json()
                if "translatedText" in js:
                    self.result_label.config(text=js["translatedText"])
                    return
            except Exception as e:
                last_err = e
                continue

        self.result_label.config(text=f"All free endpoints failed. Detail: {last_err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextTranslatorApp(root)
    root.mainloop()
