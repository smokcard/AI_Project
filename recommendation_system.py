from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


FEATURE_COLUMNS = ["feature1", "feature2", "feature3"]
DATA_PATH = Path(__file__).with_name("products.csv")


def load_products():
	if DATA_PATH.exists():
		products = pd.read_csv(DATA_PATH)
	else:
		random_generator = np.random.default_rng(42)
		features = random_generator.uniform(0, 10, size=(100, 3))
		labels = np.where(features.mean(axis=1) >= 5, "recommended", "not_recommended")
		products = pd.DataFrame(features, columns=FEATURE_COLUMNS)
		products["label"] = labels

	required_columns = FEATURE_COLUMNS + ["label"]
	missing_columns = set(required_columns) - set(products.columns)
	if missing_columns:
		raise ValueError(f"Faltan columnas requeridas en products.csv: {sorted(missing_columns)}")

	return products


products = load_products()
X = products[FEATURE_COLUMNS]
y = products["label"]

X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.2, random_state=42
)

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions) * 100
print(f"Accuracy: {accuracy:.2f}%")


def recommend(product_features):
	if len(product_features) != len(FEATURE_COLUMNS):
		raise ValueError(f"Se requieren {len(FEATURE_COLUMNS)} características numéricas.")

	product = pd.DataFrame([product_features], columns=FEATURE_COLUMNS)
	return model.predict(product)[0]


if __name__ == "__main__":
	example_features = [1.0, 2.0, 3.0]
	print(f"Recommended label: {recommend(example_features)}")
