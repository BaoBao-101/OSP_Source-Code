import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Read log Apache and assign lable (0: normal, 1: malicious)
LOG_FILE = "/opt/apache_log_monitor/access_log_labeled.csv"
df = pd.read_csv(LOG_FILE)

# Extraction feature from URL or Request
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['Request'])
y = df['Label']  # 0: normal, 1: malicious

# Train model Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model và vectorizer
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model has saved and train successfully!")
