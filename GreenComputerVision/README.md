# Introduction
With the current trend in Machine Learning being to 'buy' better results by using a bigger model or more training parameters, this investigation aims to show that there is a disproportionate level of energy waste generated for the marginal improvements seen in task performance.    

<br>

# Methods and Hardware
* All models are PyTorch implementations and pretrained on ImageNet.
* Models are fine tuned on the MedMNIST pediatric pneumonia dataset.
* Recorded accuracy and AUC as model evaluation metrics.
* GPU - 1 x NVIDIA Tesla T4 (Standard_NC8as_T4_v3 (8 cores, 56 GB RAM, 352 GB disk))
* GPU performance logging completed using Azure Monitor



<br>

# Results

<br>

![EnergyConsumption](https://user-images.githubusercontent.com/80305894/152247072-ee8a1aa1-9fea-4e1e-840b-16d7e7993e2c.png)

<sup><i>The plot above shows the energy consumed by the NVIDIA T4 GPU during fine tuning of each model on the MedMNIST dataset.</i></sup>
<br>
<br>



### Performance Metrics
| **Model** | **ACC** | **AUC** | **Mean GPU Util (%)** | **Runntime (mm:ss)** | **Energy (kJ)** |
| :-------------: | :----------: |  :----------: |  :----------: |  :----------: |  :----------: | 
| DenseNet-121  | 0.85096 | 0.97189 | 93.6 | 19:59 | 82.3 |
| DenseNet-169  |  0.82051 | 0.96969 | 95.7 | 25:28 | 104.9 |
| DenseNet-201  |  0.87179 | 0.97648 | 94.8 | 33:25 | 137.7 |
| ResNet-18  |  0.84615 | 0.96704 | 82.1 | 04:57 | 20.4 |
| ResNet-50  |  0.83654 | 0.9421 | 97.6 | 20:33 | 84.7 |
| Inception-v3  |  0.87340 | 0.94472 | 92.3 | 09:06 | 37.5 |

<br>

# Discussion

<br><br>

# Resources
| **PyTorch Framework**  |
| :---------- |
| [DenseNet](https://pytorch.org/hub/pytorch_vision_densenet/)  | 
| [ResNet](https://pytorch.org/hub/pytorch_vision_resnet/)| 
| [Inception-v3](https://pytorch.org/hub/pytorch_vision_inception_v3/)|

<br>

| **Archive**  | 
| :---------- |
| [Green AI](https://arxiv.org/abs/1907.10597) |
|  [MedMNIST](https://github.com/MedMNIST/MedMNIST)  | 
| [Densely Connected Convolutional Networks](https://arxiv.org/abs/1608.06993) |
| [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385) |
| [Rethinking the Inception Architecture for Computer Vision](https://pytorch.org/hub/pytorch_vision_inception_v3/)| 


<br>
