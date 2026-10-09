# ✋ Hand Gesture Sign Language Recognition System  

This project aims to bridge the communication gap for individuals who are **non-verbal** or have **speech impairments** by enabling them to communicate using **hand gestures**.  
It recognizes **English and Arabic letters, numbers, and commonly used words**, converting them into readable text, and optionally displaying the output on an **LCD screen** or through a **mobile application**.  

---

## 📌 Project Overview  

The **Hand Gesture Sign Language Recognition System** leverages **Computer Vision, Machine Learning, IoT, and Mobile Development** to create an interactive and inclusive platform.  
The system detects hand gestures using a camera and translates them into letters or words in real-time.  

✅ Supports **Arabic and English alphabets**  
✅ Detects **digits (0–9)** and **frequently used words**  
✅ Provides multi-platform output:  
- On-screen display  
- IoT LCD screen (via Arduino)  
- Mobile application  

---

## 🎯 Goals  

- Enable communication for people who are unable to speak.  
- Support **Arabic and English sign language**.  
- Recognize not only alphabets and digits but also **commonly used words**.  
- Provide **multi-platform output** (desktop, IoT LCD, mobile app).  
- Ensure **accuracy, usability, and accessibility**.  

---

## 🛠️ Technologies & Tools Used  

### 👁️ Computer Vision  
- **MediaPipe** → Real-time hand landmark detection  
- **OpenCV** → Image processing and camera frame handling  

### 🤖 Machine Learning  
- Collected and preprocessed gesture image data  
- Trained ML models for **letters, numbers, and words**  
- Applied **data augmentation & normalization** for better generalization  

### 🌐 Internet of Things (IoT)  
- **Arduino UNO & ESP8266** → Microcontrollers for IoT connectivity  
- **LCD Display** → Show recognized gestures in real-time  
- Used **Serial & Wi-Fi communication** between ML model and hardware  

### 📱 Mobile Application  
- Mobile app allows users to:  
  - Detect gestures using the camera  
  - Convert gestures to text in real-time  
  - Enable **on-the-go communication**  

---

## ⚙️ How It Works  

1. **Hand Detection** → Camera captures real-time frames → MediaPipe detects hand & landmarks  
2. **Gesture Classification** → Extracted data passed through trained ML model  
3. **Output Display** →  
   - Text shown on desktop  
   - Sent via Wi-Fi to **Arduino LCD screen**  
   - Displayed in **mobile app**  

---

## 📂 Dataset  

Collected gesture data from:  
- Open-source **sign language datasets**  
- Custom images captured with webcam and mobile camera  

**Covers:**  
- **A–Z** (English)  
- **Arabic letters**  
- **0–9** (Numbers)  
- Frequently used words (e.g., *Hello*, *Thank you*)  

---

## ✨ Features  

- Supports **Arabic & English sign languages**  
- Works **in real-time** with device camera  
- Offline support in mobile app (depending on version)  
- **IoT integration** with LCD display output  
- **Modular system**: ML model, CV detection, IoT, and mobile app can work independently  

---

## 🚀 Installation & Usage  

### Requirements  
- Python 3.x  
- MediaPipe  
- OpenCV  
- TensorFlow / scikit-learn  
- Arduino IDE  
- Android Studio or Flutter (for mobile app)  

### Run the Detection  
```bash
python hand_gesture_recognition.py
