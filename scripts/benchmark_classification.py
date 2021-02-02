import os
from jacinto_ai_benchmark import *

# the cwd must be the root of the respository
if os.path.split(os.getcwd())[-1] == 'scripts':
    os.chdir('../')
#
# make sure current directory is visible for python import
if not os.environ['PYTHONPATH'].startswith(':'):
    os.environ['PYTHONPATH'] = ':' + os.environ['PYTHONPATH']
#

import config_settings as settings
work_dir = os.path.join('./work_dirs', os.path.splitext(os.path.basename(__file__))[0])


################################################################################################
# configs for each model pipeline
pipeline_cfg = dict(type='accuracy',
    calibration_dataset=datasets.ImageNetCls(**settings.imagenet_train_cfg),
    input_dataset=datasets.ImageNetCls(**settings.imagenet_val_cfg),
    postprocess=settings.get_postproc_classification())

pipeline_configs = [
    #################################################################
    #       ONNX MODELS
    #################jai-devkit models##############################
    # jai-devkit: classification mobilenetv1_224x224 expected_metric: 71.82% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/pytorch-jacinto-ai-devkit/mobilenet_v1_2019-09-06_17-15-44_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    # jai-devkit: classification mobilenetv2_224x224 expected_metric: 72.13% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/pytorch-jacinto-ai-devkit/mobilenet_v2_2019-12-24_15-32-12_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    # jai-devkit: classification mobilenetv2_224x224 expected_metric: 72.13% top-1 accuracy, QAT: 71.73%
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg_qat, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/pytorch-jacinto-ai-devkit/mobilenet_v2_qat-jai_2020-12-13_16-53-07_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)}, calibrationOption=0)),
    #################pycls regnetx models#########################
    # pycls: classification regnetx200mf_224x224 expected_metric: 68.9% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(reverse_channels=True),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/pycls/RegNetX-200MF_dds_8gpu_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    # pycls: classification regnetx400mf_224x224 expected_metric: 72.7% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(reverse_channels=True),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/pycls/RegNetX-400MF_dds_8gpu_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    # pycls: classification regnetx800mf_224x224 expected_metric: 75.2% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(reverse_channels=True),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/pycls/RegNetX-800MF_dds_8gpu_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    # pycls: classification regnetx1.6gf_224x224 expected_metric: 77.0% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(reverse_channels=True),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/pycls/RegNetX-1.6GF_dds_8gpu_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    #################torchvision models#########################
    # torchvision: classification shufflenetv2_224x224 expected_metric: 69.36% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/torchvision/shufflenetv2_x1p0_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    # torchvision: classification mobilenetv2_224x224 expected_metric: 71.88% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/torchvision/mobilenetv2_tv_x1_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    # torchvision: classification mobilenetv2_224x224 expected_metric: 71.88% top-1 accuracy, QAT: 71.31%
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg_qat, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/torchvision/mobilenet_v2_tv_x1_qat-jai_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)}, calibrationOption=0)),
    # torchvision: classification resnet18_224x224 expected_metric: 69.76% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/torchvision/resnet18_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    # torchvision: classification resnet50_224x224 expected_metric: 76.15% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/torchvision/resnet50_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    # torchvision: classification vgg16_224x224 expected_metric: 71.59% top-1 accuracy - too slow inference
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tvm_dlr(),
        session=sessions.TVMDLRSession(**settings.session_tvm_dlr_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/torchvision/vgg16_opset9.onnx',
        input_shape={'input.1': (1, 3, 224, 224)})),
    #################################################################
    #       TFLITE MODELS
    #################gen-efficinetnet models#########################
    # tensorflow/tpu: classification efficinetnet-lite0_224x224 expected_metric: 75.1% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tflite_rt(),
        session=sessions.TFLiteRTSession(**settings.session_tflite_rt_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/tf_tpu/efficientnet-lite0-fp32.tflite',
        input_shape={'images': (1, 3, 224, 224)}, outDataNamesList='efficientnet-lite0/model/head/dense/BiasAdd'),
        metric=dict(label_offset_pred=-1)),
    # tensorflow/tpu: classification efficinetnet-lite2_260x260 expected_metric: 77.6% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tflite_rt(297, 260),
        session=sessions.TFLiteRTSession(**settings.session_tflite_rt_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/tf_tpu/efficientnet-lite2-fp32.tflite',
        input_shape={'images': (1, 3, 224, 260)}, outDataNamesList='efficientnet-lite2/model/head/dense/BiasAdd'),
        metric=dict(label_offset_pred=-1)),
    # tensorflow/tpu: classification efficinetnet-lite4_300x300 expected_metric: 81.5% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tflite_rt(343, 300),
        session=sessions.TFLiteRTSession(**settings.session_tflite_rt_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/tf_tpu/efficientnet-lite4-fp32.tflite',
        input_shape={'images': (1, 3, 224, 300)}, outDataNamesList='efficientnet-lite4/model/head/dense/BiasAdd'),
        metric=dict(label_offset_pred=-1)),
    # tensorflow/tpu: classification efficientnet-edgetpu-S expected_metric: 77.23% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tflite_rt(),
        session=sessions.TFLiteRTSession(**settings.session_tflite_rt_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/tf_tpu/efficientnet-edgetpu-S_float.tflite',
        input_shape={'images': (1, 3, 224, 224)}, outDataNamesList='efficientnet-edgetpu-S/model/head/dense/BiasAdd'),
        metric=dict(label_offset_pred=-1)),
    # tensorflow/tpu: classification efficientnet-edgetpu-M expected_metric: 78.69% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tflite_rt(274, 240),
        session=sessions.TFLiteRTSession(**settings.session_tflite_rt_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/tf_tpu/efficientnet-edgetpu-M_float.tflite',
        input_shape={'images': (1, 3, 224, 260)}, outDataNamesList='efficientnet-edgetpu-M/model/head/dense/BiasAdd'),
        metric=dict(label_offset_pred=-1)),
    # tensorflow/tpu: classification efficientnet-edgetpu-L expected_metric: 80.62% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tflite_rt(343, 300),
        session=sessions.TFLiteRTSession(**settings.session_tflite_rt_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/tf_tpu/efficientnet-edgetpu-L_float.tflite',
        input_shape={'images': (1, 3, 224, 300)}, outDataNamesList='efficientnet-edgetpu-L/model/head/dense/BiasAdd'),
        metric=dict(label_offset_pred=-1)),
    ##################tensorflow models#########################
    # tensorflow/models: classification mobilenetv2_224x224 expected_metric: 70.9% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tflite_rt(),
        session=sessions.TFLiteRTSession(**settings.session_tflite_rt_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/tf1_models/mobilenet_v1_float_1.0_224.tflite',
        input_shape={'input': (1, 3, 224, 224)}, outDataNamesList='MobilenetV1/Logits/Conv2d_1c_1x1/BiasAdd'),
        metric=dict(label_offset_pred=-1)),
    # tensorflow/models: classification mobilenetv2_224x224 expected_metric: 71.9% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tflite_rt(),
        session=sessions.TFLiteRTSession(**settings.session_tflite_rt_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/tf1_models/mobilenet_v2_float_1.0_224.tflite',
        input_shape={'input': (1, 3, 224, 224)}, outDataNamesList='MobilenetV2/Logits/Conv2d_1c_1x1/BiasAdd'),
        metric=dict(label_offset_pred=-1)),
    # tensorflow/models: classification mobilenetv2_224x224 expected_metric: 75.0% top-1 accuracy
    utils.dict_update(pipeline_cfg, preprocess=settings.get_preproc_tflite_rt(),
        session=sessions.TFLiteRTSession(**settings.session_tflite_rt_cfg, work_dir=work_dir,
        model_path=f'{settings.modelzoo_path}/edge/classification/imagenet1k/tf1_models/mobilenet_v2_float_1.4_224.tflite',
        input_shape={'input': (1, 3, 224, 224)}, outDataNamesList='MobilenetV2/Logits/Conv2d_1c_1x1/BiasAdd'),
        metric=dict(label_offset_pred=-1)),
]


################################################################################################
# execute each model
if __name__ == '__main__':
    pipelines.run(pipeline_configs, devices=settings.cuda_devices)
    results = pipelines.collect_results(work_dir)
    print(*results, sep='\n')


