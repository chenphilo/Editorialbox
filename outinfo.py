import os
import glob
import PyPDF2
from run_info import run_info

import re

# 判断全是英文
def no_chinese(s):
    if re.search('[\u4e00-\u9fa5]', s) is None:
        return True
    else:
        return False


# 获取一行最后的{}中的内容、、弃用
# def getcontent(string):
#     pattern = r"\{([^{}]+)\}(?=[^{}]*$)"
#     match = re.search(pattern, string)
#     if match:
#         content = match.group(1)
#         return content

#获取标题，可能有换行的情况
def extract_title(text):
    flag = 0
    for i, char in enumerate(text):
        if char == '{':
            if i==0:
                continue
            flag = flag + 1
        elif char == '}':
            flag = flag - 1
        if flag == -1:
            return text[1:i].replace('\n', '')
        
    pattern = r'{([^{}]+)}'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


def process_folders(path, output_dir,out_txt):
    try:
        # 获取所有匹配的文件夹
        folders = sorted(x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x)) and x[0].isdigit())
        output = ''
        for folder in folders:
            folder_path = os.path.join(path, folder)
            folder_name = folder.split()[-1]
            if folder_name == "Contents":
                continue
            output += f"{folder_name}\n"
            tex_file = os.path.join(folder_path, folder_name + '.tex')
            if os.path.exists(tex_file):
                with open(tex_file, encoding='utf-8') as f:
                    content = f.read()
                    lines = content.splitlines()
                    vol_num = get_line_num(lines, '输入卷号')
                    if vol_num:
                        output += f"卷号：{vol_num}  "
                    issue_num = get_line_num(lines, '输入当年期号')
                    if issue_num:
                        output += f"期号：{issue_num}  "
                    year_num = get_line_num(lines, '输入出版年份')
                    if year_num:
                        output += f"年份：{year_num}\n"
                    start_page = get_line_num(lines, '输入起始页码')
                    if start_page:
                        output += f"起始页码：{start_page}  "
                    end_page = get_line_num(lines, '输入终止页码')
                    if end_page:
                        output += f"终止页码：{end_page}  "
                    total_pages = get_line_num(lines, '输入页数')
                    if total_pages:
                        output += f"页数：{total_pages}\n"
                    for i, line in enumerate(lines):
                        if '请输入论文题目' in line:
                            tmptext = lines[i+1]+"\n"+lines[i+2]
                            output += f"中文标题: {extract_title(tmptext)}\n"
                        elif 'Insert Chinese title' in line: #英文模板的对应关键词
                            tmptext = lines[i+1]+"\n"+lines[i+2]
                            output += f"中文标题: {extract_title(tmptext)}\n"
                        elif '请输入英文标题' in line:
                            tmptext = lines[i+1]+"\n"+lines[i+2]
                            output += f"英文标题: {extract_title(tmptext)}\n"
                        elif 'Insert the title of your paper.' in line:#英文模板的对应关键词
                            tmptext = lines[i+1]+"\n"+lines[i+2]
                            output += f"英文标题: {extract_title(tmptext)}\n"
                        elif '第一作者姓名' in line:
                            author_name = lines[i+1]
                            if no_chinese(author_name):
                                output += f"第一作者英文: {author_name}\n"
                            else:
                                output += f"第一作者中文: {author_name}\n"
                        elif 'Insert the first author name.' in line:#英文模板的对应关键词
                            author_name = lines[i+1]
                            if no_chinese(author_name):
                                output += f"第一作者英文: {author_name}\n"
                            else:
                                output += f"第一作者中文: {author_name}\n"
                        elif '第二作者姓名' in line and line[0]!='%':
                            author_name = lines[i]
                            if no_chinese(author_name):
                                output += f"第二作者英文: {author_name}\n"
                            else:
                                output += f"第二作者中文: {author_name}\n"
                        elif 'Insert the second author if' in line and line[0]!='%':#英文模板的对应关键词
                            author_name = lines[i]
                            if no_chinese(author_name):
                                output += f"第二作者英文: {author_name}\n"
                            else:
                                output += f"第二作者中文: {author_name}\n"
                        elif '第三作者姓名' in line and line[0]!='%':
                            author_name = lines[i]
                            if no_chinese(author_name):
                                output += f"第三作者英文: {author_name}\n"
                            else:
                                output += f"第三作者中文: {author_name}\n"
                        elif 'Insert the third author if' in line and line[0]!='%':#英文模板的对应关键词  
                            author_name = lines[i]
                            if no_chinese(author_name):
                                output += f"第三作者英文: {author_name}\n"
                            else:
                                output += f"第三作者中文: {author_name}\n"
                        elif 'documentclass' in line:
                            try:
                                zihao = line.split(",")[1]
                                output += f"字号 {zihao}\n"
                            except:
                                continue
            sty_file = glob.glob(f"{folder_path}/*.sty")
            if sty_file:
                with open(sty_file[0], encoding='utf-8') as f:
                    content = f.read()
                    baselinestretch = get_line_num(content.splitlines(), '全文行间距')
                    if baselinestretch:
                        output += f"全文行距: {baselinestretch}\n"
            pdf_file = os.path.join(folder_path, folder_name + '.pdf')
            num_pages = 0
            if os.path.exists(pdf_file):
                with open(pdf_file, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    num_pages = len(pdf.pages)
                    output += f"--------------------------实际pdf页数: {num_pages}\n"
            output += '\n'
        import datetime
        now = datetime.datetime.now()
        with open(os.path.join(output_dir, '信息检查'+str(now.strftime("%Y_%m_%d_%H_%M_%S"))+'.txt'), 'w', encoding='utf-8') as f:
            f.write(output)
    except Exception as e:
        run_info(out_txt, e)
        run_info(out_txt, "请确认目录格式为例如[03 Ming_Xiao]，内部文件为[Ming_Xiao.tex]的格式")

def get_line_num(lines, keyword):
    for line in lines:
        if keyword in line:
            return ''.join(filter(str.isdigit, line))
    return ''

def main(script_path, out_txt):
    try:
        run_info(out_txt, "当前目录为：" + str(script_path)+"\n")
        process_folders(script_path, script_path, out_txt)
        run_info(out_txt, "检查文件生成成功，请查看。\n")   

    except Exception as e:
        run_info(out_txt, e)
        run_info(out_txt, "请确认目录格式为例如[03 Ming_Xiao]，内部文件为[Ming_Xiao.tex]的格式")

    