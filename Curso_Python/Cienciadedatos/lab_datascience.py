import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("../../Cienciadedatos/data.csv")
df = df.dropna()

X = df[["age", "income"]]
y = df["buys"]

model = DecisionTreeClassifier()
model.fit(X, y)

joblib.dump(model, "model.pkl")


loaded_model = joblib.load("model.pkl")

prediction = loaded_model.predict([[29, 58000]])

print("Prediction:", prediction[0])
