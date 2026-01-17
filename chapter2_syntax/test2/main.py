from fastapi import FastAPI

app=FastAPI()

'''练习1：在FastAPI应用中添加一个新GET路由，例如/square/[num}，接受整数路
径参数num，返回其平方值JSON。编写并测试该接口，验证对于非整数路径参数
FastAPI会返回错误提示。'''
@app.get("/square/{num}")
async def square(num: int):
    return {"num的平方是：": num*num}

'''练习2：为应用添加一个查询参数筛选功能。例如拓展/items/路由，增加可选查询
参数type来筛选不同类型的 item。在函数中读取type参数（带默认值为
None），返回包含该参数的结果。尝试不传和传不同type值调用接口，观察返回结果'''
@app.post("/items")
async def items(type: str | None = None):
    if type:
        return{"message": type}
    return{"message":"没传"}

'''练习3:定义一个 Pydantic 模型User，包含username(str)和email(str)字
段，并实现一个POST路由/users/，接受User请求体并返回创建的用户数据。用
正确和错误的数据测试该接口，体会FastAPI自动验证和错误响应的效果。'''
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None

@app.post("/users/")
async def users(user: User):
    return{"username":user.username, "email": user.email}