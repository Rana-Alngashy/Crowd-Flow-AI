import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask_cors import CORS
import cv2
import os
from ultralytics import YOLO
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
CORS(app)

# Initialize YOLO model
model = YOLO("/Users/rana/runs/detect/train4/weights/best.pt")

def count_people(image_path):
    results = model(image_path)
    return sum(1 for result in results for box in result.boxes if box.cls == 0)

def count_people_in_video(video_path):
    cap = cv2.VideoCapture(video_path)
    counts = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        temp_path = "temp_frame.jpg"
        cv2.imwrite(temp_path, frame)
        counts.append(count_people(temp_path))
        os.remove(temp_path)
    cap.release()
    return int(sum(counts) / len(counts)) if counts else 0  # Ensure integer output

def detect_movement(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()

    if not ret:
        return "No movement detected (Video not readable)"

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    movement_trend = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        movement_trend.append(float(np.mean(mag)))  # Convert to Python float immediately
        prev_gray = gray

    cap.release()

    avg_flow = np.mean(movement_trend) if movement_trend else 0
    if avg_flow > 3.0:
        return "HIGH movement - Rapid crowd flow!"
    elif avg_flow > 1.5:
        return "MODERATE movement - Normal activity."
    else:
        return "LOW movement - Crowd is stagnant."

def generate_heatmap(gates):
    plt.figure(figsize=(10,6))
    gate_names = list(gates.keys())
    crowd_counts = list(gates.values())
    colors = plt.cm.viridis(np.linspace(0, 1, len(gate_names)))

    plt.bar(gate_names, crowd_counts, color=colors)
    plt.title("Crowd Distribution at Gates")
    plt.xlabel("Gates")
    plt.ylabel("Number of People")

    heatmap_path = "static/heatmap.png"
    plt.savefig(heatmap_path)
    plt.close()
    return heatmap_path

def calculate_sustainability_score(gate_data):
    crowd_size = gate_data['count']
    movement_status = gate_data['movement']
    
    # Energy factors
    ac_factor = crowd_size * 2.5
    lighting_factor = 15 if crowd_size > 30 else 10
    
    # Movement factors
    if "HIGH" in movement_status:
        escalator_factor = crowd_size * 0.8
        security_factor = crowd_size * 1.2
    elif "MODERATE" in movement_status:
        escalator_factor = crowd_size * 0.5
        security_factor = crowd_size * 1.0
    else:
        escalator_factor = crowd_size * 0.3
        security_factor = crowd_size * 0.8
    
    return {
        'score': float((ac_factor * 0.4) + (lighting_factor * 0.2) + (escalator_factor * 0.3) + (security_factor * 0.1)),
        'details': {
            'ac_usage': int(ac_factor),
            'escalator_impact': int(escalator_factor * 100),
            'security_efficiency': int(100 - (security_factor * 10))
        }
    }

@app.route("/crowd-data", methods=["POST"])
def get_crowd_data():
    if not all(f'file{i}' in request.files for i in range(1, 4)):
        return jsonify({"error": "Please upload three files"}), 400

    temp_files = []
    gates = {}
    movement_results = {}
    sustainability_metrics = {}

    try:
        for i in range(1, 4):
            file = request.files[f'file{i}']
            ext = file.filename.split('.')[-1].lower()
            temp_path = f"temp_gate{i}.{ext}"
            file.save(temp_path)
            temp_files.append(temp_path)

            if ext in ['jpg', 'jpeg']:
                count = count_people(temp_path)
                movement_status = "Static Image (No movement detected)"
            else:
                count = count_people_in_video(temp_path)
                movement_status = detect_movement(temp_path)

            gates[f"Gate {i}"] = count
            movement_results[f"Gate {i}"] = movement_status
            
            gate_data = {
                'count': count,
                'movement': movement_status
            }
            sustainability_metrics[f"Gate {i}"] = calculate_sustainability_score(gate_data)

        heatmap_path = generate_heatmap(gates)
        recommended_gate = min(gates, key=gates.get)
        green_gate = min(sustainability_metrics, key=lambda x: sustainability_metrics[x]['score'])

        return jsonify({
            "gates": gates,
            "heatmap": heatmap_path,
            "recommended_gate": recommended_gate,
            "green_gate": green_gate,
            "movement": movement_results,
            "sustainability_metrics": sustainability_metrics,
            "predictions": {
                "Gate 1": [int(gates["Gate 1"] + i) for i in range(5)],  # Ensure integers
                "Gate 2": [int(gates["Gate 2"] + i) for i in range(5)],
                "Gate 3": [int(gates["Gate 3"] + i) for i in range(5)]
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        for file in temp_files:
            if os.path.exists(file):
                os.remove(file)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/sustainability")
def sustainability():
    return render_template("sustainability.html")

@app.route("/predictions")
def predictions():
    return render_template("predictions.html")

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)