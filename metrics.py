from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# True labels
y_true = [
    "ranking",
    "chart",
    "aggregation",
    "anomaly",
    "trend",
    "ranking",
    "chart",
    "trend",
    "aggregation",
    "anomaly"
]

# Predicted by your model
y_pred = [
    "ranking",
    "chart",
    "aggregation",
    "trend",
    "trend",
    "ranking",
    "chart",
    "trend",
    "aggregation",
    "anomaly"
]

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average="weighted")
recall = recall_score(y_true, y_pred, average="weighted")
f1 = f1_score(y_true, y_pred, average="weighted")

print("Model Performance Metrics")
print("-------------------------")
print("Accuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1 * 100, 2), "%")