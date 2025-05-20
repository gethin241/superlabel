import os
import time
from tqdm import tqdm
import numpy as np
from sklearn.metrics import confusion_matrix
from PIL import Image
import xlwt

def main():
    # 设置预测结果路径和标签路径
    pred2=r'E:\superlabel\标注软件测试-道路\测试结果\标注结果\zdd_ours_label'
    label=r'E:\superlabel\标注软件测试-道路\test_data_label255'
    # 调用计算定量评估函数
    Calculation_of_quantitative_evaluation(pred2,label,num_class=2, is_val_zero=True)
        
def Calculation_of_quantitative_evaluation(pred, label, num_class=6, is_val_zero=False):
    # 设置输出目录和模型名称
    output_dir = pred
    model_name = pred.split('/')[-1]

    print('Eval data!  \n', time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))

    # 初始化混淆矩阵
    confm = np.zeros((num_class, num_class))

    # 获取预测结果目录下的所有文件
    datas = os.listdir(pred)
    for data in tqdm(datas):
        # 如果文件不是png或tif格式，则跳过
        if not data.endswith(('png','tif')):
            continue
        # 如果标签路径下没有对应的文件，则将文件名后缀改为png
        if not os.path.isfile(os.path.join(label, data)):
            data = data.replace('.tif','.png')
        # 打开标签图片
        label_img = Image.open(os.path.join(label, data))
        label_img = np.squeeze(np.array(label_img))  # [NHW] -> [HW](N=1)
        # TODO reindex
        # 将标签图片中的255改为1
        label_img[label_img==255]=1
        if len(label_img.shape) == 3:
            label_img = label_img[:,:,0]
        # 如果预测结果路径下没有对应的文件，则将文件名后缀改为tif
        if not os.path.isfile(os.path.join(pred, data)):
            data = data.replace('.png','.tif')
        # 打开预测结果图片
        predict_img = Image.open(os.path.join(pred, data))
        predict_img = np.squeeze(np.array(predict_img))
        # 将预测结果图片中的255改为1
        predict_img[predict_img==255]=1

        # 如果标签图片和预测结果图片中没有任何一个像素点被标注，则跳过
        index = (label_img >= 0) if is_val_zero else (label_img > 0)
        # print(predict_img.shape)

        if not index.any():
            continue  # if all False
        # 获取标签图片和预测结果图片中被标注的像素点
        label_img = label_img[index]
        predict_img = predict_img[index]
        
        # 计算混淆矩阵
        tmp_confm = confusion_matrix(label_img, predict_img, labels=range(num_class))
        confm += tmp_confm

    # 如果is_val_zero为False，则去掉混淆矩阵的第一行和第一列
    if not is_val_zero:
        confm = confm[1:, 1:]

    # 计算IoU
    iou = calculate_iou_cfm(confm)
    # 计算F1分数
    f1score = calculate_f1score_cfm(confm)
    # 计算每个类别的权重
    cls_weight = confm.sum(axis=1) / confm.sum()
    # 计算加权IoU
    fw_iou = np.average(iou, weights=cls_weight)
    # 计算准确率
    oa = accuracy(confm)

    # 创建Excel文件
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Evaluation Metrics')

    log_str = ''
    # 写入IoU
    sheet.write(0, 0, 'iou')
    for i, _iou in enumerate(iou):
        log_str += ('\nclass [{}], IoU: {:.4f}'.format(i if is_val_zero else i+1, _iou))
        sheet.write(1, i if is_val_zero else i+1, float(_iou))

    # 写入F1分数
    sheet.write(2, 0, 'f1score')
    for i, _f1score in enumerate(f1score):
        log_str += ('\nclass [{}], F1score: {:.4f}'.format(i if is_val_zero else i+1, _f1score))
        sheet.write(3, i if is_val_zero else i+1, float(_f1score))

    # 写入平均F1分数和平均IoU
    sheet.write(2, i+2, 'Mean F1score')
    sheet.write(3, i+2, float(np.mean(f1score)))
    sheet.write(2, i+3, 'Mean IoU')
    sheet.write(3, i+3, float(np.mean(iou)))

    log_str += ('\nMean IoU: {:.4f}'.format(np.mean(iou)))
    log_str += ('\nMean F1score: {:.4f}'.format(np.mean(f1score)))
    log_str += ('\nAccuracy: {:.2f}%'.format(oa * 100))
    log_str += ('\nKappa: {}'.format(calculate_kappa(confm)))
    log_str += ('\nFW IoU: {}'.format(fw_iou))

    print(log_str)
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    # 将结果保存到文件
    with open(os.path.join(output_dir, '{}_acc_log2.txt'.format(model_name)), 'w') as log_file:
        workbook.save(os.path.join(output_dir, '{}_acc_log2.xls'.format(model_name)))

    print('\nFinish Eval!')
    
    

def calculate_iou_cfm(cfm):
    # 计算交集
    intersection = np.diag(cfm)
    # 计算真实集合
    ground_truth_set = cfm.sum(axis=1)
    # 计算预测集合
    predicted_set = cfm.sum(axis=0)
    # 计算并集
    union = ground_truth_set + predicted_set - intersection
    # 计算IoU
    IoU = intersection / union
    return IoU

def calculate_f1score_cfm(cfm):

    # 计算每个类别的True Positives, False Positives和False Negatives
    true_positives = np.diag(cfm)
    false_positives = np.sum(cfm, axis=0) - true_positives
    false_negatives = np.sum(cfm, axis=1) - true_positives
    
    # 计算Precision和Recall
    precision = true_positives / (true_positives + false_positives + 1e-10)  # 加上1e-10防止除以零
    recall = true_positives / (true_positives + false_negatives + 1e-10)
    
    # 计算F1分数
    f1 = 2 * (precision * recall) / (precision + recall + 1e-10)
    
    return f1

def accuracy(cfm):
    # True Positives 是混淆矩阵的对角线之和
    true_positives = np.diag(cfm).sum()
    
    # 总预测数量是混淆矩阵所有元素的总和
    total_predictions = cfm.sum()
    
    # 计算准确率
    acc = true_positives / total_predictions
    
    return acc

def calculate_kappa(cfm):
    total = cfm.sum()
    pa = np.diag(cfm).sum() / total
    pe = np.sum(cfm.sum(axis=0) * cfm.sum(axis=1)) / (total ** 2)
    kappa = (pa - pe) / (1 - pe)
    return kappa

    
    
if __name__ == '__main__':
    main()
    