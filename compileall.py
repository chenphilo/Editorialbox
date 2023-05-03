import os
import glob
from run_info import run_info

def compile_tex(folder, folder_name,out_txt):
    run_info(out_txt, f"打开路径：{folder}\n")
    os.chdir(folder)  # 切换到 tex 文件所在的文件夹
    run_info(out_txt, f'第一步：Xelatex "{folder_name}.tex"\n')
    ret = os.system(f'Xelatex "{folder_name}.tex"\n >> NUL')
    if ret != 0:
        run_info(out_txt, f'Xelatex {folder_name} 失败！\n')
        return
    run_info(out_txt, f'第二步：biber -l=zh_pinyin "{folder_name}"\n')#注意biber不能加扩展名
    ret = os.system(f'biber -l=zh_pinyin "{folder_name}"\n >> NUL')
    if ret != 0:
        run_info(out_txt, f'biber -l=zh_pinyin {folder_name} 失败！\n')
        return
    run_info(out_txt, f'第三步：Xelatex "{folder_name}.tex"\n')
    ret = os.system(f'Xelatex "{folder_name}.tex"\n >> NUL')
    if ret != 0:
        run_info(out_txt, f'Xelatex {folder_name} 失败！\n')
        return
    run_info(out_txt, f'第四步：Xelatex "{folder_name}.tex"\n')
    ret = os.system(f'Xelatex "{folder_name}.tex"\n >> NUL')
    if ret != 0:
        run_info(out_txt, f'Xelatex {folder_name} 失败！\n')
        return

    

def compile_pdfs(folder_path , out_txt):
    # 获取所有匹配的文件夹
    folders = glob.glob(os.path.join(folder_path, "[0-9][0-9]*"))
    # 遍历所有文件夹，并将其中唯一的PDF文件添加到合并器中
    for folder in folders:
        if folder.startswith(os.path.join(folder_path, "000")):
            continue
        folder_name = folder.split()[-1]# 读取文件夹名最后的作者名
        tex_path = os.path.join(folder, f'{folder_name}.tex')
        if os.path.exists(tex_path):
            try:
                compile_tex(folder, folder_name, out_txt)
            except:
                run_info(out_txt, f"编译{folder_name}文件时出错！\n")
        else:
            run_info(out_txt, f"没有找到{folder_name}文件！\n")

    run_info(out_txt, "运行结束，请确认上方是否有错。\n")
