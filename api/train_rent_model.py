import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv(r"C:\projects\current\Django-React-master (2)\Django-React-master\djangobackend\gujarat_properties_1000.csv")

feature_cols = [
    "area_sqft", "bedrooms", "bathrooms", "floor_number", "total_floors",
    "balcony_sqft", "parking_spaces", "amenities_score",
    "nearby_school_km", "nearby_hospital_km", "nearby_metro_km",
    "crime_rate", "air_quality_index"
]

X = df[feature_cols]
y = df["monthly_rent"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

joblib.dump(model, "rent_price_model.pkl")

print("Training Score:", model.score(X_train, y_train))
print("Test Score:", model.score(X_test, y_test))
