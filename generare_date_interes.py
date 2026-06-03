from flask import Flask, jsonify, request
import numpy as np
import pandas as pd

app = Flask(__name__)

def generare_date(num_samples, defect_rate, seed):
    np.random.seed(seed)

    # Feature initialization with rounded values
    speed = np.round(np.random.uniform(1.0, 2.0, size=num_samples), 3)
    temperature = np.round(np.random.normal(loc=65, scale=5, size=num_samples), 3)
    vibration = np.round(np.random.normal(loc=0.015, scale=0.005, size=num_samples), 3)
    noise = np.round(np.random.normal(loc=55, scale=5, size=num_samples), 3)
    load = np.round(np.random.uniform(50, 100, size=num_samples), 3)

    # Generate random defects
    defect_feature = np.random.choice(
        [0, 1, 2, 3, 4, 5], 
        size=num_samples, 
        p=[1 - defect_rate] + [defect_rate / 5] * 5
    )

    # Apply defects to the corresponding features
    for i, feature in enumerate(defect_feature):
        if feature == 1:  # Speed defect
            speed[i] = max(round(speed[i] - np.random.uniform(0.5, 1.0), 2), 0.5)
        elif feature == 2:  # Temperature defect
            temperature[i] = round(temperature[i] + np.random.normal(loc=20, scale=5), 2)
        elif feature == 3:  # Vibration defect
            vibration[i] = round(vibration[i] + np.random.normal(loc=0.05, scale=0.01), 2)
        elif feature == 4:  # Noise defect
            noise[i] = round(noise[i] + np.random.normal(loc=30, scale=5), 2)
        elif feature == 5:  # Load defect
            load[i] = round(load[i] + np.random.uniform(20, 40), 2)

    # Create DataFrame
    data = pd.DataFrame({
        'Speed': speed,
        'Temperature': temperature,
        'Vibration': vibration,
        'Noise': noise,
        'Load': load,
        'Defect': defect_feature
    })

    json_data = {f"Data{i}": row for i, row in enumerate(data.to_dict(orient="records"))}

    return jsonify(json_data)


def simulare_date(defect_rate, seed):
    np.random.seed(seed)

    # Initialize features
    speed = np.round(np.random.uniform(1.0, 2.0, size=1), 3)
    temperature = np.round(np.random.normal(loc=65, scale=5, size=1), 3)
    vibration = np.round(np.random.normal(loc=0.015, scale=0.005, size=1), 3)
    noise = np.round(np.random.normal(loc=55, scale=5, size=1), 3)
    load = np.round(np.random.uniform(50, 100, size=1), 3)

    defect_feature = np.random.choice(
        [0, 1, 2, 3, 4, 5], 
        size=1, 
        p=[1 - defect_rate] + [defect_rate / 5] * 5
    )

    if defect_feature[0] == 1:  # Speed defect
        speed = np.maximum(speed - np.random.uniform(0.5, 1.0, size=1), 0.5)
    elif defect_feature[0] == 2:  # Temperature defect
        temperature += np.random.normal(loc=20, scale=5, size=1)
    elif defect_feature[0] == 3:  # Vibration defect
        vibration += np.random.normal(loc=0.05, scale=0.01, size=1)
    elif defect_feature[0] == 4:  # Noise defect
        noise += np.random.normal(loc=30, scale=5, size=1)
    elif defect_feature[0] == 5:  # Load defect
        load += np.random.uniform(20, 40, size=1)

    combined_data = np.array([speed[0], temperature[0], vibration[0], noise[0], load[0], defect_feature[0]])
    rounded_data = np.round(combined_data, 4)  # Ensure numeric array with 4 decimal places

    # Convert to JSON
    return jsonify({
        "Data0": {
            'Speed': rounded_data[0],
            'Temperature': rounded_data[1],
            'Vibration': rounded_data[2],
            'Noise': rounded_data[3],
            'Load': rounded_data[4],
            'Defect': int(rounded_data[5])
        }
    })

@app.route('/generate_data', methods=['GET'])
def generate_data():
    num_samples = request.args.get('num_samples', default=100, type=int)
    defect_rate = request.args.get('defect_rate', default=0.1, type=float)
    seed = request.args.get('seed', default=10, type=int)
    
    data_json = generare_date(num_samples, defect_rate, seed)
    return data_json

@app.route('/simulate_data', methods=['GET'])
def simulate_data():
    defect_rate = request.args.get('defect_rate', default=0.1, type=float)
    seed = request.args.get('seed', default=10, type=int)
    
    return simulare_date(defect_rate, seed)

if __name__ == '__main__':
    app.run(debug=False)