import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm

def main():
    color_list = [
                [0, 0, 0],
                [255, 255, 255],
                [255,128,0],
                [0,255,0],
                [0,128,0],
                [0,255,255],
                [0,0,255],
                [255,255,0],
        ]
    input_dir = r'E:\superlabel\标注软件测试-道路\test_data_label'
    output_dir=r'E:\superlabel\标注软件测试-道路\test_data_label255'
    os.makedirs(output_dir,exist_ok=True)
    for filename in tqdm(os.listdir(input_dir)):
        if filename.endswith((".tif", ".png", ".jpg")):
            # img = cv2.imread(os.path.join(input_dir, filename), -1)
            img = Image.open(os.path.join(input_dir, filename))
            img = np.array(img)
            color_label = colour_code_label(img, color_list)
            color_label = Image.fromarray(color_label.astype(np.uint8))
            # cv2.imwrite(os.path.join(output_dir, filename), color_label[:,:,::-1])
            color_label.save(os.path.join(output_dir, filename))

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

if __name__ == '__main__':
    main()
