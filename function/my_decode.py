
import numpy as np
import tensorflow as tf


class decode_reslut():
    # 获得图像的宽和高
    # 确定图像的最低分数显示
    def __init__(self, image_np, min_score):
        self.im_width = image_np.shape[0]
        self.im_height = image_np.shape[1]
        self.min_score = min_score

    def decode_box(self, predict_result):
        (boxes, scores, classes, num) = predict_result
        boxes = boxes.numpy()
        scores = scores.numpy()
        classes = classes.numpy()
        num = num.numpy()

        for i in range(num.astype(np.uint32)[0]):
            boxes[i][0] *= self.im_width
            boxes[i][2] *= self.im_width
            boxes[i][1] *= self.im_height
            boxes[i][3] *= self.im_height
            if scores[i] >= self.min_score:
                self.object_num = i
                break
        processed_scores = scores[:self.object_num]
        processed_classes = classes[:self.object_num]
        processed_boxes = boxes[:self.object_num]

        return (processed_boxes, processed_scores, processed_classes, num)