import datetime
import os
from run_info import run_info


# 中文文章的目录构建

def clean_name(name):#删除名字中的非中文内容
    return ''.join(filter(lambda x: '\u4e00' <= x <= '\u9fff', name))

def twoname(name):#两个名字加一个空隙
    name = clean_name(name)
    if len(name)==2:
        return name[0]+"\\hspace{1em}"+name[1]
    else:
        return name


def process_info(info,flag):#处理每组信息，并非遍历整个txt，只遍历给到的部分
    page = ''
    engname1, engname2, engname3 = '', '', ''
    zhname1, zhname2, zhname3 = '', '', ''
    zhtitle = ''
    entitle = ''
    for line in info:
        if '起始页码：' in line:
            page = int(line.split()[0][5:].strip())
        elif '第一作者英文:' in line:
            engname1 = line[7:].strip()
        elif '第一作者中文:' in line:
            zhname1 = twoname(line[7:].strip())
        elif '第二作者英文:' in line:
            engname2 = line[7:].strip()
        elif '第二作者中文:' in line:
            zhname2 = twoname(line[7:].strip())
        elif '第三作者英文:' in line:
            engname3 = line[7:].strip()
        elif '第三作者中文:' in line:
            zhname3 = twoname(line[7:].strip())
            
        elif '中文标题:' in line:
            zhtitle = line.split('中文标题:')[-1].strip()
        elif '英文标题' in line:
            entitle = line.split('英文标题:')[-1].strip()

    # 多作者判断
    if zhname2 and zhname3:
        authors = '&\\textit{{\\large {}，{}，{}}}'.format(zhname1, zhname2, zhname3)
        en_authors = '\\textit{{{}, {}, {}}}'.format(engname1, engname2, engname3)
    elif zhname2:
        authors = '&\\textit{{\\large {}，{}}}'.format(zhname1, zhname2)
        en_authors = '\\textit{{{}, {}}}'.format(engname1, engname2)
    else:
        authors = '&\\textit{{\\large {}}}'.format(zhname1)
        en_authors = '\\textit{{{}}}'.format(engname1)

    zhtitle = zhtitle.replace("\\\\","").replace("\\Large","").replace("\\large","").replace("{","").replace("}","").strip()
    entitle = entitle.replace("\\\\","").replace("\\Large","").replace("\\large","").strip()#英文不去{}，因为有斜体

    if flag =="ch":
        if '——' in zhtitle:
            zhtitle1, zhtitle2 = zhtitle.split('——')
            zhtitle1 = zhtitle1.strip()
            zhtitle2 = '~~~~——' + zhtitle2.strip()
            return f'{{\\large {zhtitle1}}}\n{authors}\n& {page}\\\\\n{{\\large {zhtitle2}}}\n\n\\vdistance\n\n'

        else:
            return f'{{\\large {zhtitle}}}\n{authors}\n& {page}\\\\\n\n\\vdistance\n\n'
    elif flag =="en":
        if '---' in entitle:
            entitle1, entitle2 = entitle.split('---')
            entitle1 = entitle1.strip()
            entitle2 = '---' + entitle2.strip()
            return f'\\large {entitle1}\\\\\n\\large ~~~~---{entitle2}\\\\\n{en_authors}\n& {page}\\\\\n\n\n\\vdistance\n\n'

        else:
            return f'\\large {entitle}\\\\\n{en_authors}\n& {page}\\\\\n\n\\vdistance\n\n'


def process_file(path,flag):# 处理文件，返回生成的TeX字符串
    with open(path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    start_idx = 0
    end_idx = 0
    for i, line in enumerate(content):
        if '起始页码' in line and start_idx == 0:
            start_idx = i
        elif '起始页码' in line:
            end_idx = i - 1

            yield process_info(content[start_idx:end_idx+1],flag)
            start_idx = i
    # 出循环再做一次
    yield process_info(content[end_idx:],flag)

def generate_tex(path,flag,out_txt):#生成TeX文件
    date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if flag =="ch":
        run_info(out_txt,"开始生成中文目录")
        try:
            tex_path = os.path.abspath(os.path.join(os.path.dirname(path), 'Chinese Content_{}.tex'.format(date_str)))
            with open(tex_path, 'w', encoding='utf-8') as file:
                # 写入模板头部
                with open("ch_content_head.txt", 'r', encoding='utf-8') as another_file:
                    file.write(another_file.read())
                file.write("\n\n%中间主体\n\n")
                # 写入目录
                for info in process_file(path,flag):
                    file.write(info)
                # 写入模板尾部
                with open("ch_content_end.txt", 'r', encoding='utf-8') as another_file:
                    file.write(another_file.read())
            run_info(out_txt,'中文目录TeX文件已生成\n')
        except Exception as e:
            run_info(out_txt,e)
            run_info(out_txt,'中文目录TeX文件生成失败\n')
    

    # 英文目录
    elif flag =="en":
        run_info(out_txt,"开始生成英文目录")
        try:
            tex_path = os.path.abspath(os.path.join(os.path.dirname(path), 'contents_{}.tex'.format(date_str)))
            with open(tex_path, 'w', encoding='utf-8') as file:
                # 写入模板头部
                with open("en_content_head.txt", 'r', encoding='utf-8') as another_file:
                    file.write(another_file.read())
                file.write("\n\n%中间主体\n\n")
                # 写入目录
                for info in process_file(path,flag):
                    file.write(info)
                # 写入模板尾部
                with open("en_content_end.txt", 'r', encoding='utf-8') as another_file:
                    file.write(another_file.read())
            run_info(out_txt,'英文目录TeX文件已生成\n')
        except Exception as e:
            run_info(out_txt,e)
            run_info(out_txt,'英文目录TeX文件生成失败\n')
