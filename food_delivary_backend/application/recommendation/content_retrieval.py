import pickle
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "content_recommender.pkl"

with open(MODEL_PATH, "rb") as file:
    model_loader = pickle.load(file)


vectorizer = model_loader["vectorizer"]
tfidf_matrix = model_loader["tfidf_matrix"]
similarity_matrix = model_loader["similarity_matrix"]
food_data = model_loader["food_data"]


# food_id = food_data.iloc[0]["id"]

def recommend_food_by_id(food_id, top_n=5)->list[dict]:
    matches = food_data[food_data["id"] == food_id]

    if matches.empty:
        return []

    food_index = matches.index[0]

    similarity_scores = list(
        enumerate(similarity_matrix[food_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove the selected food itself
    similarity_scores = [
        item for item in similarity_scores
        if item[0] != food_index
    ]

    recommendations = []

    for index, score in similarity_scores[:top_n]:
        recommendations.append({
            "food_id": int(food_data.iloc[index]["id"]),
            "name": food_data.iloc[index]["name"],
            "restaurant_id": int(food_data.iloc[index]["restaurantID"]),
            "similarity": round(float(score), 3)
        })

    return recommendations


def search_food(food_name):
    matches = food_data[food_data["name"].str.lower().str.contains(food_name.lower(), na=False)]

    if matches.empty:
        return []

    results = []

    for _, row in matches.iterrows():
        results.append({
            "food_id": int(row["id"]),
            "name": row["name"],
            "restaurant_id": int(row["restaurantID"])
        })

    return results


print("\nSearching for dosa:")

results = search_food("dosa")
for result in results:
    print(result)


print("\nRecommendations for food ID 1:")

recommendations = recommend_food_by_id(1)
for recommendation in recommendations:
    print(recommendation)

