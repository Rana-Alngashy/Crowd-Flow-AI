# Crowd Flow AI - "Sadeed-سديد" 

An AI-powered crowd management MVP designed for smart stadiums.  
It uses YOLOv8 for crowd detection, Optical Flow for movement tracking, and smart gate recommendations to enhance fan experience and reduce energy use.

## Features
- Real-time people detection from images/videos
- Optical flow analysis to detect crowd movement intensity
- Heatmap & predictions
  
## 📦 Model Weights

Due to GitHub file size limits, the trained YOLOv8 model (`best.pt`) is hosted externally.

👉 [Download best.pt from Google Drive](https://drive.google.com/drive/folders/1zFwnPZHso66BMuPZwQjB_kk5XpPa8P8j?usp=share_link)

After downloading, place the file inside a folder named `weights/` in your project root:

## How to Run
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Open `http://localhost:5000` in your browser

## Dataset
Used [FDST Dataset](sweetyy83/Lstn_fdst_dataset) for model training



