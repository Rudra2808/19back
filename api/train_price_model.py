import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv("C:\projects\current\Django-React-master (2)\Django-React-master\djangobackend\gujarat_properties.csv")

X = df[[
    "area_sqft", "bedrooms", "bathrooms", "floors", "balcony_sqft",
    "year_built", "parking_spaces", "amenities_score",
    "nearby_schools_km", "nearby_hospital_km", "nearby_metro_km",
    "crime_rate", "air_quality_index", "market_trend_score"
]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

joblib.dump(model, "price_prediction_model.pkl")

print("Training Score:", model.score(X_train, y_train))
print(r2_score(y_test))
print("Test Score:", model.score(X_test, y_test))
