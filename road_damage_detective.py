import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import cv2

sys.path.append('function')

from PIL import Image
from utils import label_map_util
from utils import visualization_utils as vis_util
from my_decode import *


# 用于将tf1模型打包
def wrap_frozen_graph(graph_def, inputs, outputs):
  def _imports_graph_def():
    tf.compat.v1.import_graph_def(graph_def, name="")
  wrapped_import = tf.compat.v1.wrap_function(_imports_graph_def, [])
  import_graph = wrapped_import.graph
  return wrapped_import.prune(
      tf.nest.map_structure(import_graph.as_graph_element, inputs),
      tf.nest.map_structure(import_graph.as_graph_element, outputs))


# 用于将图像转化为numpy数组
def load_image_into_numpy_array(image_path):
    image = Image.open(image_path)
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(im_height, im_width, 3).astype(np.uint8)


# 定义相关的错误类型
category_index = {1: {'id': 1, 'name': 'ShuXiang'},
                    2: {'id': 2, 'name': 'HengXiang'},
                    3: {'id': 3, 'name': 'GuiLie'},
                    4: {'id': 4, 'name': 'Keng'},
                    5: {'id': 5, 'name': 'BanMaXian'},
                    6: {'id': 6, 'name': 'ZhongXian'},
                    7: {'id': 7, 'name': 'JinGai'}}


# 载入模型
graph_def = tf.compat.v1.GraphDef()
graph_def.ParseFromString(open('.\model\\frozen_inference_graph_mobilenet.pb','rb').read())
mobile_func = wrap_frozen_graph(graph_def, 
                                inputs='image_tensor:0', 
                                outputs=('detection_boxes:0', 'detection_scores:0','detection_classes:0', 'num_detections:0'))

# 图片的预处理（进行中值滤波）
processed_image = []
image_path_list = [filename for filename in os.listdir('.\\save_image')] # 获取不同方位图像的列表
# 对不同目录的图片分别进行滤波
for image_path in image_path_list:
    file_list = [filename for filename in os.listdir('.\\save_image\\' + image_path)]
    img_list = []
    for file in file_list:
        img = load_image_into_numpy_array('image_test/' + file)
        img_list.append(img)
    last_img = np.median(img_list, axis=0).astype(np.uint8)
    processed_image.append(last_img)

# 模型的预测

# 同时预测不同方向的图片
image_tensor = tf.convert_to_tensor(processed_image)
result = mobile_func(image_tensor).numpy()


# 对输出进行解码
result_decoded = []
for image in processed_image:

im_decode = decode_reslut(processed_image[0], 0.3)
