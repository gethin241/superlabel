import os
import cv2
import numpy as np
import tqdm
import glob
from PIL import Image

def remap_labels_in_folder(folder_path, label_mapping, output_path):
    """
    遍历指定文件夹中的标签图像，并按照给定的映射表重新映射标签值。

    Args:
    - folder_path (str): 包含标签图像的文件夹路径。
    - label_mapping (list): 一个列表，用于指定新的标签映射关系，索引位置表示原始标签值，值表示新的标签值。
    - output_path (str): 保存处理后图像的文件夹路径。
    """


    # 获取文件夹中的所有文件名
    image_files = os.listdir(folder_path)
    image_files = [f for f in image_files if f.endswith('.png') or f.endswith('.tif')]

    for image_file in tqdm.tqdm(image_files):
        image_path = os.path.join(folder_path, image_file)

        # 使用 cv2 读取图像
        # img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        img = np.array(Image.open(image_path))
        
        if img is None:
            continue

        # 根据映射表重新映射标签值
        remapped_img = np.zeros_like(img)
        for x, y in label_mapping.items():
            remapped_img[img == x] = y
        
        # 保存处理后的图像
        output_file = os.path.join(output_path, image_file)
        # cv2.imwrite(output_file, remapped_img)
        pil_label = Image.fromarray(remapped_img)
        pil_label.save(output_file)
if __name__ == '__main__':


    paths=glob.glob(r'E:\temp\标注软件测试结果\数据集\label01')
    for folder_path in paths:
        # 示例用法
        # folder_path = r'/opt/data/private/datas/BJR2/crop512/train/label'
        label_mapping = {
            0: 0,
            1: 255,
            }
        output_path = folder_path.replace('label01','label255')
        print(folder_path)
        print(output_path)
        os.makedirs(output_path, exist_ok=True)

        remap_labels_in_folder(folder_path, label_mapping,output_path)

