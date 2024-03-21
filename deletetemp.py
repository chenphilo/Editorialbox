import os
from run_info import run_info

def delete_specific_files(directory):
    # 扩展名列表
    extensions_to_delete = ['.aux', '.bbl', '.bcf', '.blg', '.out', '.run.xml', '.synctex.gz']
    # 计数器，记录删除的文件数量
    files_deleted = 0
    
    # 遍历指定目录及其所有子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查当前文件的扩展名是否在要删除的扩展名列表中
            if any(file.endswith(ext) for ext in extensions_to_delete):
                # 构建完整的文件路径
                file_path = os.path.join(root, file)
                try:
                    # 尝试删除文件
                    os.remove(file_path)
                    files_deleted += 1
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    return files_deleted


def delete_main(directory, output_text):
    try:
        files_deleted = delete_specific_files(directory)
        run_info(output_text, f"删除完成，共删除{files_deleted}个文件。\n")

    except Exception as e:
        run_info(output_text, e)
        run_info(output_text, "程序错误\n")


# if __name__ == "__main__":
#     # 示例目录，请根据实际情况调整
#     directory = "/path/to/your/project/directory"
#     output_text = "operation_log.txt"
#     main(directory, output_text)
