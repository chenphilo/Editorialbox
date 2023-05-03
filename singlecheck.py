import PyPDF2
import os
from run_info import run_info

def check_single_char_lines(pdf_path):
    # 获取 PDF 文件名和所在路径
    pdf_name = os.path.basename(pdf_path)
    pdf_dir = os.path.dirname(pdf_path)

    # 创建保存结果的文件
    result_file = open(os.path.join(pdf_dir, "check单字成行.txt"), 'w',encoding="utf-8")

    # 打开 PDF 文件
    pdf_file = open(pdf_path, 'rb')

    # 创建 PyPDF2 的 PdfFileReader 对象
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # 遍历每一页
    for page_num in range(len(pdf_reader.pages)):
        # 获取当前页
        page = pdf_reader.pages[page_num]

        # 提取当前页中的所有文本
        text = page.extract_text()

        # 将文本按行分割成列表
        lines = text.split('\n')

        prev_line = ""
        # 遍历每一行并匹配单字成行的情况
        for line in lines:
            # 使用正则表达式匹配汉字数量
            # chinese_count = len(re.findall('[\u4e00-\u9fa5]', line))

            # 如果该行只有一个汉字，则写入到结果文件中
            if len(line) <3:
                result_file.write(f"{pdf_name}，第{page_num+1}页：\n{prev_line}\n{line}\n\n")
            prev_line = line

    # 关闭结果文件和 PDF 文件
    result_file.close()
    pdf_file.close()


def main(windows_path,output_text):
    python_path = os.path.normpath(windows_path)

    try:
        check_single_char_lines(python_path)
        run_info(output_text, "生成txt完成\n")

    except Exception as e:
        run_info(output_text,e)
        run_info(output_text,"程序错误\n")
