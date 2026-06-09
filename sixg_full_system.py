import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# ==========================================
# 1️⃣ 6G PEAK INFRASTRUCTURE CONFIGURATION
# ==========================================

print("\n====== 6G PEAK CONFIGURATION ======")
print("5 Ultra-Dense Base Stations Deployed")
print("20 Active Mobile Users")
print("mmWave Spectrum (28 GHz assumed)")
print("Massive MIMO Enabled")
print("Target Latency < 1ms")
print("Peak Throughput Multi-Gbps (Simulated)\n")

NUM_STATIONS = 5
NUM_USERS = 20

stations = np.random.uniform(-500, 500, (NUM_STATIONS, 2))
users = np.random.uniform(-500, 500, (NUM_USERS, 2))

# ==========================================
# 2️⃣ NETWORK SLICING CONFIGURATION
# ==========================================

print("====== NETWORK SLICING ENABLED ======")

slices = {
    "eMBB": {"bandwidth": "High", "latency_target": 5},
    "URLLC": {"bandwidth": "Medium", "latency_target": 1},
    "IoT": {"bandwidth": "Low", "latency_target": 10}
}

user_slice = {}
for i in range(NUM_USERS):
    assigned = random.choice(list(slices.keys()))
    user_slice[i] = assigned

print("Slices Assigned to Users\n")

# ==========================================
# 3️⃣ GENERATE NETWORK METRICS
# ==========================================

def generate_metrics(slice_type):
    if slice_type == "eMBB":
        return [random.uniform(10,20), random.uniform(1,3), random.uniform(200,500), random.uniform(1,3)]
    elif slice_type == "URLLC":
        return [random.uniform(1,5), random.uniform(0,1), random.uniform(100,200), random.uniform(0.1,1)]
    else:
        return [random.uniform(20,40), random.uniform(2,5), random.uniform(50,100), random.uniform(2,5)]

# Features: [delay, packet_loss, throughput, jitter]

network_data = []
labels = []

for i in range(NUM_USERS):
    metrics = generate_metrics(user_slice[i])
    network_data.append(metrics)
    labels.append(0)  # normal traffic

# ==========================================
# 4️⃣ ADD SIMULATED QUANTUM ATTACK DATA
# ==========================================

print("Simulating Quantum Threat Traffic...\n")

for _ in range(10):
    attack_sample = [random.uniform(150,300),
                     random.uniform(10,25),
                     random.uniform(5,30),
                     random.uniform(10,20)]
    network_data.append(attack_sample)
    labels.append(1)  # quantum risk

X = np.array(network_data)
y = np.array(labels)

# ==========================================
# 5️⃣ MACHINE LEARNING MODEL
# ==========================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=300)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("====== ML RISK ENGINE ======")
print(f"Model Accuracy: {accuracy*100:.2f}%\n")

# ==========================================
# 6️⃣ REAL-TIME RISK PREDICTION
# ==========================================

new_sample = np.array([[220, 18, 15, 12]])
new_sample_scaled = scaler.transform(new_sample)

prediction = model.predict(new_sample_scaled)[0]
probability = model.predict_proba(new_sample_scaled)[0][1]

if prediction == 1:
    print("⚠ Quantum Attack Risk Detected")
    print(f"Confidence: {probability*100:.2f}%")
    print("Reason: High delay + packet loss + degraded throughput\n")
else:
    print("Network Safe\n")

# ==========================================
# 7️⃣ ADAPTIVE LEARNING DEMO
# ==========================================

print("Updating Model with New Threat Pattern...")

new_threat = np.array([[260, 22, 10, 15]])
new_threat_scaled = scaler.transform(new_threat)

X_train = np.vstack((X_train, new_threat_scaled))
y_train = np.append(y_train, 1)

model.fit(X_train, y_train)

print("Model Updated Successfully (Adaptive Learning Enabled)\n")

print("====== SYSTEM READY ======")
