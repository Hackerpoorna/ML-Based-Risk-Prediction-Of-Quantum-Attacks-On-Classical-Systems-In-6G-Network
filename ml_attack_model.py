import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("6g_simulation_dataset.csv")

# Features
X = data[["delay_ms","packet_loss_pct","throughput_mbps","jitter_ms"]]

# Target
y = data["attack_type"]

# Encode labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train/test split
X_train,X_test,y_train,y_test = train_test_split(X,y_encoded,test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train,y_train)

print("ML Model Trained Successfully")

# Example prediction
sample = [[210,18,45,16]]

prediction = model.predict(sample)

print("Predicted Attack:",encoder.inverse_transform(prediction))
