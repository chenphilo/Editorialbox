import os
import glob
import PyPDF2
from run_info import run_info

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
                            title = lines[i+1]
                            output += f"论文题目: {title}\n"
                        elif '请输入英文标题' in line:
                            eng_title = lines[i+1]
                            output += f"英文标题: {eng_title}\n"
                        elif '请输入第一作者姓名' in line:
                            author_name = lines[i+1]
                            output += f"作者姓名: {author_name}\n"
                        elif 'documentclass' in line:
                            zihao = line.split(",")[1]
                            output += f"字号 {zihao}\n"
            sty_file = glob.glob(f"{folder_path}/*.sty")
            if os.path.exists(sty_file[0]):
                with open(sty_file[0], encoding='utf-8') as f:
                    content = f.read()
                    baselinestretch = get_line_num(content.splitlines(), '全文行间距')
                    if baselinestretch:
                        output += f"全文行距: {baselinestretch}\n"
            pdf_file = os.path.join(folder_path, folder_name + '.pdf')
            num_pages = 0
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
        run_info(out_txt, "请确认目录格式，文件名为03 Ming_Xiao，内部文件为Ming_Xiao.tex\n")

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
        run_info(out_txt, "请确认目录格式为03 Ming_Xiao，内部文件为Ming_Xiao.tex的格式")
