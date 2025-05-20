import os
import shutil

def copy_matching_structure(src_folder, dst_folder, ref_folder):
    # 获取参考文件夹中的所有文件名（不带后缀）
    ref_files = {os.path.splitext(f)[0] for f in os.listdir(ref_folder) if os.path.isfile(os.path.join(ref_folder, f))}
    
    for root, dirs, files in os.walk(src_folder):
        # 计算当前遍历到的目录相对于源文件夹的相对路径
        rel_path = os.path.relpath(root, src_folder)
        dest_path = os.path.join(dst_folder, rel_path)

        # 如果当前目录下的文件或文件夹名（不考虑后缀）在参考文件夹的文件名列表中，则进行复制操作
        for name in dirs + files:
            name_no_ext, ext = os.path.splitext(name)
            if name_no_ext in ref_files:
                # 构建源路径和目的路径
                src_path = os.path.join(root, name)
                dest_item_path = os.path.join(dest_path, name)

                # 确保目的目录存在
                os.makedirs(os.path.dirname(dest_item_path), exist_ok=True)

                # 判断是文件还是文件夹并复制
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_item_path)
                    print(f"Directory copied: {src_path} -> {dest_item_path}")
                else:
                    shutil.copy2(src_path, dest_item_path)
                    print(f"File copied: {src_path} -> {dest_item_path}")

# 使用方法
source_directory = r'E:\superlabel\superlabel'  # 目标目录
destination_directory = r'E:\superlabel\sidefarm'  # 指定文件夹
reference_directory = r'E:\superlabel\sidefarm\thejsons'  # 指定文件夹里的文件名作为参考

copy_matching_structure(source_directory, destination_directory, reference_directory)