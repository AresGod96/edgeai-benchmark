# Copyright (c) 2018-2021, Texas Instruments
# All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import copy
import numpy as np
import cv2
from PIL import ImageDraw


##############################################################################
class IndexArray():
    def __init__(self, index=0):
        self.index = index

    def __call__(self, input, info_dict):
        return input[self.index], info_dict


class ArgMax():
    def __init__(self, axis=-1):
        self.axis = axis

    def __call__(self, tensor, info_dict):
        if self.axis is None:
            axis = 1 if tensor.ndim == 4 else 0
        else:
            axis = self.axis
        #
        if tensor.shape[axis] > 1:
            tensor = tensor.argmax(axis=axis)
            tensor = tensor[0]
        #
        return tensor, info_dict


class Concat():
    def __init__(self, axis=-1, start_index=0, end_index=-1):
        self.axis = axis
        self.start_index = start_index
        self.end_index = end_index

    def __call__(self, tensor_list, info_dict):
        if isinstance(tensor_list, (list,tuple)):
            max_dim = 0
            for t_idx, t in enumerate(tensor_list):
                max_dim = max(max_dim, t.ndim)
            #
            for t_idx, t in enumerate(tensor_list):
                if t.ndim < max_dim:
                    tensor_list[t_idx] = t[...,np.newaxis]
                #
            #
            tensor = np.concatenate(tensor_list[self.start_index:self.end_index], axis=self.axis)
        else:
            tensor = tensor_list
        #
        return tensor, info_dict


class ShuffleList():
    def __init__(self, indices=None):
        self.indices = indices

    def __call__(self, tensor_list, info_dict):
        if self.indices is not None:
            tensor_list_orig = tensor_list
            tensor_list = []
            for ind in self.indices:
                tensor_list.append(tensor_list_orig[ind])
            #
        #
        return tensor_list, info_dict


##############################################################################
class SegmentationImageResize():
    def __call__(self, label, info_dict):
        image_shape = info_dict['data_shape']
        label = cv2.resize(label, dsize=(image_shape[1],image_shape[0]), interpolation=cv2.INTER_NEAREST)
        return label, info_dict


class SegmentationImageSave():
    def __init__(self):
        self.colors = [(r,g,b) for r in range(0,256,32) for g in range(0,256,32) for b in range(0,256,32)]

    def __call__(self, tensor, info_dict):
        data_path = info_dict['data_path']
        # img_data = info_dict['data']
        image_name = os.path.split(data_path)[-1].split('.')[0] + '.png'
        run_dir = info_dict['run_dir']
        save_dir = os.path.join(run_dir, 'outputs')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, image_name)

        # TODO: convert label to color here
        if isinstance(tensor, np.ndarray):
            # convert image to BGR
            tensor = tensor[:,:,::-1] if tensor.ndim > 2 else tensor
            cv2.imwrite(save_path, tensor)
        else:
            # add fill code here
            tensor.save(save_path)
        #
        return tensor, info_dict


##############################################################################
class DetectionResizeOnlyNormalized():
    def __call__(self, bbox, info_dict):
        img_data = info_dict['data']
        assert isinstance(img_data, np.ndarray), 'only supports np array for now'
        data_shape = info_dict['data_shape']
        data_height, data_width, _ = data_shape
        # avoid accidental overflow
        bbox = bbox.clip(-1e6, 1e6)
        # scale the detections from normalized shape (0-1) to data shape
        bbox[...,0] = (bbox[...,0]*data_width).clip(0, data_width)
        bbox[...,1] = (bbox[...,1]*data_height).clip(0, data_height)
        bbox[...,2] = (bbox[...,2]*data_width).clip(0, data_width)
        bbox[...,3] = (bbox[...,3]*data_height).clip(0, data_height)
        return bbox, info_dict


class DetectionResizePad():
    def __init__(self, resize_with_pad=False, normalized_detections=True):
        self.resize_with_pad = resize_with_pad
        self.normalized_detections = normalized_detections

    def __call__(self, bbox, info_dict):
        img_data = info_dict['data']
        assert isinstance(img_data, np.ndarray), 'only supports np array for now'
        # avoid accidental overflow
        bbox = bbox.clip(-1e6, 1e6)
        # img size without pad
        data_shape = info_dict['data_shape']
        data_height, data_width, _ = data_shape
        resize_shape = info_dict['resize_shape']
        resize_height, resize_width, _ = resize_shape
        if self.resize_with_pad:
            # account for padding
            border = info_dict['resize_border']
            left, top, right, bottom = border
            bbox[...,0] -= left
            bbox[...,1] -= top
            bbox[...,2] -= left
            bbox[...,3] -= top
            resize_height, resize_width = (resize_height - top - bottom), (resize_width - left - right)
        #
        # scale the detections from the input shape to data shape
        sh = data_height / (1.0 if self.normalized_detections else resize_height)
        sw = data_width / (1.0 if self.normalized_detections else resize_width)
        bbox[...,0] = (bbox[...,0] * sw).clip(0, data_width)
        bbox[...,1] = (bbox[...,1] * sh).clip(0, data_height)
        bbox[...,2] = (bbox[...,2] * sw).clip(0, data_width)
        bbox[...,3] = (bbox[...,3] * sh).clip(0, data_height)
        return bbox, info_dict


class DetectionFilter():
    def __init__(self, detection_thr, detection_max=None):
        self.detection_thr = detection_thr
        self.detection_max = detection_max

    def __call__(self, bbox, info_dict):
        if self.detection_thr is not None:
            bbox_score = bbox[:,5]
            bbox_selected = (bbox_score >= self.detection_thr)
            bbox = bbox[bbox_selected,...]
        #
        if self.detection_max is not None:
            bbox = sorted(bbox, key=lambda b:b[5])
            bbox = bbox[range(self.detection_max),...]
        #
        return bbox, info_dict


class DetectionFormatting():
    def __init__(self, dst_indices=(0,1,2,3), src_indices=(1,0,3,2)):
        self.src_indices = src_indices
        self.dst_indices = dst_indices

    def __call__(self, bbox, info_dict):
        bbox_copy = copy.deepcopy(bbox)
        bbox_copy[...,self.dst_indices] = bbox[...,self.src_indices]
        return bbox_copy, info_dict


DetectionXYXY2YXYX = DetectionFormatting
DetectionYXYX2XYXY = DetectionFormatting
DetectionYXHW2XYWH = DetectionFormatting


class DetectionXYXY2XYWH():
    def __call__(self, bbox, info_dict):
        w = bbox[...,2] - bbox[...,0]
        h = bbox[...,3] - bbox[...,1]
        bbox[...,2] = w
        bbox[...,3] = h
        return bbox, info_dict


class DetectionXYWH2XYXY():
    def __call__(self, bbox, info_dict):
        x2 = bbox[...,0] + bbox[...,2]
        y2 = bbox[...,1] + bbox[...,3]
        bbox[...,2] = x2
        bbox[...,3] = y2
        return bbox, info_dict


class DetectionBoxSL2BoxLS():
    def __call__(self, bbox, info_dict):
        score = bbox[...,4]
        label = bbox[...,5]
        bbox_copy = copy.deepcopy(bbox)
        bbox_copy[...,4] = label
        bbox_copy[...,5] = score
        return bbox_copy, info_dict


class DetectionImageSave():
    def __init__(self):
        self.colors = [(r,g,b) for r in range(0,256,32) for g in range(0,256,32) for b in range(0,256,32)]
        self.thickness = 2

    def __call__(self, bbox, info_dict):
        data_path = info_dict['data_path']
        img_data = info_dict['data']
        image_name = os.path.split(data_path)[-1]
        run_dir = info_dict['run_dir']
        save_dir = os.path.join(run_dir, 'outputs')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, image_name)

        img_data = copy.deepcopy(img_data)
        if isinstance(img_data, np.ndarray):
            for bbox_one in bbox:
                label = int(bbox_one[4])
                label_color = self.colors[label % len(self.colors)]
                pt1 = (int(bbox_one[0]),int(bbox_one[1]))
                pt2 = (int(bbox_one[2]),int(bbox_one[3]))
                cv2.rectangle(img_data, pt1, pt2, color=label_color, thickness=self.thickness)
            #
            cv2.imwrite(save_path, img_data[:,:,::-1])
        else:
            img_rect = ImageDraw.Draw(img_data)
            for bbox_one in bbox:
                label = int(bbox_one[4])
                label_color = self.colors[label % len(self.colors)]
                rect = (int(bbox_one[0]),int(bbox_one[1]),int(bbox_one[2]),int(bbox_one[3]))
                img_rect.rectangle(rect, outline=label_color, width=self.thickness)
            #
            img_data.save(save_path)
        #
        return bbox, info_dict



##############################################################################
class NPTensorToImage(object):
    def __init__(self, data_layout='NCHW'):
        self.data_layout = data_layout

    def __call__(self, tensor, info_dict):
        assert isinstance(tensor, np.ndarray), 'input tensor must be an array'
        if tensor.ndim >= 3 and tensor.shape[0] == 1:
            tensor = tensor[0]
        #
        if tensor.ndim==2:
            if self.data_layout=='NHWC':
                tensor = tensor[..., np.newaxis]
            else:
                tensor = tensor[np.newaxis, ...]
        assert tensor.ndim == 3, 'could not convert to image'
        tensor = np.transpose(tensor, (1,2,0)) if self.data_layout == 'NCHW' else tensor
        assert tensor.shape[2] in (1,3), 'invalid number of channels'
        return tensor, info_dict

    def __repr__(self):
        return self.__class__.__name__ + f'({self.data_layout})'