from run_info import run_info
import re
import random

def parse_line(line):
    line = line.strip().strip(	)
    if not line:
        return None
    
    tags = {
        "type": "",
        "original": "",
        "index": "",
        "author": "",
        "title": "",
        "editor": "",
        "journal": "",
        "year": "",
        "address": "",
        "publisher": "",
        "pages": "",
        "number": ""
    }
    
    # 三种标准格式
    pattern1 = r'\s*\[(.*)\]\s*(.*)\s*，\s*“(.*?)”\s*，\s*(.*?)\s*，\s*(.*?)\s*，\s*(.*?)年\s*，\s*(.*?)\s*：\s*(.*?)\s*，\s*第(.*?)页\s*。\s*'
    match1 = re.match(pattern1, line)
    pattern11 = r'\s*\[(.*)\]\s*(.*)\s*，\s*“(.*?)”\s*，\s*(.*?)\s*，\s*(.*?)\s*，\s*(.*?)年\s*，\s*(.*?)\s*，\s*第(.*?)页\s*。\s*'
    match11 = re.match(pattern11, line)#没冒号的版本

    pattern2 = r'\s*\[(.*)\]\s*(.*)\s*，\s*“\s*(.*?)\s*”\s*，\s*(.*?)\s*，\s*(.*?)年\S*，\s*(.*?)\s*，\s*第(.*?)页\s*。\s*'
    match2 = re.match(pattern2, line)

    pattern3 = r'\s*\[(.*)\]\s*(.*)\s*，\s*(.*?)\s*，\s*(.*?)年\s*，\s*(.*?)\s*：\s*(.*?)\s*。\s*'
    match3 = re.match(pattern3, line)
    pattern33 = r'\s*\[(.*)\]\s*(.*)\s*，\s*(.*?)\s*，\s*(.*?)年\s*，\s*(.*?)\s*。\s*'
    match33 = re.match(pattern33, line)#没冒号的版本

    # %Chinese InProceedings/InCollections
    if match1:
        # print("match InProceedings")
        tags.update({
            "type": "InProceedings",
            "original": line,
            "index": match1.group(1),
            "author": match1.group(2),
            "title": match1.group(3),
            "editor": match1.group(4),
            "journal": match1.group(5),
            "year": match1.group(6),
            "address": match1.group(7),
            "publisher": match1.group(8),
            "pages": match1.group(9),
        })
    elif match11:
        # print("match InProceedings 无冒号")
        tags.update({
            "type": "InProceedings",
            "original": line,
            "index": match11.group(1),
            "author": match11.group(2),
            "title": match11.group(3),
            "editor": match11.group(4),
            "journal": match11.group(5),
            "year": match11.group(6),
            "address": match11.group(7),
            "publisher": match11.group(7),
            "pages": match11.group(8),
        })
    # %Chinese ARTICLE
    elif match2:
        # print("match ARTICLE")
        tags.update({
            "type": "ARTICLE",
            "original": line,
            "index": match2.group(1),
            "author": match2.group(2),
            "title": match2.group(3),
            "journal": match2.group(4),
            "year": match2.group(5),
            "number": match2.group(6),
            "pages": match2.group(7),
        })
    # %Chinese BOOK
    elif match3:
        # print("match BOOK")
        tags.update({
            "type": "BOOK",
            "original": line,
            "index": match3.group(1),
            "author": match3.group(2),
            "journal": match3.group(3),
            "year": match3.group(4),
            "address": match3.group(5),
            "publisher": match3.group(6),
        })
    elif match33:
        # print("match BOOK")
        tags.update({
            "type": "BOOK",
            "original": line,
            "index": match33.group(1),
            "author": match33.group(2),
            "journal": match33.group(3),
            "year": match33.group(4),
            "address": match33.group(5),
            "publisher": match33.group(5),
        })
    else:
        # print("no match")
        tags.update({
            "type": "None",
            "original": line,
            "index": 'index' + str(random.randint(100000000, 999999999)),
            "author": 'author',
        })
        
    return tags

def write_to_file(data, file):
    file.write("%" + data["original"] + "\n")
    file.write("% 判断格式为" + data["type"] + "\n")
    file.write("@misc{" + data["index"] + ", \n")
    file.write("    userf={cn},\n")
    file.write("    author={" + data["author"] + "},  \n")
    file.write("    title={" + data["title"] + "},\n")
    file.write("    year={" + data["year"] + "},\n")
    file.write("    editor={" + data["editor"] + "},\n")
    file.write("    journal={" + data["journal"] + "},\n")
    file.write("    publisher={" + data["publisher"] + "}, \n")
    file.write("    pages={" + data["pages"] + "},\n")
    file.write("    address = {" + data["address"] + "}\n")
    file.write("}\n\n")
    ############################
    # if data["type"] == "InProceedings":
    #     file.write("@misc{" + data["index"] + ", \n")
    #     file.write("    userf={cn},\n")
    #     file.write("    author={" + data["author"] + "},  \n")
    #     file.write("    title={" + data["title"] + "},\n")
    #     file.write("    year={" + data["year"] + "},\n")
    #     file.write("    editor={" + data["editor"] + "},\n")
    #     file.write("    journal={" + data["journal"] + "},\n")
    #     file.write("    publisher={" + data["publisher"] + "}, \n")
    #     file.write("    pages={" + data["pages"] + "},\n")
    #     file.write("    address = {" + data["address"] + "}\n")
    #     file.write("}\n\n")
    # elif data["type"] == "ARTICLE":
    #     file.write("@misc{" + data["index"] + ", \n")
    #     file.write("    userf={cn},\n")
    #     file.write("    author={" + data["author"] + "},  \n")
    #     file.write("    title={" + data["title"] + "},\n")
    #     file.write("    year={" + data["year"] + "},\n")
    #     file.write("    journal={" + data["journal"] + "},\n")
    #     file.write("    number\t={" + data["number"] + "},\n")
    #     file.write("    pages={" + data["pages"] + "},\n")
    #     file.write("}\n\n")
    # elif data["type"] == "BOOK":
    #     file.write("@misc{" + data["index"] + ", \n")
    #     file.write("    userf={cn},\n")
    #     file.write("    author={" + data["author"] + "},  \n")
    #     file.write("    year={" + data["year"] + "},\n")
    #     file.write("    journal={" + data["journal"] + "},\n")
    #     file.write("    publisher={" + data["publisher"] + "}, \n")
    #     file.write("    address = {" + data["address"] + "}\n")
    #     file.write("}\n\n")
    # else:
    #     file.write("不符合标准，请手动处理 \n\n")

def cbibtex_process_file(input_file_path, output_text):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, open(input_file_path + "_bibtex.bib", 'w', encoding='utf-8') as output_file:
            for line in input_file:
                data = parse_line(line)
                write_to_file(data, output_file)
        run_info(output_text, "生成bibtex完成\n")
    except Exception as e:
        run_info(output_text, e)
        return False
    