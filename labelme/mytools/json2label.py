import json, os, tqdm
import numpy as np
import cv2
from PIL import Image

def main():
    input_dir = r"E:\superlabel\标注软件测试-道路\测试结果\标注结果\zdd_ours"
    output_dir = input_dir+'_label'
    # output_dir = r"E:\superlabel\标注软件测试2样本数量\测试结果\final800"
    os.makedirs(output_dir, exist_ok=True)
    class_names = [
        "noinfo",
        "farmland",
        "forest",
        "grass",
        "water",
        "artificial facilities",
        "unused land",
    ]

    # 遍历指定目录中的所有.tif文件
    for filename in tqdm.tqdm(os.listdir(input_dir)):
        if filename.endswith(".json"):
            input_filepath = os.path.join(input_dir, filename)

            output_filepath = os.path.join(
                output_dir, os.path.splitext(filename)[0] + ".tif"
            )
            labelme_json_to_labelindex_tif(input_filepath, class_names, output_filepath)


def labelme_json_to_labelindex_tif(
    labelme_json_path,
    class_list,
    output_tif_path,
    image_height=512,
    image_width=512,
    color_list=None,
    output_color=False,
):
    # 读取labelme格式的JSON文件
    with open(labelme_json_path, "r", encoding='utf-8', errors='ignore') as f:
        labelme_data = json.load(f)

    # 构建一个映射表: 类别名称 -> 类别索引
    class_to_index = {class_name: idx for idx, class_name in enumerate(class_list)}

    # 创建一个二维数组来存储label index
    label_index_image = np.zeros((image_height, image_width), dtype=np.uint8)

    # 计算多边形的面积并排序
    def polygon_area(points):
        polygon = np.array(points, dtype=np.int32)
        return cv2.contourArea(polygon)

    shapes_sorted_by_area = sorted(
        labelme_data["shapes"],
        key=lambda shape: polygon_area(shape["points"]),
        reverse=True,
    )

    # 填充label index图像
    for shape in shapes_sorted_by_area:
        label = shape["label"]
        if label in class_to_index or True:
            # class_index = class_to_index[label]
            # TODO 
            class_index = 255
            points = shape["points"]
            polygon = np.array(points, dtype=np.int32)
            cv2.fillPoly(label_index_image, [polygon], class_index)
        else:
            print(f"Warning: label '{label}' not found in class_list")

    # 保存label index图像为.tif文件
    # cv2.imwrite(output_tif_path, label_index_image)
    pil_label = Image.fromarray(label_index_image)
    pil_label.save(output_tif_path)
    
    if output_color:
        # 创建一个三通道的彩色图像
        color_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
        for class_index, color in enumerate(color_list):
            color_image[label_index_image == class_index] = color
        cv2.imwrite(output_tif_path.replace(".tif", "_color.tif"), color_image[:,:,::-1])


if __name__ == "__main__":
    main()
