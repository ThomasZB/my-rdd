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
    return np.array(image.getdata()).reshape(im_height, im_width, 3).astype(np.int32)


def relu(x):
    return np.maximum(0, x)


def image_predict():
    # 定义相关的错误类型
    category_index = {1: {'id': 1, 'name': 'Vertical crack'},
                        2: {'id': 2, 'name': 'Transverse crack'},
                        3: {'id': 3, 'name': 'Cracked ground'},
                        4: {'id': 4, 'name': 'Pothole'},
                        5: {'id': 5, 'name': 'Cross walk blur'},
                        6: {'id': 6, 'name': 'White line blur'},
                        7: {'id': 7, 'name': 'Manhole cover'}}


    # 载入模型
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(open('.\model\\frozen_inference_graph_mobilenet.pb','rb').read())
    mobile_func = wrap_frozen_graph(graph_def, 
                                    inputs='image_tensor:0', 
                                    outputs=('detection_boxes:0', 'detection_scores:0','detection_classes:0', 'num_detections:0'))

    # 图片的预处理（进行中值滤波）
    processed_image = []
    image_path_list = [filename for filename in os.listdir('.\\save_image')]  # 获取不同方位图像的列表
    substracted = load_image_into_numpy_array('file\\test.bmp')
    # 对不同目录的图片分别进行滤波
    for image_path in image_path_list: 
        file_list = [filename for filename in os.listdir('.\\save_image\\' + image_path)]
        img_list = []
        for file in file_list:
            img = load_image_into_numpy_array('save_image\\' + image_path + '\\' + file)
            img = relu(np.subtract(img, substracted)).astype(np.uint8)
            img_list.append(img)
        last_img = np.median(img_list, axis=0).astype(np.uint8)
        processed_image.append(last_img)

    processed_image = np.array(processed_image).astype(np.uint8)

    # 模型的预测
    image_tensor = tf.convert_to_tensor(processed_image)  # 同时预测不同方向的图片
    predict_result = mobile_func(image_tensor)

    # 对输出进行解码
    result_decoded = []
    for i in range(3):
        tmp_result = (predict_result[0][i], predict_result[1][i], predict_result[2][i], predict_result[3][i])
        im_decode = decode_reslut(processed_image[i], 0.2)
        result_decoded.append(im_decode.decode_box(tmp_result))
        vis_util.visualize_boxes_and_labels_on_image_array(
            processed_image[i],
            np.squeeze(tmp_result[0]),
            np.squeeze(tmp_result[2]).astype(np.int32),  # class
            np.squeeze(tmp_result[1]),
            category_index,
            min_score_thresh=0.2,
            use_normalized_coordinates=True,
            line_thickness=8)
        im = Image.fromarray(processed_image[i])
        im.save("predict_image\\" + str(i) + ".jpg")
    return result_decoded

