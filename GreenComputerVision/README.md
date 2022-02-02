# Model Cost Evaluation


## Methods and Hardware
- GPU - 1 x NVIDIA Tesla T4 (Standard_NC8as_T4_v3 (8 cores, 56 GB RAM, 352 GB disk))
- Performance logging completed using Azure Monitor
- All models are pretrained on via PyTorch on ImageNet, and then fine tuned on the MedMNIST pediatric pneumonia dataset. 



<br>

## Resources
| **PyTorch Framework**  | **Archive**  | 
| :----------: | :----------: |
| [DenseNet](https://pytorch.org/hub/pytorch_vision_densenet/)  | [Densely Connected Convolutional Networks](https://arxiv.org/abs/1608.06993) |
| [ResNet](https://pytorch.org/hub/pytorch_vision_resnet/)| [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385) |
| [Inception-v3](https://pytorch.org/hub/pytorch_vision_inception_v3/)| [Rethinking the Inception Architecture for Computer Vision](https://pytorch.org/hub/pytorch_vision_inception_v3/)| 
|  | [Green AI](https://arxiv.org/abs/1907.10597) |




## Results

| **Model** | **ACC** | **AUC** | **Mean GPU Util (%)** | **Runntime (mm:ss)** | **Energy (kJ)** |
| :-------------: | :----------: |  :----------: |  :----------: |  :----------: |  :----------: | 
| DenseNet-121  | 0.85096 | 0.97189 | 93.6 | 19:59 | 82.3 |
| DenseNet-169  |  0.82051 | 0.96969 | 95.7 | 25:28 | 104.9 |
| DenseNet-201  |  0.87179 | 0.97648 | 94.8 | 33:25 | 137.7 |
| ResNet-18  |  0.84615 | 0.96704 | 82.1 | 04:57 | 20.4 |
| ResNet-50  |  0.83654 | 0.9421 | 97.6 | 20:33 | 84.7 |
| Inception-v3  |  0.87340 | 0.94472 | 92.3 | 09:06 | 37.5 |

