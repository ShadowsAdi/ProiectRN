import numpy as np
import pandas as pd

np.random.seed(42)
num_samples = 300000
defect_rate = 0.05

speed = np.random.uniform(1.0, 2.0, size=num_samples)
temperature = np.random.normal(loc=65, scale=5, size=num_samples)
vibration = np.random.normal(loc=0.015, scale=0.005, size=num_samples) 
noise = np.random.normal(loc=55, scale=5, size=num_samples)
load = np.random.uniform(50, 100, size=num_samples)

# Introducerea defectelor
defects = np.random.choice([0, 1], size=num_samples, p=[1-defect_rate, defect_rate])

temperature[defects == 1] += np.random.normal(loc=20, scale=5, size=sum(defects))
vibration[defects == 1] += np.random.normal(loc=0.05, scale=0.01, size=sum(defects))
noise[defects == 1] += np.random.normal(loc=30, scale=5, size=sum(defects))
speed[defects == 1] = np.maximum(speed[defects == 1] - np.random.uniform(0.5, 1.0, size=sum(defects)), 0.5)
load[defects == 1] += np.random.uniform(20, 40, size=sum(defects))

data = pd.DataFrame({
    'Speed': speed,
    'Temperature': temperature,
    'Vibration': vibration,
    'Noise': noise,
    'Load': load,
    'Defect': defects
})

data.to_csv('date_interes_conveior.csv', index=False)