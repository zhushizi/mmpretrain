# 深度学历 csdn：李大脑袋741
import os
import shutil
import random
import pandas as pd

# 指定数据集路径
dataset_path = './dataset/tongue_fur_color'
dataset_name = dataset_path.split('/')[-1]
print('数据集:', dataset_name)

# 获取类别文件夹
classes = os.listdir(dataset_path)
if not classes:
    print("错误：数据集为空或路径错误。")
    exit()

# 创建 train、val、test 文件夹
for folder in ['train', 'val', 'test']:
    folder_path = os.path.join(dataset_path, folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

# 在 train、val、test 文件夹中为每个类别创建子文件夹
for defect in classes:
    for folder in ['train', 'val', 'test']:
        defect_folder_path = os.path.join(dataset_path, folder, defect)
        os.makedirs(defect_folder_path, exist_ok=True)

# 设置验证集和测试集比例
val_frac = 0.3
test_frac = 0.1
random.seed(123)  # 固定随机种子，确保结果一致

# 初始化统计数据框
df = pd.DataFrame(columns=['class', 'trainset', 'testset', 'valset'])

# 输出数据集统计
print('{:^18} {:^18} {:^18} {:^18}'.format('类别', '训练集数据个数', '测试集数据个数', '验证集数据个数'))

# 遍历每个类别
for defect in classes:
    old_dir = os.path.join(dataset_path, defect)
    images_filename = os.listdir(old_dir)
    random.shuffle(images_filename)

    # 计算各集数据个数
    total_count = len(images_filename)
    testset_num = int(total_count * test_frac)
    valset_num = int(total_count * val_frac)
    trainset_num = total_count - testset_num - valset_num

    # 分配数据集
    testset_images = images_filename[:testset_num]
    valset_images = images_filename[testset_num:testset_num + valset_num]
    trainset_images = images_filename[testset_num + valset_num:]

    # 移动图像至相应文件夹
    for image, folder in zip([testset_images, valset_images, trainset_images], ['test', 'val', 'train']):
        for img in image:
            shutil.move(
                os.path.join(dataset_path, defect, img),
                os.path.join(dataset_path, folder, defect, img)
            )

    # 删除旧文件夹
    if not os.listdir(old_dir):
        shutil.rmtree(old_dir)

    # 输出各类别的统计数据
    print(f"{defect:^18} {trainset_num:^18} {testset_num:^18} {valset_num:^18}")

    # 保存至数据框
    df = pd.concat([df, pd.DataFrame({
        'class': [defect],
        'trainset': [trainset_num],
        'testset': [testset_num],
        'valset': [valset_num]
    })], ignore_index=True)

# 重命名数据集文件夹
new_dataset_path = dataset_name + 'new'
if not os.path.exists(new_dataset_path):
    shutil.move(dataset_path, new_dataset_path)

# 保存数据统计信息至 csv 文件
df['total'] = df['trainset'] + df['testset'] + df['valset']
df.to_csv('数据量统计.csv', index=False)