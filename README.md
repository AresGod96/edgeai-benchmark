# Jacinto-AI-Benchmark

This repository provides a collection of scripts for various image recognition tasks such as classification, segmentation and detection. Scripts are provided for Model Import/Calibration, Inference and Accuracy benchmarking of Deep Neural Networks. This benchmarks in this repository can be run either in PC simulation mode or directly in [Jacinto 7](https://training.ti.com/jacinto7) family of SoCs, for example [TDA4VM](https://www.ti.com/product/TDA4VM). 


#### Notice
This repository is part of Jacinto-AI-DevKit, which is a collection of repositories providing Training & Quantization scripts, Model Zoo and Accuracy Benchmarks. If you have not visited the landing page of [**Jacinto-AI-Devkit**](https://github.com/TexasInstruments/jacinto-ai-devkit) please do so before attempting to use this repository.


## Introduction
Deep Neural Networks (a.k.a. DNNs or Deep Learning Models or simply models) can be run on our SoCs using RTOS SDK for Jacinto 7 (PROCESSOR-SDK-RTOS-J721E). It can be downloaded from the page for Processor SDK for Jacinto 7 TDA4x a.k.a. **[PROCESSOR-SDK-J721E](https://www.ti.com/tool/PROCESSOR-SDK-J721E)**. 

RTOS SDK for Jacinto 7 TDA4x provides TI Deep Learning Library (TIDL), which is an optimized library that can run DNNs on our SoCs. TIDL provides several familiar interfaces for model inference - such as onnxruntime, tflite_runtime, tvm/dlr - apart from its own native interface. All these runtimes that are provided as part of TIDL have extensions on top of public domain runtimes that allow us to offload model execution into our high performance C7x+MMA DSP. For more information how to obtain and use these runtimes, please go through the TIDL documentation in the RTOS SDK. The documentation of TIDL can be seen if you click on the "SDK Documentation" link in the download page for [PROCESSOR-SDK-RTOS-J721E)](https://www.ti.com/tool/download/PROCESSOR-SDK-RTOS-J721E)

Getting the correct functionality and accuracy with Deep Learning Models is not easy. Several aspects such as dataset loading, pre and post processing operations have to be matched to that of the original training framework to get meaningful functionality and accuracy. There is much difference in these operations across various popular models and much effort is required to match that functionality. **In this repository, we provide high level scripts that help to do inference and accuracy benchmarking on our platform easily, with just a few lines of Python code.** Aspects such dataset loading, pre and post processing as taken care for several popular models.

**Important Note**: This repository is being made available for experimentation, analysis and research - this is not meant for deployment in production.  We do not own the datasets that are used to train or evaluate the models used in this benchmark and some of these datasets have restrictions on how they can be used.


## Components of this repository
This repository is generic and can be used with a variety of runtimes and models supported by TIDL. This repository contains several parts:<br>
- [jai_benchmark](./jai_benchmark): Core scritps for core import/calibration, inference and accuracy benchmark scripts provided as a python package (that can be imported using: import jai_benchmark or using: from jai_benchmark import *)<br>
- [scripts](./scripts): these are the top level scripts - to import/calibrate models, to infer and do accuracy benchmark, to collect accuracy report and to package the generate artifacts.<br>


## Requirements
#### Environment
We have tested this on Ubuntu 18.04 PC with Anaconda Python 3.6. This is the recommended environment. Create a Python 3.6 environment if you don't have it and activate it.

#### Requirement: PROCESSOR-SDK-RTOS-J721E
As explained earlier, RTOS SDK for Jacinto 7 is required to run this package. Please visit the links given above to download and untar/extract the RTOS SDK on your Ubuntu desktop machine.

After extracting, follow the instructions in the RTOS package to download the dependencies required for it. Especially the following 3 steps are required:<br>
- (1) Install PSDK-RTOS dependencies - especially graphviz and gcc-arm: Change directory to **psdk_rtos/scripts** inside the extracted SDK and run **setup_psdk_rtos.sh**<br>
- (2) In the extracted SDK, change directory to tidl folder (it has the form tidl_j7_xx_xx_xx_xx). Inside the tidl folder, change directory to **ti_dl/test/tvm-dlr** and run **prepare_model_compliation_env.sh** to install TVM Deep Learning compiler, DLR Deep Learning Runtime and their dependencies. In our SDK, we have support to use TVM+DLR to offload part of the graph into the underlying TIDL backend running on the C7x+MMA DSP, while keeping the unsupported layers running on the main ARM processor. <br>
- (3) Inside the tidl folder, change directory to **ti_dl/test/tflrt** and run **prepare_model_compliation_env.sh** to install TFLite Runtime and its dependencies. In our SDK, we have support to use TFLite Runtime to offload part of the graph into the underlying TIDL backend running on the C7x+MMA DSP, while keeping the unsupported layers running on the main ARM processor.<br>

Please also read the details below for obtaining teh ModelZoo and Datasets - these are also required to do the benchmarking. 

#### Requirement: ModelZoo
DNN Models, config files and pre-imported/calibrated artifacts that are used in this benchmark are provided in another repository called **[Jacinto-AI-ModelZoo](https://git.ti.com/cgit/jacinto-ai/jacinto-ai-modelzoo/about/)**. Please see the documentation of that repository to understand how to clone it. After cloning, jacinto-ai-benchmark and jacinto-ai-modelzoo must be inside the same parent folder for the default settings to work.

Jacinto-AI-ModelZoo uses git-lfs, so please install git-lfs before cloning. After cloning, **jacinto-ai-benchmark** and **jacinto-ai-modelzoo** must be in the same parent folder. 


#### Requirement: Datasets
This benchmark code can use several datasets. In fact, the design of this code is flexible to add support for additional datasets easily.

We already have support to download several of these datasets automatically - but this may not always work because the source URLs may change. For example the ImageNet download URL has changed recently and the automatic download no longer works. 

If you start the download and interrupt it in between, the datasets may be partially downloaded and it can lead to unexpected failures. If the download of a dataset is interrupted in between, delete that dataset folder manually to start over. 

Also, the download may take several hours even with a good internet connection. 

Because of all these reasons **it is a good idea to download datasets manually (especially ImageNet) ane make it available at the expected locations.** To make the datasets manually available, they should be placed at the locations specified for each dataset - if you have the datasets stored somewhere else, create symbolic links as necessary.

The following link explains how to **[Obtain Datasets](./docs/datasets.md)** for benchmarking.


## Installation Instructions
After cloning this repository, install it as a Python package by running:
```
./setup.sh
```

Open the shell scripts that starts the actual benchmarking [run_benchmarks.sh](./run_benchmarks.sh), [tutorials](./tutorials) and see the environment variables **PSDK_BASE_PATH** and **TIDL_BASE_PATH** being defined. Change these paths appropriately to reflect what is in your PC.

Once installed, the **jai_benchmark** will be a available as a package in your Python environment. It can be imported just like any other Python package in a Python script:<br>
```
import jai_benchmark
```
or
```
from jai_benchmark import *
```


## Usage

#### Accuracy Benchmarking
Accuracy benchmark can be done by running [run_benchmarks.sh](./run_benchmarks.sh)

[run_benchmarks.sh](../run_benchmarks.sh) sets up some environment variables and then runs the benchmark code provided in [scripts/benchmark_accuracy.py](./scripts/benchmark_accuracy.py) using one of the yaml settings files.

For full fledged benchmarking on pc, you can use the yaml file [accuracy_import_infer_pc.yaml](./accuracy_import_infer_pc.yaml)

Change the yaml settings file appropriately to run on J7 EVM. [accuracy_import_for_j7.yaml](./accuracy_import_for_j7.yaml) can be used to run the import/calibration of the models on PC, but targeted for the J7 platform. This will create the imported artifacts corresponding to the models in the folder specified as work_dir in the benchmark script. 

Finally [accuracy_infer_on_j7.yaml](./accuracy_infer_on_j7.yaml) can be used when running the benchmark on the J7 EVM. This step will need the folder containing imported artifacts - so copy them over to the EVM or mount that folder via NFS.

By default, the accuracy benchmark script uses our pre-defined models and configs, provided in [examples](./examples) folder.

If you would like to use the models and configs provided in jacinto-ai-modelzoo, please change the configs_path and modelzoo_path to that location, as shown in [run_benchmarks.sh](../run_benchmarks.sh) 

If you would like to do accuracy benchmark for your own custom model, then please look at the example given in [scripts/benchmark_custom.py](./scripts/benchmark_custom.py).


#### Generate report
A CSV report containing all your benchmarking resutls can be generated by running [scripts/generate_report.py](./scripts/generate_report.py)


#### Package artifacts
The original artifacts folder contains several files that are generated during import/calibration. Only some of the files are needed for final inference. The artifacts and models can be packaged for sharing by running [scripts/package_artifacts.py](./scripts/package_artifacts.py) 


#### Custom models and configs
It is easy to benchmark your own models and configs using this repository. Please see the example provided in [scripts/benchmark_custom.py](./scripts/benchmark_custom.py)


## LICENSE
Please see the License under which this repository is made available: [LICENSE](./LICENSE)


## References
[1] **ImageNet ILSVRC Dataset**: Olga Russakovsky*, Jia Deng*, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma, Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C. Berg and Li Fei-Fei. (* = equal contribution) ImageNet Large Scale Visual Recognition Challenge. International Journal of Computer Vision, 2015. http://www.image-net.org/ <br>

[2] **COCO Dataset**: Microsoft COCO: Common Objects in Context, Tsung-Yi Lin, Michael Maire, Serge Belongie, Lubomir Bourdev, Ross Girshick, James Hays, Pietro Perona, Deva Ramanan, C. Lawrence Zitnick, Piotr Dollár, https://arxiv.org/abs/1405.0312, https://cocodataset.org/ <br>

[3] **PascalVOC Dataset**: The PASCAL Visual Object Classes (VOC) Challenge, Everingham, M., Van Gool, L., Williams, C. K. I., Winn, J. and Zisserman, A., International Journal of Computer Vision, 88(2), 303-338, 2010, http://host.robots.ox.ac.uk/pascal/VOC/ <br>

[4] **ADE20K Scene Parsing Dataset** Scene Parsing through ADE20K Dataset. Bolei Zhou, Hang Zhao, Xavier Puig, Sanja Fidler, Adela Barriuso and Antonio Torralba. Computer Vision and Pattern Recognition (CVPR), 2017. Semantic Understanding of Scenes through ADE20K Dataset. Bolei Zhou, Hang Zhao, Xavier Puig, Tete Xiao, Sanja Fidler, Adela Barriuso and Antonio Torralba. International Journal on Computer Vision (IJCV). https://groups.csail.mit.edu/vision/datasets/ADE20K/, http://sceneparsing.csail.mit.edu/ <br>

[5] **Cityscapes Dataset**: M. Cordts, M. Omran, S. Ramos, T. Rehfeld, M. Enzweiler, R. Benenson, U. Franke, S. Roth, and B. Schiele, “The Cityscapes Dataset for Semantic Urban Scene Understanding,” in Proc. of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016. https://www.cityscapes-dataset.com/ <br>

[6] **MMDetection: Open MMLab Detection Toolbox and Benchmark**, Chen, Kai and Wang, Jiaqi and Pang, Jiangmiao and Cao, Yuhang and Xiong, Yu and Li, Xiaoxiao and Sun, Shuyang and Feng, Wansen and Liu, Ziwei and Xu, Jiarui and Zhang, Zheng and Cheng, Dazhi and Zhu, Chenchen and Cheng, Tianheng and Zhao, Qijie and Li, Buyu and Lu, Xin and Zhu, Rui and Wu, Yue and Dai, Jifeng and Wang, Jingdong and Shi, Jianping and Ouyang, Wanli and Loy, Chen Change and Lin, Dahua. arXiv:1906.07155, 2019 <br>

[7] **SSD: Single Shot MultiBox Detector**, Wei Liu, Dragomir Anguelov, Dumitru Erhan, Christian Szegedy, Scott Reed, Cheng-Yang Fu, Alexander C. Berg. In the Proceedings of the European Conference on Computer Vision (ECCV), 2016. <br>

[8] **MLPerf Inference Benchmark**, Vijay Janapa Reddi and Christine Cheng and David Kanter and Peter Mattson and Guenther Schmuelling and Carole-Jean Wu and Brian Anderson and Maximilien Breughe and Mark Charlebois and William Chou and Ramesh Chukka and Cody Coleman and Sam Davis and Pan Deng and Greg Diamos and Jared Duke and Dave Fick and J. Scott Gardner and Itay Hubara and Sachin Idgunji and Thomas B. Jablin and Jeff Jiao and Tom St. John and Pankaj Kanwar and David Lee and Jeffery Liao and Anton Lokhmotov and Francisco Massa and Peng Meng and Paulius Micikevicius and Colin Osborne and Gennady Pekhimenko and Arun Tejusve Raghunath Rajan and Dilip Sequeira and Ashish Sirasao and Fei Sun and Hanlin Tang and Michael Thomson and Frank Wei and Ephrem Wu and Lingjie Xu and Koichi Yamada and Bing Yu and George Yuan and Aaron Zhong and Peizhao Zhang and Yuchen Zhou, arXiv:1911.02549, 2019 <br>

[8] **Pytorch/Torchvision**: Torchvision the machine-vision package of torch, Sébastien Marcel, Yann  Rodriguez, MM '10: Proceedings of the 18th ACM international conference on Multimedia October 2010 Pages 14851488 https://doi.org/10.1145/1873951.1874254, https://pytorch.org/vision/stable/index.html

[8] **TensorFlow Model Garden**: The TensorFlow Model Garden is a repository with a number of different implementations of state-of-the-art (SOTA) models and modeling solutions for TensorFlow users. https://github.com/tensorflow/models <br>

[9] **TensorFlow Object Detection API**: Speed/accuracy trade-offs for modern convolutional object detectors. Huang J, Rathod V, Sun C, Zhu M, Korattikara A, Fathi A, Fischer I, Wojna Z, Song Y, Guadarrama S, Murphy K, CVPR 2017, https://github.com/tensorflow/models/tree/master/research/object_detection <br>

[10] **Tensorflow DeepLab**: DeepLab: Deep Labelling for Semantic Image Segmentation https://github.com/tensorflow/models/tree/master/research/deeplab

[11] **TensorFlow Official Model Garden**, Chen Chen and Xianzhi Du and Le Hou and Jaeyoun Kim and Pengchong, Jin and Jing Li and Yeqing Li and Abdullah Rashwan and Hongkun Yu, 2020, https://github.com/tensorflow/models/tree/master/official <br>

[12] **GluonCV**: GluonCV and GluonNLP: Deep Learning in Computer Vision and Natural Language Processing
Jian Guo, He He, Tong He, Leonard Lausen, Mu Li, Haibin Lin, Xingjian Shi, Chenguang Wang, Junyuan Xie, Sheng Zha, Aston Zhang, Hang Zhang, Zhi Zhang, Zhongyue Zhang, Shuai Zheng, Yi Zhu, https://arxiv.org/abs/1907.04433

