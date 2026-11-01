from recommendation.content_retrieval import search_food, recommend_food_by_id


def search_food_items(food_name):
    return search_food(food_name)


def get_food_recommendations(food_id, top_n=5):
    return recommend_food_by_id(food_id, top_n)