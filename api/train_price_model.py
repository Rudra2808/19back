import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Load dataset
df = pd.read_csv("C:\projects\current\Django-React-master (2)\Django-React-master\djangobackend\gujarat_properties.csv")

# Features & target
X = df[[
    "area_sqft", "bedrooms", "bathrooms", "floors", "balcony_sqft",
    "year_built", "parking_spaces", "amenities_score",
    "nearby_schools_km", "nearby_hospital_km", "nearby_metro_km",
    "crime_rate", "air_quality_index", "market_trend_score"
]]
y = df["price"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "price_prediction_model.pkl")

# Print scores
print("Training Score:", model.score(X_train, y_train))
print("Test Score:", model.score(X_test, y_test))
