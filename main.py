import tkinter as tk
import os
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.scrolledtext as st
from run_info import run_info
import merge
import outinfo
import compileall
import singlecheck

# 定义一个主窗口类，继承自tk.Tk
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # 设置窗口位置，大小
        windowwidth = 400
        windowheight = 500
        self.geometry(f"{windowwidth}x{windowheight}+500+200")
        # 设置窗口标题
        self.title("编辑部工具箱")
        # 创建标签框架
        self.tab_control = ttk.Notebook(self)
        # 创建四个标签页对象
        self.tab1 = MergeTab(self.tab_control, "合并文件", self.run_tab1)
        self.tab2 = InfoTab(self.tab_control, "检查tex信息", self.run_tab2)
        self.tab3 = CompTab(self.tab_control, "编译全部", self.run_tab3)
        self.tab4 = SingleTab(self.tab_control, "检查单字成行", self.run_tab4)
        # 添加标签页到标签框架
        self.tab_control.add(self.tab1, text=self.tab1.name)
        self.tab_control.add(self.tab2, text=self.tab2.name)
        self.tab_control.add(self.tab3, text=self.tab3.name)
        self.tab_control.add(self.tab4, text=self.tab4.name)
        # 显示标签框架
        self.tab_control.pack(expand=1, fill="both")

        # 创建一个输出文本框，放在窗口底部
        self.output_text = st.ScrolledText(self, height=25)
        self.output_text.pack(side="bottom", fill="x")
        run_info(self.output_text, "欢迎使用编辑部工具箱!\n运行日志:\n")



    # 定义四个函数，用于运行每个标签页对应的功能
    def run_tab1(self):
        # 在这里书写合并文件的函数
        run_info(self.output_text,"运行合并文件的函数\n")
        file_path = self.tab1.entry.get()
        merge.merge_pdfs(file_path, self.output_text)

    def run_tab2(self):
        # 在这里书写分割文件的函数
        run_info(self.output_text,"运行检查文件的函数\n")
        file_path = self.tab2.entry.get()
        outinfo.main(file_path, self.output_text)


    def run_tab3(self):
        # 在这里书写转换文件的函数
        run_info(self.output_text,"运行全编译的函数\n")
        file_path = self.tab3.entry.get()
        compileall.compile_pdfs(file_path, self.output_text)


    def run_tab4(self):
        # 在这里书写压缩文件的函数
        run_info(self.output_text,"运行检查单字成行的函数\n")
        file_path = self.tab4.entry.get()
        singlecheck.main(file_path,self.output_text)

        

# 定义一个标签页类，继承自ttk.Frame
class TabPage(ttk.Frame):
    def __init__(self, parent, name, run_function):
        super().__init__(parent)
        # 设置标签页的名字和对应的运行函数
        self.name = name
        self.run_function = run_function
        # 在标签页上显示标签的名字
        self.label = ttk.Label(self, text=f"输入路径或浏览选择路径")
        self.label.grid(column=0, row=0, padx=10, pady=10, sticky="w")
        # 在标签页上创建一个文本框，用于输入或显示文件路径
        self.entry = tk.Entry(self, text=f"{self.name}", exportselection=False)
        self.entry.grid(column=0, row=1, sticky="nsew")
        # 将第二列的权重设置为1，使其自适应
        self.columnconfigure(1, weight=1)

        # 在标签页上创建一个按钮，用于浏览文件并获取文件路径
        self.button = tk.Button(self, text="浏览", command=self.browse_file)
        self.button.grid(column=0, row=2, sticky="nsew")

        # 在标签页上创建一个按钮，用于运行对应的功能
        self.run_button = tk.Button(self, text="运行", command=self.run_function)
        self.run_button.grid(column=0, row=3, sticky="nsew")

    # 定义一个函数，用于浏览文件并获取文件路径
    def browse_file(self):
        path = fd.askdirectory() # 更改为askdirectory()方法
        self.entry.delete(0, tk.END) # 删除当前文本框中的内容
        self.entry.insert(0, path) # 插入文件路径或目录路径

# 合并tab类
class MergeTab(TabPage):
    def __init__(self, parent, name, run_function):
        super().__init__(parent, name, run_function)
        # 在标签页上创建一个额外的说明标签，用于显示更多的使用说明
        instruction_text = "使用说明：输入路径为一期的目录，例如：\n E:\Github\Studies_in_Logic\\2023年第2期(69)，点击运行则可合并所有pdf"
        self.additional_instruction = ttk.Label(self, text=str(instruction_text), wraplength=400-20)
        self.additional_instruction.grid(column=0, row=5, padx=10, pady=10)
        
# 输出信息tab类
class InfoTab(TabPage):
    def __init__(self, parent, name, run_function):
        super().__init__(parent, name, run_function)
        # 在标签页上创建一个额外的说明标签，用于显示更多的使用说明
        instruction_text = "使用说明：输入路径为一期的目录，例如：\n E:\Github\Studies_in_Logic\\2023年第2期(69)，点击运行则可在该目录生成检查文档"
        self.additional_instruction = ttk.Label(self, text=str(instruction_text), wraplength=400-20)
        self.additional_instruction.grid(column=0, row=5, padx=10, pady=10)

# 全部编译tab类
class CompTab(TabPage):
    def __init__(self, parent, name, run_function):
        super().__init__(parent, name, run_function)
        # 在标签页上创建一个额外的说明标签，用于显示更多的使用说明
        instruction_text = "使用说明：输入路径为一期的目录，例如：\n E:\Github\Studies_in_Logic\\2023年第2期(69)，点击运行则可编译所有子文件中tex"
        self.additional_instruction = ttk.Label(self, text=str(instruction_text), wraplength=400-20)
        self.additional_instruction.grid(column=0, row=5, padx=10, pady=10)

# 单字成行tab类
class SingleTab(TabPage):
    def __init__(self, parent, name, run_function):
        super().__init__(parent, name, run_function)
        # 在标签页上创建一个额外的说明标签，用于显示更多的使用说明
        instruction_text = "使用说明：请输入pdf完整路径，例如：E:\Github\Studies_in_Logic\\2023年第2期(69)\文件.pdf"
        self.additional_instruction = ttk.Label(self, text=str(instruction_text), wraplength=400-20)
        self.additional_instruction.grid(column=0, row=5, padx=10, pady=10)


# 创建主窗口对象并运行主循环
if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()

