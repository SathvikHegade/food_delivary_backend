from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.cart import Carts
from models.food_items import FoodItem
from schemas.cart import cartCreate, CartDisplayResponse, CartItemResponse
from auth.oauth2 import get_current_user
from models.users import User

router=APIRouter()

@router.post("/",status_code=status.HTTP_201_CREATED)
def add_to_cart(cart_item:cartCreate,db:Session=Depends(get_db),current_user_email:str=Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    food=db.query(FoodItem).filter(FoodItem.id == cart_item.food_item_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Food item with id {cart_item.food_item_id} does not exist"
        )
    
    existing_item=db.query(Carts).filter(Carts.user_id==user.id,Carts.food_item_id==cart_item.food_item_id).first()
    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return {"message":"Cart item quantity updated successfully"}
    
    new_cart_entry = Carts(
        user_id=user.id,
        food_item_id=cart_item.food_item_id,
        quantity=cart_item.quantity
    )
    db.add(new_cart_entry)
    db.commit()
    db.refresh(new_cart_entry)
    
    return {"message": "Item added to cart successfully"}

@router.get("/", response_model=CartDisplayResponse, status_code=status.HTTP_200_OK)
def view_my_cart(db: Session = Depends(get_db), current_user_email: str = Depends(get_current_user)):
    # 1. Resolve the logged-in user from token email
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or not authorized to view")


    cart_items =db.query(Carts, FoodItem).join(FoodItem, Carts.food_item_id == FoodItem.id).filter(Carts.user_id == user.id).all()

    formatted_items =[]
    grand_total_price =0.0


    for cart, food in cart_items:
        item_total_price =food.price * cart.quantity
        grand_total_price +=item_total_price
        
        item_data = {
        "food_item_id": food.id,
        "food_name": food.name,
        "price": food.price,
        "quantity": cart.quantity,
        "item_total_price": item_total_price
        }
        formatted_items.append(CartItemResponse(**item_data))

    return CartDisplayResponse(items=formatted_items, grand_total_price=grand_total_price)

@router.delete("/{food_item_id}",status_code=status.HTTP_200_OK)
def remove_from_cart(food_item_id:int,db:Session=Depends(get_db),current_user_email:str=Depends(get_current_user)):
    user=db.query(User).filter(User.email==current_user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")

    cart_item=db.query(Carts).filter(Carts.user_id==user.id,Carts.food_item_id==food_item_id).first()
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found in your shopping cart"
        )
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart successfully"}

@router.patch("/{food_item_id}/increase", status_code=status.HTTP_200_OK)
def increase_cart_quantity(food_item_id: int, db: Session = Depends(get_db), current_user_email: str = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    cart_item = db.query(Carts).filter(Carts.user_id == user.id, Carts.food_item_id == food_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in your cart")

    cart_item.quantity += 1
    db.commit()
    db.refresh(cart_item)

    food = db.query(FoodItem).filter(FoodItem.id == food_item_id).first()
    return {"food_name": food.name, "quantity": cart_item.quantity}


@router.patch("/{food_item_id}/decrease", status_code=status.HTTP_200_OK)
def decrease_cart_quantity(food_item_id: int, db: Session = Depends(get_db), current_user_email: str = Depends(get_current_user)):
    #resolve logged-in user
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #find the item in the users cart
    cart_item = db.query(Carts).filter(Carts.user_id == user.id, Carts.food_item_id == food_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in your cart")

    food = db.query(FoodItem).filter(FoodItem.id == food_item_id).first()

    #conditional evaluation logic
    if cart_item.quantity > 1:
        # Subtract 1 if there's plenty of quantity left
        cart_item.quantity -= 1
        db.commit()
        db.refresh(cart_item)
        return {"food_name": food.name, "quantity": cart_item.quantity}
    else:
        #if quantity is exactly 1, executing a decrease drops it to 0, so remove it entirely
        db.delete(cart_item)
        db.commit()
        return {"food_name": food.name, "quantity": 0, "message": "Item completely removed from cart"}