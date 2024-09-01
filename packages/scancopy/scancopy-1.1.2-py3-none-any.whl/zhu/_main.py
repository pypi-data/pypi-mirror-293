import os
import json
import shutil
from tkinter import Tk, Label, Text, Entry, Button, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
def start():
        
    CONFIG_FILE = "config.json"

    def save_config(keywords, extensions, source_path, destination_path):
        config_data = {
            "keywords": keywords,
            "extensions": extensions,
            "source_path": source_path,
            "destination_path": destination_path
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)

    def load_config():
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def browse_directory(entry):
        directory = filedialog.askdirectory()
        entry.delete(0, 'end')
        entry.insert(0, directory)
        save_config(keywords_entry.get("1.0", "end-1c"), extensions_entry.get(), source_path_entry.get(), entry.get())

    def scan_and_copy_files():
        keywords_text = keywords_entry.get("1.0", "end-1c")
        keywords = [line.strip() for line in keywords_text.split('\n') if line.strip()]
        
        extensions_text = extensions_entry.get().strip()
        extensions = [ext.strip().lstrip('.') for ext in extensions_text.split(',')]

        source_dir = source_path_entry.get()
        dest_dir = destination_path_entry.get()

        # Ensure the destination directory exists
        os.makedirs(dest_dir, exist_ok=True)

        copied_files = 0
        failed_file_kws = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                _, ext = os.path.splitext(file)
                
                if any(keyword in file for keyword in keywords) and ext.lstrip('.').lower() in extensions:
                    src_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(dest_dir, file)
                    # 复制文件 ,先判断文件是否存在
                    if os.path.exists(dest_file_path):
                        continue   
                    shutil.copy2(src_file_path, dest_file_path)
                    copied_files += 1
                else:
                    print(f"Skipping file: {file}")
                    failed_file_kws.append(file)
        if len(failed_file_kws) > 0:
            # 输入到failed_file_kws_entry
            failed_file_kws_entry.delete("1.0", "end")
            failed_file_kws_entry.insert("end", "\n".join(failed_file_kws))

        messagebox.showinfo("完成", f"已复制 {copied_files} 个,未复制{str(len(failed_file_kws))}个" )
    
    # 加载配置文件
    config = load_config()

    # 创建主窗口
    root = Tk()
    root.title("文件扫描与复制工具")

    # 关键词输入框
    Label(root, text="关键词").grid(row=0, column=0)
    keywords_entry = ScrolledText(root, height=10)  # 多行文本输入框
    keywords_entry.grid(row=0, column=1)
    keywords_entry.insert('end', config.get('keywords', ''))

    # 失败关键词
    Label(root, text="失败关键词").grid(row=1, column=0)
    failed_file_kws_entry = ScrolledText(root, height=10)
    failed_file_kws_entry.grid(row=1, column=1)
    failed_file_kws_entry.insert('end', config.get('failed_file_kws', ''))


    # 文件后缀输入框
    Label(root, text="文件后缀 (逗号分隔)").grid(row=2, column=0)
    extensions_entry = Entry(root, width=50)
    extensions_entry.grid(row=2, column=1)
    extensions_entry.insert(0, config.get('extensions', ''))

    # 扫描路径输入框
    Label(root, text="扫描路径").grid(row=3, column=0)
    source_path_entry = Entry(root, width=50)
    source_path_entry.grid(row=3, column=1)
    source_path_entry.insert(0, config.get('source_path', ''))
    Button(root, text="浏览", command=lambda: browse_directory(source_path_entry)).grid(row=2, column=2)

    # 保存路径输入框
    Label(root, text="保存路径").grid(row=4, column=0)
    destination_path_entry = Entry(root, width=50)
    destination_path_entry.grid(row=4, column=1)
    destination_path_entry.insert(0, config.get('destination_path', ''))
    Button(root, text="浏览", command=lambda: browse_directory(destination_path_entry)).grid(row=3, column=2)


    # 输入框内容变化时保存配置
    def on_keywords_change(event):
        save_config(keywords_entry.get("1.0", "end-1c"), extensions_entry.get(), source_path_entry.get(), destination_path_entry.get())

    keywords_entry.bind("<KeyRelease>", on_keywords_change)

    def on_extensions_change(event):
        save_config(keywords_entry.get("1.0", "end-1c"), extensions_entry.get(), source_path_entry.get(), destination_path_entry.get())

    extensions_entry.bind("<KeyRelease>", on_extensions_change)

    def on_source_path_change(event):
        save_config(keywords_entry.get("1.0", "end-1c"), extensions_entry.get(), source_path_entry.get(), destination_path_entry.get())

    source_path_entry.bind("<KeyRelease>", on_source_path_change)

    def on_destination_path_change(event):
        save_config(keywords_entry.get("1.0", "end-1c"), extensions_entry.get(), source_path_entry.get(), destination_path_entry.get())

    destination_path_entry.bind("<KeyRelease>", on_destination_path_change)

    # 开始按钮
    Button(root, text="开始扫描并复制文件", command=scan_and_copy_files).grid(row=5, column=1)

    root.mainloop()
 

start()