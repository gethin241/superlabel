import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm

# paths to the folders to visualize
folder_paths = [
    r'E:\hunan_images\diff_emb_predicts',
    r'E:\hunan_images\cl_blocks_diffseg',
    r'E:\hunan_images\diff_emb_predicts_edit_label',
    r'E:\hunan_images\images_2018',
    r'E:\hunan_images\labels_2018_index',
]
output_path=r'E:\hunan_images\diff_emb_predicts_edit_plts'

os.makedirs(output_path,exist_ok=True)

color_list = [
            [255, 255, 255],
            [255,128,0],
            [0,255,0],
            [0,128,0],
            [0,255,255],
            [0,0,255],
            [255,255,0],
    ]

def colour_code_label(label, label_values):
    """
    Given a [HW] array of class keys(or one hot[HWC]), colour code the label;
    also can weight the colour coded label and image, maybe save the final result.

    Args:
        label: single channel array where each value represents the class key.
        label_values
    Returns:
        Colour coded label
    """
    label, colour_codes = np.array(label), np.array(label_values)
    if len(label.shape) == 3:
        label = np.argmax(label, axis=2)  # [HWC] -> [HW]
    color_label = np.zeros((label.shape[0], label.shape[1], 3), dtype=np.uint8)
    mask = label < len(colour_codes)
    color_label[mask] = colour_codes[label[mask].astype(int)]
    return color_label

def get_common_files(folder_paths):
    # 获取第一个文件夹中的文件列表
    file_lists = [set(os.listdir(folder_paths[0]))]

    # 遍历其余文件夹，获取它们的文件列表，并取交集
    for folder_path in folder_paths[1:]:
        file_lists.append(set(os.listdir(folder_path)))

    common_files = list(file_lists[0].intersection(*file_lists[1:]))
    common_files_sorted = sorted(common_files)

    return common_files_sorted

def visualize_folders(folder_paths, save_folder):
    num_folders = len(folder_paths)
    num_subplot_rows = 2
    num_subplot_cols = (num_folders + 1) // num_subplot_rows

    # 创建用于保存图片的文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # 获取所有文件夹中的共同文件
    common_files=get_common_files(folder_paths)
    
    process_bar=tqdm(common_files)

    # 遍历共同文件，逐个可视化
    for i, file in enumerate(common_files):
        process_bar.update(1)
        fig = plt.figure(figsize=[5 * num_subplot_cols, 5 * num_subplot_rows])
        for j, folder_path in enumerate(folder_paths):
            img = cv2.imread(os.path.join(folder_path, file), -1)
            
            if len(img.shape) == 3:
                img = img[:, :, ::-1]
            elif len(img.shape) == 2:
                if 'cl_blocks' in folder_path:
                    img = img == 255
                else:
                    img = colour_code_label(img, color_list)
            
            ax = fig.add_subplot(num_subplot_rows, num_subplot_cols, j + 1)
            ax.imshow(img, cmap='gray' if len(img.shape) == 2 else None)
            ax.axis('off')
            ax.set_title(f'{os.path.basename(folder_path)}')
        
        # 保存可视化结果
        plt.tight_layout()
        plt.savefig(os.path.join(save_folder, f'{file}.png'))
        plt.close()
        

visualize_folders(folder_paths, output_path)
