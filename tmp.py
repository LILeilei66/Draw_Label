import os

origin_path = 'E:\Draw_Label\Draw_Label-master\dataset\良性\img_origin'
label_path = 'E:\Draw_Label\Draw_Label-master\dataset\良性\img_label'

origin_list = os.listdir(origin_path)
label_list = os.listdir(label_path)
for i in label_list:
    name = i.split('.')[-2]
    name = name+'.gif'
    if name not in origin_list:
        print(name)