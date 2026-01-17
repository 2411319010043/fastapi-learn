"""
第2章：FastAPI 基础语法
演示路由定义、路径参数、查询参数和请求体
"""

from fastapi import FastAPI

app = FastAPI(title="第2章：FastAPI 基础语法")


#======================================================
# 1. 基础路由和视图函数
#======================================================

@app.get("/")
async def root():
    """根路径，演示最简单的GET路由"""
    return{"message": "欢迎来到 FastAPI 基础语法学习！"}

@app.get("/hello")
def hello_sync():
    """同步函数示例（非async）"""
    return{"message":"这是一个同步函数"}

@app.get("/hello-async")
async def hello_async():
    """异步函数示例（async）"""
    return{"message":"这是一个异步函数"}


# =============================================================================
# 2. 路径参数演示
# =============================================================================

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """路径参数示例：自动类型转换和校验"""
    return {"item_id": item_id, "description": f"这是第{item_id}个物品"}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str):
    """多个路径参数示例"""
    return{
        "user_id": user_id,
        "item_id": item_id,
        "message": f'用户{user_id} 的物品 {item_id}'
    }

# 使用枚举限制路径参数的值，model_name 只能是这 3 个之一，其他值 → 自动 422
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """使用枚举限制路径参数"""
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "深度学习FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN 所有的图像"}
    
    return {"model_name": model_name, "message": "有一些剩余"}


# =============================================================================
# 3. 查询参数演示
# =============================================================================

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    """查询参数示例：分页"""
    return{
        "skip": skip,
        "limit": limit,
        "message": f"跳过{skip}个，限制{limit}个"
    }

from typing import Optional

@app.get("/items/{item_id}/details")
async def read_item_details(
    item_id: int,
    q: Optional[str],
    short: bool = False
):
    """混合路径参数和查询参数"""
    item = {"item_id": item_id}
    
    if q:
        item.update({"q": q})
    
    if not short:
        item.update({"description": "这是一个很长的描述，包含物品的详细信息..."})
    
    return item

# 必须查询参数
@app.get("/items/{item_id}/required")
async def read_item_required(item_id: int, needy: str):
    """必需的查询参数（没有默认值）"""
    return{"item_id": item_id, "needy": needy}


# =============================================================================
# 4. 请求体（JSON）演示
# =============================================================================

from pydantic import BaseModel

class Item(BaseModel):
    """物品数据模型"""
    name: str
    description: str | None = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    # item 参数会直接是 Item 类型实例
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return {
        "message": "物品创建成功",
        "item": item_dict
    }

# 请求体 + 路径参数 + 查询参数
