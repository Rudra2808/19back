import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Load dataset - update path as needed
df = pd.read_csv(r"C:\projects\current\Django-React-master (2)\Django-React-master\djangobackend\gujarat_properties_1000.csv")

# Rename columns to match your CSV if needed, e.g. floors -> total_floors
# Use these numerical columns available in your dataset:
feature_cols = [
    "area_sqft", "bedrooms", "bathrooms", "floor_number", "total_floors",
    "balcony_sqft", "parking_spaces", "amenities_score",
    "nearby_school_km", "nearby_hospital_km", "nearby_metro_km",
    "crime_rate", "air_quality_index"
]

# Extract features and target
X = df[feature_cols]
y = df["monthly_rent"]

# Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model to a file
joblib.dump(model, "rent_price_model.pkl")

# Print R^2 scores on train and test data
print("Training Score:", model.score(X_train, y_train))
print("Test Score:", model.score(X_test, y_test))
