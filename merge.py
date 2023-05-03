import os
import glob
from PyPDF2 import PdfMerger
import datetime
from run_info import run_info



def compile_tex(tex_path):
    """
    编译tex文件为pdf文件
    tex_path: str, 不带扩展名的tex文件路径
    """
    os.system(f"XeLaTeX {tex_path}")
    os.system(f"biber -l=zh_pinyin {tex_path}")
    os.system(f"XeLaTeX {tex_path}")

def add_pdf_and_outlines(pdf_merger, folder, folder_name, tmpcount):
    pdf_file_path = os.path.join(folder, f"{folder_name}.pdf")
    pdf_merger.append(pdf_file_path)
    pdf_merger.add_outline_item(title=folder_name, pagenum=tmpcount)
    tmpcount = len(pdf_merger.pages)
    return tmpcount

def merge_pdfs(folder_path, out_txt):
    # 获取文件夹路径
    # if getattr(sys, 'frozen', False):
    #     # 如果是以可执行文件形式运行
    #     folder_path = os.path.abspath(os.path.dirname(sys.executable))
    # else:
    #     # 如果是以脚本形式运行
    #     folder_path = os.path.abspath(os.path.dirname(__file__))
    
    run_info(out_txt, f"文件夹路径：{folder_path}\n")

    # 获取所有匹配的文件夹
    folders = glob.glob(os.path.join(folder_path, "[0-9][0-9]*"))

    # 创建一个PdfMerger对象
    pdf_merger = PdfMerger()

    try:
        # 将扉页添加到合并器中
        cover_file_path = os.path.join(folder_path, "扉页.pdf")
        run_info(out_txt, f"找pdf路径：{cover_file_path}\n")
        if os.path.exists(cover_file_path):
            pdf_merger.append(cover_file_path)
        else:
            run_info(out_txt, "没有找到扉页文件！\n")

        pdf_merger.add_outline_item('cover', 0)
    
    except Exception as e:
        run_info(out_txt, f"处理扉页时出错啦：{e}\n")

    # 遍历所有文件夹，并将其中唯一的PDF文件添加到合并器中
    for folder in folders:
        tmpcount = len(pdf_merger.pages)
        if folder.startswith(os.path.join(folder_path, "000")):
            chinese_content_path = os.path.join(folder, 'Chinese Content.pdf')
            run_info(out_txt, f"找pdf路径：{chinese_content_path}\n")
            english_content_path = os.path.join(folder, 'contents.pdf')
            run_info(out_txt, f"找pdf路径：{english_content_path}\n")
            if os.path.exists(chinese_content_path):
                try:
                    tmpcount =  add_pdf_and_outlines(pdf_merger, folder, 'Chinese Content', tmpcount)
                except Exception as e:
                    run_info(out_txt, f"处理中文目录时出错啦：{e}\n")
            else:
                run_info(out_txt, "没有找到中文目录文件！\n")
            if os.path.exists(english_content_path):
                try:
                    tmpcount =  add_pdf_and_outlines(pdf_merger, folder, 'contents', tmpcount)
                except Exception as e:
                    run_info(out_txt, f"处理英文目录时出错啦：{e}\n")
            else:
                run_info(out_txt, "没有找到英文目录文件！\n")
        else:
            folder_name = folder.split()[-1]# 读取文件夹名最后的作者名
            pdf_path = os.path.join(folder, f'{folder_name}.pdf')
            run_info(out_txt, f"找pdf路径：{pdf_path}\n")
            if os.path.exists(pdf_path):
                try:
                    tmpcount =  add_pdf_and_outlines(pdf_merger, folder, folder_name, tmpcount)
                except Exception as e:
                    run_info(out_txt, f"处理{folder_name}时出错啦：{e}\n")
            else:
                run_info(out_txt, f"没有找到{folder_name}文件！\n")

    # 将所有PDF文件合并并保存到指定路径
    now = datetime.datetime.now()
    output_path = os.path.join(
        folder_path, f"合并{now.strftime('%Y_%m_%d_%H_%M_%S')}.pdf")
    with open(output_path, "wb") as output_file:
        pdf_merger.write(output_file)

    run_info(out_txt, "运行结束，请确认上方是否有错。\n")
