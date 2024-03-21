from run_info import run_info
import re

def contains_chinese(text):
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def parse_line(index, line):
    print("Parsing line:", line)  #正在解析的行
    # if not line:
    #     print("Empty line detected.")  #检测到空行
    #     return None
    has_chinese = contains_chinese(line)

    tags = {
        "userf": "cn" if has_chinese else "", # cn或空
        "type": "", # 类型
        "original": line, # 原始数据
        "index": index,
        "author": "",
        "title": "",
        "editor": "",
        "booktitle": "",
        "journal": "",
        "year": "",
        "address": "",
        "publisher": "",
        "pages": "",
        "number": "",
        "volume": ""
    }
    # 先根据特殊符号能填则填
    if tags["userf"] == "cn":
        if "年" in line:
            year = re.findall(r'(\d+)年', line)
            if year:
                tags["year"] = year[0]
        else:
            year = re.findall(r'([12]\d\d\d)', line)
            if year:
                tags["year"] = year[0]

        pages = re.findall(r'第(.+)页', line)
        if pages:
            tags["pages"] = pages[0]

        number = re.findall(r'(\d+)期', line)
        if number:
            tags["number"] = number[0]

        address = re.findall(r'(.+)：(.+)', line)
        if address:
            tags["address"] = address[0][0]
            tags["publisher"] = address[0][1]
    else:
        year = re.findall(r'([12]\d\d\d).', line)
        if year:
            tags["year"] = year[0]

        # address = re.findall(r'(.+): (.+)', line)
        # if address:
        #     tags["address"] = address[0][0]
        #     tags["publisher"] = address[0][1]
        
        pages = re.findall(r'pp\.(\d+-*\d*)', line)
        if pages:
            tags["pages"] = pages[0]
        

    # 下方为完全匹配的情况，代码还很不成熟，需要进一步完善
    #中文格式
    c_title_exp = '[\u4e00-\u9fff\u3000：]+'#匹配书名，标题等
    c_name_exp = '[\u4e00-\u9fff，]+'#匹配名字
    c_name_exp2 = '[\u4e00-\u9fff]+'#匹配名字
    c_year_exp = '[12]\d\d\d'#匹配年份
    pattern_cn_pr = r'\s*(\[\d\])*\s*('+c_name_exp+')\s*，\s*“('+c_title_exp+')”\s*，\s*('+c_name_exp+')\s*，\s*('+c_title_exp+')\s*，\s*('+c_year_exp+')年\s*，\s*('+c_name_exp2+')\s*：\s*('+c_name_exp2+')\s*，\s*第(\d+-*\d*)页\s*。\s*'#中文proceedings
    pattern_cn_pr_noad = r'\s*(\[\d\])*\s*('+c_name_exp+')\s*，\s*“('+c_title_exp+')”\s*，\s*('+c_name_exp+')\s*，\s*('+c_title_exp+')\s*，\s*('+c_year_exp+')年\s*，\s*('+c_name_exp2+')\s*，\s*第(\d+-*\d*)页\s*。\s*' #中文无出版地proceedings
    pattern_cn_b = r'\s*(\[\d\])*\s*('+c_name_exp+')\s*，\s*('+c_title_exp+')\s*，\s*('+c_year_exp+')年\s*，\s*('+c_name_exp2+')\s*：\s*('+c_name_exp2+')\s*。\s*'#中文book
    pattern_cn_b_noad = r'\s*(\[\d\])*\s*('+c_name_exp+')\s*，\s*('+c_title_exp+')\s*，\s*('+c_year_exp+')年\s*，\s*('+c_name_exp2+')\s*。\s*'#中文无出版地book
    pattern_cn_ar = r'\s*(\[\d\])*\s*('+c_name_exp+')\s*，\s*“\s*('+c_title_exp+')\s*”\s*，\s*('+c_title_exp+')\s*，\s*('+c_year_exp+')年\s*，\s*(.*?)期\s*，\s*第(\d+-*\d*)页\s*。\s*'#中文article
    ### 英文参考文献
    title_exp = '[a-zA-Z\s]+:?[a-zA-Z\s]*'#匹配书名，标题等
    name_exp = '[a-zA-Z\.\s]+'#匹配名字
    year_exp = '[12]\d\d\d'#匹配年份
    pattern_en_pr = r'\s*(\[\d\])*\s*('+ name_exp +')\.\s*('+ year_exp +')\.\s*“('+title_exp+')”\.\s*[iI][nN]:?\s*('+ name_exp +')\s*\(?[Ee][Dd]s?\)?[\.,]\s*('+title_exp+')\.\s*([a-zA-Z\s,]+):\s*([a-zA-Z\s]+)\.\s*(.*?)\.\s*'#proceedings
    pattern_en_pr_noad = r'\s*(\[\d\])*\s*('+ name_exp +')\.\s*('+ year_exp +')\.\s*“('+title_exp+')”\.\s*[iI][nN]:?\s*('+ name_exp +')\s*\(?[Ee][Dd]s?\)?[\.,]\s*('+title_exp+')\.\s*([a-zA-Z\s]+)\.\s*(.*?)\.\s*'#无出版地proceedings
    ##^(?:[^:]*:)?[^:]*[a-zA-Z].*$
    pattern_en_b = r'\s*(\[\d\])*\s*('+ name_exp +')\.\s*('+ year_exp +')\.\s*('+title_exp+')\.\s*([a-zA-Z\s,]+):\s*([a-zA-Z\s]+)\.\s*'#books
    pattern_en_b_noad = r'\s*(\[\d\])*\s*('+ name_exp +')\.\s*('+ year_exp +')\.\s*('+title_exp+')\.\s*([a-zA-Z\s]+)\.\s*'#无出版地books
    pattern_en_ar = r'\s*(\[\d\])*\s*('+ name_exp +')\.\s*('+ year_exp +')\.\s*“('+title_exp+')”\.([a-zA-Z\s])\.\s*(\d+)\((\d+)\)\.\s*pp\.(\d+)\-+(\d+)\.\s*'#article
    pattern_en_ar_nonum = r'\s*(\[\d\])*\s*('+ name_exp +')\.\s*('+ year_exp +')\.\s*“('+title_exp+')”\.([a-zA-Z\s])\.\s*(\d+):\s*pp\.(\d+)\-+(\d+)\.\s*'#无number article
    match_en_pr = re.match(pattern_en_pr, line)
    match_en_pr_noad = re.match(pattern_en_pr_noad, line)
    match_en_b = re.match(pattern_en_b, line)
    match_en_b_noad = re.match(pattern_en_b_noad, line)
    match_en_ar = re.match(pattern_en_ar, line)
    match_en_ar_nonum = re.match(pattern_en_ar_nonum, line)

    match_cn_pr = re.match(pattern_cn_pr, line)
    match_cn_pr_noad = re.match(pattern_cn_pr_noad, line)
    match_cn_b = re.match(pattern_cn_b, line)
    match_cn_b_noad = re.match(pattern_cn_b_noad, line)
    match_cn_ar = re.match(pattern_cn_ar, line)
    # %Chinese InProceedings
    if match_cn_pr:
        # print("match InProceedings")
        tags.update({
            "userf": "cn",
            "type": "inproceedings",
            "author": match_cn_pr.group(2),
            "title": match_cn_pr.group(3),
            "editor": match_cn_pr.group(4),
            "booktitle": match_cn_pr.group(5),
            "year": match_cn_pr.group(6),
            "address": match_cn_pr.group(7),
            "publisher": match_cn_pr.group(8),
            "pages": match_cn_pr.group(9),
        })
    elif match_cn_pr_noad:
        # print("match InProceedings 无冒号")
        tags.update({
            "userf": "cn",
            "type": "inproceedings",
            "author": match_cn_pr_noad.group(2),
            "title": match_cn_pr_noad.group(3),
            "editor": match_cn_pr_noad.group(4),
            "booktitle": match_cn_pr_noad.group(5),
            "year": match_cn_pr_noad.group(6),
            "address": match_cn_pr_noad.group(7),
            "publisher": match_cn_pr_noad.group(7),
            "pages": match_cn_pr_noad.group(8),
        })
    # %Chinese ARTICLE
    elif match_cn_ar:
        # print("match ARTICLE")
        tags.update({
            "userf": "cn",
            "type": "article",
            "author": match_cn_ar.group(2),
            "title": match_cn_ar.group(3),
            "journal": match_cn_ar.group(4),
            "year": match_cn_ar.group(5),
            "number": match_cn_ar.group(6),
            "pages": match_cn_ar.group(7),
        })
    # %Chinese BOOK
    elif match_cn_b:
        # print("match BOOK")
        tags.update({
            "userf": "cn",
            "type": "book",
            "author": match_cn_b.group(2),
            "journal": match_cn_b.group(3),
            "year": match_cn_b.group(4),
            "address": match_cn_b.group(5),
            "publisher": match_cn_b.group(6),
        })
    elif match_cn_b_noad:
        # print("match BOOK")
        tags.update({
            "userf": "cn",
            "type": "book",
            "author": match_cn_b_noad.group(2),
            "journal": match_cn_b_noad.group(3),
            "year": match_cn_b_noad.group(4),
            "address": match_cn_b_noad.group(5),
            "publisher": match_cn_b_noad.group(5),
        })

    ## 英文参考文献
    elif match_en_pr:
        # print("match en InProceedings")
        tags.update({
            "type": "inproceedings",
            "author": match_en_pr.group(2),
            "year": match_en_pr.group(3),
            "title": match_en_pr.group(4),
            "editor": match_en_pr.group(5),
            "booktitle": match_en_pr.group(7),
            "address": match_en_pr.group(8),
            "publisher": match_en_pr.group(9),
            "pages": match_en_pr.group(10),
        })
    elif match_en_pr_noad:
        # print("match en InProceedings")
        tags.update({
            "type": "inproceedings",
            "author": match_en_pr_noad.group(2),
            "year": match_en_pr_noad.group(3),
            "title": match_en_pr_noad.group(4),
            "editor": match_en_pr_noad.group(5),
            "booktitle": match_en_pr_noad.group(7),
            "publisher": match_en_pr_noad.group(8),
            "pages": match_en_pr_noad.group(9),
        })
    elif match_en_b:
        # print("match en BOOK")
        tags.update({
            "type": "book",
            "author": match_en_b.group(2),
            "year": match_en_b.group(3),
            "title": match_en_b.group(4),
            "address": match_en_b.group(5),
            "publisher": match_en_b.group(6),

        })
    elif match_en_b_noad:
        # print("match en BOOK")
        tags.update({
            "type": "book",
            "author": match_en_b_noad.group(2),
            "year": match_en_b_noad.group(3),
            "title": match_en_b_noad.group(4),
            "publisher": match_en_b_noad.group(5),

        })
    elif match_en_ar:
        # print("match en ARTICLE")
        tags.update({
            "type": "article",
            "author": match_en_ar.group(2),
            "year": match_en_ar.group(3),
            "title": match_en_ar.group(4),
            "journal": match_en_ar.group(5),
            "number": match_en_ar.group(7),
            "volume": match_en_ar.group(6),
            "pages": match_en_ar.group(8) + "-" + match_en_ar.group(9),
        })
    elif match_en_ar_nonum:
        # print("match en ARTICLE")
        tags.update({
            "type": "article",
            "author": match_en_ar_nonum.group(2),
            "year": match_en_ar_nonum.group(3),
            "title": match_en_ar_nonum.group(4),
            "journal": match_en_ar_nonum.group(5),
            "volume": match_en_ar.group(6),
            "pages": match_en_ar_nonum.group(7) + "-" + match_en_ar_nonum.group(8),

        })
    else:
        # print("no match")
        tags.update({
            "userf": "cn",
            "type": "misc",
            "author": line,
        })
        
    return tags

def write_to_file(data, file):
    file.write("%" + data["original"])
    file.write("% 判断格式为" + data["type"] + "\n")
    file.write("@" + data["type"] + "{" + data["index"] + ", \n")
    file.write("    userf={" + data["userf"]+"}, \n")
    file.write("    author={" + data["author"] + "},  \n")
    file.write("    title={" + data["title"] + "},\n")
    file.write("    year={" + data["year"] + "},\n")
    file.write("    editor={" + data["editor"] + "},\n")
    file.write("    journal={" + data["journal"] + "},\n")
    file.write("    booktitle={" + data["booktitle"] + "},\n")
    file.write("    number={" + data["number"] + "},\n")
    file.write("    volume={" + data["volume"] + "},\n")
    file.write("    publisher={" + data["publisher"] + "}, \n")
    file.write("    pages={" + data["pages"] + "},\n")
    file.write("    address = {" + data["address"] + "}\n")
    file.write("}\n\n")

def cbibtex_process_file(input_file_path, output_text):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, open(input_file_path + "_bibtex.bib", 'w', encoding='utf-8') as output_file:
            i = 1
            for line in input_file:
                if line.strip() == "":
                    continue
                else:
                    try:
                        data = parse_line(str(i), line)
                        write_to_file(data, output_file)
                        i = i+1
                    except Exception as e:
                        run_info(output_text, e)
                        continue
        run_info(output_text, "生成bibtex完成\n")
    except Exception as e:
        run_info(output_text, e)
        return False