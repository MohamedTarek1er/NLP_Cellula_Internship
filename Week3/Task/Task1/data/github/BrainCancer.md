# 🧠 Brain Tumor Classification Using EfficientNet

A deep learning–based **brain tumor MRI classification system** with an interactive **Streamlit GUI** and **explainable AI (Grad-CAM)** for model interpretability.

The model classifies brain MRI images into **four categories**:

* **Glioma**
* **Meningioma**
* **Pituitary Tumor**
* **No Tumor**
---
## Project Highlights

* EfficientNet-based CNN for high-accuracy classification
* Medical MRI image analysis
* Explainable AI using **Grad-CAM**
* Interactive **Streamlit GUI**
* Confidence scores & class probabilities
* Zoomed important tumor regions
* Trained model saved in `.h5` format

---

## Demo (GUI Features)

* Upload brain MRI image
* View predicted tumor class
* See prediction confidence
* Visualize Grad-CAM heatmap
* Inspect the most important region used by the model

---

## Dataset

The dataset consists of **brain MRI images** organized into four classes:

```
dataset/
├── glioma/
├── meningioma/
├── notumor/
└── pituitary/
```

* Image type: Brain MRI (RGB)
* Input size: **224 × 224**
* Data split:

  * Training
  * Validation
  * Testing

> The dataset is commonly used for academic and research purposes.

---

##  Data Analysis & Augmentation

Before model training, an exploratory data analysis (EDA) phase was conducted:

* Analysis of **class distribution** to detect imbalance
* Visualization of **pixel intensity distributions** for MRI images
* Inspection of sample images from each class

To improve generalization and reduce overfitting, **data augmentation** techniques were applied during training:

* Random rotations
* Zoom transformations
* Horizontal flipping

---

##  Model Architecture & Training Strategy

Multiple deep learning architectures were evaluated, including:

* ResNet
* DenseNet
* EfficientNet

Among these, **EfficientNet** achieved the best performance and was selected as the final model.

### Training Process

1. **Transfer Learning Phase**

   * Loaded EfficientNet with ImageNet pre-trained weights
   * All convolutional layers were initially **frozen**
   * Trained only the custom classification head

2. **Fine-Tuning Phase**

   * Gradually **unfroze selected top layers** of EfficientNet
   * Fine-tuned the model to better capture MRI-specific features

3. **Training Optimization**

   * Learning Rate Scheduler (adaptive learning rate reduction)
   * Early Stopping to prevent overfitting

---

##  Model Evaluation

The trained model was evaluated using multiple robust metrics:

* **Confusion Matrix** for class-wise performance analysis
* **Precision**
* **Recall**
* **F1-score**

These metrics ensure reliable assessment beyond accuracy, which is crucial for medical image classification.

---

##  Explainable AI (Grad-CAM)

To enhance clinical trust and interpretability, the system integrates **Grad-CAM**:

* Highlights regions that influenced the model decision
* Useful for medical validation
* Helps understand tumor localization

Grad-CAM is generated from the **last convolutional layer** of EfficientNet.

---

##  Streamlit Application

The project includes a fully designed **Streamlit web interface**:

### Features

* MRI image upload
* Real-time prediction
* Class probability visualization
* Grad-CAM overlay
* Zoomed tumor-focused region

---

**Required libraries:**

* tensorflow
* streamlit
* numpy
* opencv-python
* pillow

---

---

##  Results

* High classification accuracy on test data
* Reliable differentiation between tumor types
* Grad-CAM confirms focus on clinically relevant regions

---

##  Future Improvements

* Grad-CAM++ / Score-CAM
* Tumor bounding box extraction
* DICOM image support
* Multi-slice MRI analysis
* Model confidence thresholding
* Cloud deployment

---
