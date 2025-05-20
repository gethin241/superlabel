from osgeo import gdal, ogr
import numpy as np
import json, os
import tqdm
import shutil


def main():
    input_dir = r"E:\superlabel\testgen626_test\testgen626_test"
    shpfile_dir = input_dir + "_shpfile"
    output_dir = input_dir + "_jsonfile"
    os.makedirs(shpfile_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    class_names = [
        "noinfo",
        "road",
        # "farmland",
        # "forest",
        # "grass",
        # "water",
        # "artificial facilities",
        # "unused land",
    ]
    ignore_0 = True

    # 遍历指定目录中的所有.tif文件
    for filename in tqdm.tqdm(os.listdir(input_dir)):
        if filename.endswith((".tif", ".png")):
            input_filepath = os.path.join(input_dir, filename)
            shpfile_filepath = os.path.join(
                shpfile_dir, os.path.splitext(filename)[0] + ".shp"
            )
            output_filepath = os.path.join(
                output_dir, os.path.splitext(filename)[0] + ".json"
            )

            # 示例调用
            raster_to_vector(input_filepath, shpfile_filepath)
            vector_to_labelme(
                shpfile_filepath, output_filepath, input_filepath, 512, 512, class_names,ignore_0
            )
    
    shutil.rmtree(shpfile_dir)
        
def raster_to_vector(raster_path, vector_output_path, min_area=5):

    # 读取栅格标签
    ds = gdal.Open(raster_path)
    band = ds.GetRasterBand(1)

    # 创建矢量文件
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds_out = driver.CreateDataSource(vector_output_path)
    layer = ds_out.CreateLayer("label", geom_type=ogr.wkbPolygon)

    # 添加DN属性字段
    dn_field = ogr.FieldDefn("DN", ogr.OFTInteger)
    layer.CreateField(dn_field)

    # 获取栅格标签中每个类别的多边形，并将像素值作为DN值写入矢量文件
    gdal.Polygonize(band, None, layer, 0, [], callback=None)

    # 对每个多边形进行简化和过滤
    feature = layer.GetNextFeature()
    while feature is not None:
        geometry = feature.GetGeometryRef()
        simplified_geometry = geometry.Simplify(2)  # 调整简化程度，可以根据需要调整
        
        # 检查面积是否大于最小面积阈值
        if simplified_geometry.GetArea() < min_area:
            layer.DeleteFeature(feature.GetFID())
        else:
            feature.SetGeometry(simplified_geometry)
            layer.SetFeature(feature)

        feature = layer.GetNextFeature()

    # 关闭数据集
    ds = None
    ds_out = None
    del ds
    del ds_out

def correct_points(points,
    image_height=512,
    image_width=512,):
    total_x = 0
    total_y = 0
    for point in points:
        # Accumulate sum of coordinates for averaging later
        total_x += point[0]
        total_y += point[1]

    # Calculate average coordinates
    avg_x = total_x / len(points)
    avg_y = total_y / len(points)

    # Calculate how many times 512 fits into the average coordinates
    divisor_x = int(avg_x // 512)
    divisor_y = int(avg_y // 512)
    
    for point in points:
        point[0] = point[0] - divisor_x * 512
        point[1] = point[1] - divisor_y * 512
        # print(point)
        
    return points
    

def vector_to_labelme(vector_input_path, labelme_output_path, 
                      image_path, image_height, image_width, class_names=None, ignore_0=False):
    # 打开矢量数据源
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.Open(vector_input_path, 0)  # 0 表示只读模式
    if data_source is None:
        raise Exception(f"无法打开矢量文件 {vector_input_path}")

    # 获取图层
    layer = data_source.GetLayer()

    # 构建Labelme格式的数据
    labelme_data = {
        "version": "4.9.5",  # LabelMe版本号
        "flags": {},
        "shapes": [],
        "imagePath": os.path.basename(image_path),
        "imageData": None,
        "imageHeight": image_height,
        "imageWidth": image_width,
    }

    # 将矢量数据转换为Labelme格式
    for feature in layer:
        geometry = feature.GetGeometryRef()
        shape_category = feature.GetField("DN")  # 假设'DN'字段存储了类别值
        if ignore_0 and shape_category == 0:
            continue
        if class_names is not None:
            shape_category = class_names[shape_category]

        if geometry.GetGeometryName() == 'POLYGON':
            ring_count = geometry.GetGeometryCount()
            if ring_count > 0:
                exterior = [[x,y] for x,y in geometry.GetGeometryRef(0).GetPoints()]
                # 纠正坐标
                exterior = correct_points(exterior)
                labelme_shape = {
                    "label": str(shape_category),
                    "points": exterior,
                    "group_id": None,
                    "shape_type": "polygon",
                    "flags": {},
                }
                labelme_data["shapes"].append(labelme_shape)

                # 如果有多于一个环，则可能包含孔洞
                for i in range(1, ring_count):
                    interior = [[x,y] for x,y in geometry.GetGeometryRef(i).GetPoints()]
                    # 纠正坐标
                    interior = correct_points(interior)
                    # 可以选择忽略孔洞，或者处理它们
                    # 这里我们选择忽略孔洞
                    # labelme_data["shapes"].append({
                    #     "label": str(shape_category),
                    #     "points": interior,
                    #     "group_id": None,
                    #     "shape_type": "polygon",
                    #     "flags": {},
                    # })

    # 保存为JSON文件
    with open(labelme_output_path, "w") as f:
        json.dump(labelme_data, f, indent=2)

if __name__ == "__main__":
    main()
