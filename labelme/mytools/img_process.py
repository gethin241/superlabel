import json, os, shutil
from PIL import Image
import tqdm
import numpy as np
import cv2


def main():
    image_input_dir = r"E:\temp\farmland_50_100_800\image"
    cl_input_dir = r"E:\temp\farmland_50_100_800\cl_test800"
    output_dir = r"E:\temp\farmland_50_100_800\final800"
    os.makedirs(output_dir, exist_ok=True)
    search_dir = r'E:\temp\farmland_50_100_800\image'
    merge_img(image_input_dir, cl_input_dir, output_dir,search_dir)
    
def erode_dilate_image(image, dilation_size=15, erosion_size=15):
    """
    使用 OpenCV 对一张灰度图进行腐蚀和膨胀操作。

    参数:
    - image: PIL.Image 对象，灰度图像。
    - dilation_size: 膨胀核的大小（正方形）。
    - erosion_size: 腐蚀核的大小（正方形）。

    返回:
    - result: 膨胀后的 PIL.Image 对象。
    """

    # 将 PIL 图像转换为 OpenCV 格式的 NumPy 数组
    image_array = np.array(image)
    
    # 创建结构元素（核）
    dilation_kernel = np.ones((dilation_size, dilation_size), dtype=np.uint8)
    erosion_kernel = np.ones((erosion_size, erosion_size), dtype=np.uint8)
    
    # 进行腐蚀操作
    eroded_array = cv2.erode(image_array, erosion_kernel, iterations=1)
    
    # 进行膨胀操作
    dilated_array = cv2.dilate(eroded_array, dilation_kernel, iterations=1)
    
    # 将结果转换回 PIL.Image 对象
    result = Image.fromarray(dilated_array.astype(np.uint8), 'L')
    
    return result
    
def merge_img(img_dir1,img_dir2,output_dir,search_dir):
    
    def merge_two_img(im1,im2,output):
        # 调整图像大小
        width, height = im1.size
        im2 = im2.resize((width, height))
        
        # 创建一个新的图像，将两个图像水平合并
        new_im = Image.new('RGB', (width * 2, height))
        new_im.paste(im1, (0, 0))
        new_im.paste(im2, (width, 0))
        
        # 保存合并后的图像
        new_im.save(output)
    
    os.makedirs(output_dir, exist_ok=True)
    for filename in tqdm.tqdm(os.listdir(search_dir)):
        if filename.endswith((".tif",".png")):
            img1 = os.path.join(img_dir1, filename)
            img2 = os.path.join(img_dir2, filename)
            output = os.path.join(output_dir, filename)
            
            # 加载图片
            img1 = Image.open(img1)
            img2 = Image.open(img2)
            
            # 处理细小噪声
            img2 = erode_dilate_image(img2)
            merge_two_img(img1,img2,output)
            # shutil.copy(img1,output)


if __name__ == "__main__":
    main()
