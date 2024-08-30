from fastapi import FastAPI, Body
from pydantic import BaseModel, create_model
from bson import ObjectId
from starlette.exceptions import HTTPException
from typing import Dict, Any
import sys
from datetime import timedelta
sys.path.append(".")
from app.config import settings
from app.auth.auth import create_access_token, verify_password, get_password_hash

class User(BaseModel):
    username: str
    password: str

def generate_apis(app: FastAPI, db_connector):
    user_collection = db_connector.get_collection("users")

    if settings.auth["jwt_enabled"]:
        @app.post("/signup")
        async def signup(user: User):
            try:
                existing_user = db_connector.find_one(user_collection, {"username": user.username})
                if existing_user:
                    raise HTTPException(status_code=400, detail="Username already registered")
                
                hashed_password = get_password_hash(user.password)
                user_data = {"username": user.username, "password": hashed_password}
                db_connector.insert_one(user_collection, user_data)
                return {"msg": "User created successfully"}
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

        @app.post("/login")
        async def login(user: User):
            try:
                db_user = db_connector.find_one(user_collection, {"username": user.username})
                if not db_user or not verify_password(user.password, db_user["password"]):
                    raise HTTPException(status_code=401, detail="Invalid username or password")
                
                access_token_expires = timedelta(minutes=settings.auth["access_token_expire_minutes"])
                access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
                return {"access_token": access_token, "token_type": "bearer"}
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    for model in settings.models:
        model_name = model["model_name"]
        fields = model["fields"]

        # Create a dictionary with field names and types
        model_fields: Dict[str, Any] = {k: (eval(v), ...) for k, v in fields.items()}

        # Dynamically create a Pydantic model
        pydantic_model = create_model(model_name, __module__=__name__, **model_fields)

        collection = db_connector.get_collection(model_name)

        @app.post(f"/{model_name.lower()}/")
        async def create_item(item: dict = Body(...)):
            validated_item = pydantic_model(**item)
            item_data = validated_item.dict()
            result = collection.insert_one(item_data)
            return {"id": str(result.inserted_id)}

        @app.get(f"/{model_name.lower()}/")
        async def read_items():
            items = list(collection.find())
            for item in items:
                item["_id"] = str(item["_id"])
            return items

        @app.get(f"/{model_name.lower()}/{{item_id}}")
        async def read_item(item_id: str):
            item = collection.find_one({"_id": ObjectId(item_id)})
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            item["_id"] = str(item["_id"])
            return item

        @app.put(f"/{model_name.lower()}/{{item_id}}")
        async def update_item(item_id: str, updated_item: dict = Body(...)):
            validated_item = pydantic_model(**updated_item)
            result = collection.update_one(
                {"_id": ObjectId(item_id)}, {"$set": validated_item.dict()}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Item not found")
            return {"detail": "Item updated"}

        @app.delete(f"/{model_name.lower()}/{{item_id}}")
        async def delete_item(item_id: str):
            result = collection.delete_one({"_id": ObjectId(item_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Item not found")
            return {"detail": "Item deleted"}
