from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from schemas.restaurant import Restaurant_create, restaurant_update
from database import get_db
from sqlalchemy.orm import Session
from models.restaurant import Restaurant
from auth.oauth2 import get_current_user
from models.users import User
from schemas.food_items import FoodItemCreate, FoodItemResponse
from models.food_items import FoodItem
import shutil
import os
from logger import logger
import uuid
from sqlalchemy import func
from models.users import Review # Ensure this import is at the top
from schemas.restaurant import ReviewCreate
from models.order import Order
from models.order_item import OrderItem


router = APIRouter()




@router.post("",status_code=status.HTTP_201_CREATED, summary="Create a new restaurant",description="Registers a new restaurant in the system. Requires owner authentication.")
def review(loading:Restaurant_create, db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):

    # user = db.query(User).filter(User.email == current_user).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_restaurant = Restaurant(
        name=loading.name,
        location=loading.location,
        rating=0.0,
        owner_id=current_user.id # current_user is already the User object
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return {
        "message": f"Restaurant created successfully by {current_user.email}",
        "restaurant": new_restaurant
    }

@router.patch("/{restaurant_id}/image")
def upload_restaurant_image(restaurant_id:int, file:UploadFile=File(...), db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    # user = db.query(User).filter(User.email == current_user).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="restaurant not found")
        
    if restaurant.owner_id!=current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="you are not authorized to add pictures/logo to this restaurant."
        )

    #save the file locally
    allowed_extensions = {".jpg", ".jpeg", ".png"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only JPG and PNG images are allowed.")

    #generate a secure, unique filename
    secure_filename = f"{uuid.uuid4()}{file_ext}"
    upload_dir = "static/images"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, secure_filename)


    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    

    restaurant.image_url = file_path
    db.commit()
    
    return {"message": "Image uploaded successfully", "path": file_path}  


@router.get("/",summary="Get all restaurants", description="Returns a paginated list of all registered restaurants.")
def get_restaurants(db: Session = Depends(get_db), page: int = 1, limit: int = 10):
    #calculate how many items to skip
    skip=(page-1)*limit
    
    #fetch the slice of data
    restaurants = db.query(Restaurant).offset(skip).limit(limit).all()
    
    #get the total count for the frontend (optional but highly recommended)
    total_restaurants = db.query(Restaurant).count()
    
    return {
        "page": page,
        "limit": limit,
        "total": total_restaurants,
        "restaurants": restaurants
    }

@router.get("/search",summary="Search restaurants", description="Filter restaurants by name, minimum rating, or location.")
def search_restaurants(name:str=None,min_rating:float=None,location:str=None,db:Session=Depends(get_db)):
    #The .ilike() filter makes the search case-insensitive
    #%name% acts as a wildcard, finding the string anywhere in the name
    
    query = db.query(Restaurant)
    if name:
        query = query.filter(Restaurant.name.ilike(f"%{name}%"))
    if min_rating:
        query = query.filter(Restaurant.rating >= min_rating)
    if location:
        query = query.filter(Restaurant.location.ilike(f"%{location}%"))
    return query.all()
            

@router.get("/{restaurant_id}",summary="Get restaurant by ID", description="Returns details of a specific restaurant.")
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


@router.delete("/{restaurant_id}",status_code=status.HTTP_204_NO_CONTENT,summary="Delete a restaurant")
def delete_restaurant(restaurant_id: int, db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    # user = db.query(User).filter(User.email == current_user).first()

    deleteID=db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if(not deleteID ):
        raise HTTPException(status_code=404,detail="restaurant not found")
    
    if deleteID.owner_id !=current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this restaurant. You do not own it!"
        )
    
    db.delete(deleteID)
    db.commit()
    return {"message":"restaurant id="+str(restaurant_id)+" "+"deleted successfully by"+" "+str(current_user)}


@router.put("/{restaurant_id}")
def update_restaurant(restaurant_id: int,UserInput:restaurant_update,db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    # user = db.query(User).filter(User.email == current_user).first()

    UpdateRes=db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if(not UpdateRes):
        raise HTTPException(status_code=404,detail="restaurant not found")
    
    if UpdateRes.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to modify this restaurant. You do not own it!"
        )
    
    if UserInput.name is not None:
        UpdateRes.name=UserInput.name   
    if UserInput.location is not None:
        UpdateRes.location=UserInput.location
    # if UserInput.rating is not None:
    #     UpdateRes.rating=UserInput.rating

    db.commit()
    db.refresh(UpdateRes)
    return{"message": "Restaurant updated successfully", "restaurant": UpdateRes}


@router.post("/{restaurant_id}/food-items", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
def create_food_item(restaurant_id: int, food_item: FoodItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # user = db.query(User).filter(User.email == current_user).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
        

    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="restaurant not found")
        
    if restaurant.owner_id!=current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="you are not authorized to add menu items to this restaurant."
        )

    new_food_item=FoodItem(**food_item.model_dump(), restaurantID=restaurant_id)
    db.add(new_food_item)
    db.commit()
    db.refresh(new_food_item)
    
    return new_food_item


@router.get("/{restaurant_id}/food-items", response_model=List[FoodItemResponse])
def get_restaurant_menu(restaurant_id: int, db: Session = Depends(get_db)):

    restaurant=db.query(Restaurant).filter(Restaurant.id ==restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
        
    menu_items=db.query(FoodItem).filter(FoodItem.restaurantID==restaurant_id).all()
    return menu_items

@router.post("/{restaurant_id}/reviews", status_code=status.HTTP_201_CREATED)
def add_review(
    restaurant_id: int, 
    review_data: ReviewCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # 1. Verify restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # 2. Verified Purchase Check: Did they order from here?
    has_ordered = db.query(Order).join(OrderItem).join(FoodItem).filter(
        Order.user_id == current_user.id,
        FoodItem.restaurantID == restaurant_id,
        Order.status == "DELIVERED" 
    ).first()

    if not has_ordered:
        raise HTTPException(
            status_code=403, 
            detail="You must have a completed order from this restaurant to leave a review."
        )

    # 3. Create and add review
    new_review = Review(
        restaurant_id=restaurant_id, 
        user_id=current_user.id, 
        rating=review_data.rating,
        comment=review_data.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.restaurant_id == restaurant_id
    ).scalar()

    restaurant.rating = round(avg_rating or 0, 1)

    db.commit()
    db.refresh(restaurant)
    return {"message": "Review added successfully", "new_rating": restaurant.rating}