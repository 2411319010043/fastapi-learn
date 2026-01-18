## 为什么学fastapi

1. 与python生态天然契合
2. **高性能+原生异步**
3. pydantic+类型提示带来的开发效率
4. 便于做“流式”与“事件驱动”接口

# 环境安装与配置

1. 安装FastAPI和Uvicorn

   ```python
   pip install "fastapi[standard]"
   ```

2. 项目依赖管理

   ```python
   # 列出项目依赖
   pip freeze > requirements.txt
   # 一键安装全部依赖
   pip install -r requirements.txt
   ```

3. Uvicorn开发服务器7/

   ```python
   # 启动服务器
    # main:应用所在模块
    # app:FastAPI实例对象
   uvicorn main:app --reload
   ```

# FastAPI基础语法

1. 路由与视图函数

   ```python
   from fastapi import FastAPI
   
   app = FastAPI()
   
    # @app.get("/") 装饰器声明GET方法访问根路径/时，由其下方函数处理请求
   @app.get("/")
    # 路径函数read_root()返回一个字典，FastAPI自动转为JSON
   async def read_root():
       return {"message": "Hello FastAPI"}
   ```
   
    + 装饰器中的路径字符串确定URL，装饰器名称确定HTTP方法，函数名任意

2. 路径参数

   * URL路径中包含变量部分。
   * 通过在装饰器路径中使用`{参数名}`标记,并在函数参数列表中声明同名参数，即可捕获路径参数。

   ```python
    # URL路径定义了item_id为路径参数。FastAPI自动解析URL中对应位置的值，并传递给函数参数item_id.
   @app.get("/items/{item_id}")
    # 函数签名中表明了item_id为int类型，FastAPI会自动传入值做类型转换和校验。
    # 如果传入的不是有效整数，会返回422错误
   async def read_item(item_id: int):
       return {"item_id": item_id}
   ```

3. 查询参数

   * 通过URL中`?key=value`形式传递，可用于过滤，分页等。
   * FastAPI会自动将请求URL中的查询参数**按名称**匹配到函数参数

   ```python
   @app.get("/i/{item_id}")
    # q参数赋予了默认值None,所以q是可选参数。
   async def read_item(item_id: int, q: str|None = None):
       if q:
           return{"item_id": item_id, "q": q}
       return {"item_id": item_id}
   ```

   * 客户端请求可以使用`?q=xxx`来提供查询参数；如果不提供就为None。
   * FastAPI根据是否设置默认值**(包括None)**判断参数是否必须
     - 有默认值 —> 可选参数
     - 无默认值 —> 必需参数

4. 请求体(JSON)

   * 对于POST/PUT等需要请求体的操作，FastAPI借助Pydantic数据模型将JSON请求体映射为python对象进行处理。
   * 开发者定义Pydantic模型类，并在路径操作函数的参数中注解该模型类型，FastAPI自动解析请求JSON为模型实例

   ```python
   from pydantic import BaseModel
   
   class Item(BaseModel):
       name: str
       description: str | None = None
       price: float
   
   @app.post("/items/")
   async def create_item(item: Item):
       # item 参数会直接是 Item 类型实例
       return {"item_name": item.name, "price": item.price}
   ```

   * 定义了Pydantic模型`Item`基础自`BaseModel`,包含`name`、`description`、`price`三个字段，其中`description`为可选字符串。
   * 在`create_item`路由中，将函数参数声明为`Item`,FastAPI会读取请求体JSON，并按照`Item`模型自动解析数据、完成类型转换和校验。
   * 开发者可像操作普通对象一样访问`item.name`等属性。
   * **FastAPI为请求体模型提供了丰富的文档支持和验证机制：一旦为参数使用Pydantic模型，自动文档会展示请求体模型，并支持示例数据；同时，对于缺失必需字段或类型不匹配的数据，FastAPI会自动返回422错误和详细错误说明，无需手工编写验证逻辑。通过这种证明式的方式，减少了样板代码，提高了开发效率和可靠性**

# 数据模型与验证

* 在FastAPl中，数据模型主要通过Pydantic提供，用于定义请求和响应的数据结构，并自动完成验证。
* 借助Pydantic，我们可以轻松描述数据模式、设置默认值和约束条件。
* FastAPI结合Python类型提示与Pydantic，在请求进入和响应返回时执行严格的数据校验，这使得API具有健壮性和自文档化特性。

```python
class User(BaseModel):
    username: str
    password: str
    age: int | None = None  # 可选字段
```

定义好数据模型后，将其用作路径操作函数参数（请求）或返回值（响应模型）。FastAPI会将传入数据按模型字段解析，自动完成以下工作：

* **<u>数据解析与类型转换</u>**：根据模型字段类型，从JSON中读取数据并转换为对应的Python类型（如将字符串数字转换为`int`）。如果某字段缺失且无默认值，校验失败。
* **<u>数据校验</u>：**利用Pydantic的校验机制验证每个字段的类型和约束。如果请求数据有错误，例如字段类型不符、缺少必需字段等，FastAPI会返回HTTP 422错误，响应体详细列出出错字段路径和错误原因。
* <u>**模型实例注入**</u>：校验通过后，函数参数将接收到模型类的实例，开发者可以直接访问其属性（如item.name）。不需要手工解析 JSON。
* **<u>自动文档模式</u>：**FastAPI根据Pydantic模型生成**JSON Schema**，在交互式文档中展示数据模型结构和字段要求，帮助客户端了解**API**请求格式。
