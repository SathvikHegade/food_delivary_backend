from recommendation.content_retrieval import search_food, recommend_food_by_id
from models.restaurant import Restaurant
from sqlalchemy.orm import Session


def search_food_items(food_name, db):
    result = search_food(food_name)

    restaurant_ids = {
        item["restaurant_id"]
        for item in result
    }

    restaurants = (
        db.query(Restaurant)
        .filter(Restaurant.id.in_(restaurant_ids))
        .all()
    )

    restaurant_lookup = {
        restaurant.id: restaurant.name
        for restaurant in restaurants
    }

    for item in result:
        item["restaurant_name"] = restaurant_lookup.get(
            item["restaurant_id"],
            "Unknown"
        )

    return result


def get_food_recommendations(food_id: int,top_n: int,db: Session):
    result = recommend_food_by_id(food_id, top_n)

    restaurant_ids = {
        item["restaurant_id"]
        for item in result
    }

    restaurants = (
        db.query(Restaurant)
        .filter(Restaurant.id.in_(restaurant_ids))
        .all()
    )

    restaurant_lookup = {
        restaurant.id: restaurant.name
        for restaurant in restaurants
    }

    for item in result:
        item["restaurant_name"] = restaurant_lookup.get(
            item["restaurant_id"],
            "Unknown"
        )

    return result