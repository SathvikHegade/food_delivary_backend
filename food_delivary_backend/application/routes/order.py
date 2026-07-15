from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.cart import Carts 
from models.order import Order
from models.order_item import OrderItem
from models.users import User 
from models.food_items import FoodItem 
from schemas.order import OrderResponse, OrderHistoryResponse
from auth.oauth2 import get_current_user

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(db: Session = Depends(get_db), current_user_email: str = Depends(get_current_user)):
    try:
        #fetch the logged in user profile
        user = db.query(User).filter(User.email == current_user_email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        #grab all items in this users cart along with current food prices
        cart_items = db.query(Carts, FoodItem).join(FoodItem, Carts.food_item_id == FoodItem.id).filter(Carts.user_id == user.id).all()
        if not cart_items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your shopping cart is empty")

        #calculate total billing amount
        grand_total_price = sum(food.price * cart.quantity for cart, food in cart_items)

        #create and stage the master record inside order_table
        new_order = Order(user_id=user.id, total_amount=grand_total_price, status="PLACED")
        db.add(new_order)
        
        db.flush()#flush() pushes changes to DB and grabs new_order.id WITHOUT committing yet

        #move individual cart rows to the order_item_table snapshot
        for cart, food in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                food_item_id=food.id,
                quantity=cart.quantity,
                price=food.price  #locks down historical price at checkout
            )
            db.add(order_item)

        #completely clear out the users temporary shopping cart records
        db.query(Carts).filter(Carts.user_id == user.id).delete()
        
        #commit item snapshotting and cart clearance simultaneously
        db.commit()
        db.refresh(new_order)

        return new_order
    
    except HTTPException:
        #pass intentional HTTPExceptions through without converting them to 500s
        db.rollback()
        raise 
        
    except Exception as e:
        #catch unexpected database errors
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your order: {str(e)}"
        )
    
@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_single_order(order_id: int, db: Session =Depends(get_db), current_user_email: str =Depends(get_current_user)):
    user =db.query(User).filter(User.email ==current_user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    order = db.query(Order).filter(Order.id ==order_id).first()
    

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        

    if order.user_id !=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this order")

    return order

@router.get("/", response_model=OrderHistoryResponse, status_code=status.HTTP_200_OK)
def get_order_history(db: Session = Depends(get_db), current_user_email: str =Depends(get_current_user)):
    user =db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


    orders =db.query(Order).filter(Order.user_id ==user.id).order_by(Order.created_at.desc()).all()

    total_orders_count =len(orders)
    

    return {
        "total_orders": total_orders_count,
        "orders": orders
    }