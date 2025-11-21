# 🔌 API 使用範例

本文檔提供完整的 API 使用範例，幫助您快速上手甜點店管理系統。

## 🔐 認證

### 1. 登入取得 Token

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "emp001",
    "password": "password123"
  }'
```

**回應範例:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "emp001",
    "employee_id": 1,
    "employee_name": "張經理",
    "department": "人資"
  }
}
```

### 2. 使用 Token 訪問 API

在後續請求中加入 Authorization Header:
```bash
export TOKEN="your_access_token_here"

curl -X GET http://localhost:5000/api/hr/employees \
  -H "Authorization: Bearer $TOKEN"
```

## 👥 人資管理 (HR)

### 查詢員工列表

```bash
# 取得所有員工
curl -X GET "http://localhost:5000/api/hr/employees" \
  -H "Authorization: Bearer $TOKEN"

# 按部門篩選
curl -X GET "http://localhost:5000/api/hr/employees?department=SALES" \
  -H "Authorization: Bearer $TOKEN"

# 搜尋員工
curl -X GET "http://localhost:5000/api/hr/employees?search=張" \
  -H "Authorization: Bearer $TOKEN"
```

### 新增員工

```bash
curl -X POST http://localhost:5000/api/hr/employees \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_code": "EMP004",
    "name": "王銷售",
    "email": "sales@bakery.com",
    "phone": "0945678901",
    "department": "SALES",
    "position": "STAFF",
    "hire_date": "2024-01-15",
    "is_active": true
  }'
```

### 更新員工資料

```bash
curl -X PATCH http://localhost:5000/api/hr/employees/4 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "position": "SUPERVISOR",
    "phone": "0945678999"
  }'
```

### 新增薪資紀錄

```bash
curl -X POST http://localhost:5000/api/hr/employees/4/salaries \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "effective_date": "2024-01-01",
    "base_salary": 35000,
    "bonus": 5000,
    "deductions": 0,
    "notes": "年度調薪"
  }'
```

### 申請請假

```bash
curl -X POST http://localhost:5000/api/hr/leave-records \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 4,
    "leave_type": "ANNUAL",
    "start_date": "2024-12-25",
    "end_date": "2024-12-27",
    "days": 3,
    "reason": "年終休假"
  }'
```

### 核准請假

```bash
curl -X PATCH http://localhost:5000/api/hr/leave-records/1/approve \
  -H "Authorization: Bearer $TOKEN"
```

### 新增績效評論

```bash
curl -X POST http://localhost:5000/api/hr/employees/4/performance \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer_id": 1,
    "review_date": "2024-06-30",
    "rating": 4,
    "strengths": "銷售能力優秀，客戶滿意度高",
    "improvements": "需要加強團隊協作",
    "goals": "下半年目標業績增長 20%",
    "comments": "整體表現良好"
  }'
```

## 💰 財務管理 (Finance)

### 查詢材料庫存

```bash
# 取得所有材料
curl -X GET http://localhost:5000/api/finance/materials \
  -H "Authorization: Bearer $TOKEN"
```

### 新增材料

```bash
curl -X POST http://localhost:5000/api/finance/materials \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "MAT004",
    "name": "巧克力",
    "unit": "KG",
    "unit_price": 300.00,
    "current_stock": 20.0,
    "min_stock": 5.0,
    "supplier": "可可進口商"
  }'
```

### 查詢庫存異動紀錄

```bash
curl -X GET http://localhost:5000/api/finance/materials/1/movements \
  -H "Authorization: Bearer $TOKEN"
```

### 查詢財務交易

```bash
curl -X GET http://localhost:5000/api/finance/transactions \
  -H "Authorization: Bearer $TOKEN"
```

### 查詢損益報表（即時盈利與成本）

```bash
curl -X GET http://localhost:5000/api/finance/reports/profit-loss \
  -H "Authorization: Bearer $TOKEN"
```

**回應範例:**
```json
{
  "period": "2024-01-01 to 2024-01-31",
  "income": 150000.00,
  "expense": 80000.00,
  "material_cost": 35000.00,
  "profit": 70000.00,
  "profit_margin": 46.67
}
```

## 🛒 銷售管理 (Sales)

### 查詢客戶列表

```bash
# 所有客戶
curl -X GET http://localhost:5000/api/sales/customers \
  -H "Authorization: Bearer $TOKEN"

# 搜尋客戶
curl -X GET "http://localhost:5000/api/sales/customers?search=陳" \
  -H "Authorization: Bearer $TOKEN"

# 只顯示 VIP
curl -X GET "http://localhost:5000/api/sales/customers?is_vip=true" \
  -H "Authorization: Bearer $TOKEN"
```

### 新增客戶

```bash
curl -X POST http://localhost:5000/api/sales/customers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_code": "CUST003",
    "name": "黃先生",
    "phone": "0965432109",
    "email": "huang@example.com",
    "address": "台中市南區",
    "birthday": "1985-05-15",
    "is_vip": false
  }'
```

### 查詢訂單列表（快速查詢與排序）

```bash
# 所有訂單（按優先級排序）
curl -X GET http://localhost:5000/api/sales/orders \
  -H "Authorization: Bearer $TOKEN"

# 按狀態篩選
curl -X GET "http://localhost:5000/api/sales/orders?status=CONFIRMED" \
  -H "Authorization: Bearer $TOKEN"

# 按交付日期排序
curl -X GET "http://localhost:5000/api/sales/orders?sort_by=delivery_date" \
  -H "Authorization: Bearer $TOKEN"

# 查詢特定客戶訂單
curl -X GET "http://localhost:5000/api/sales/orders?customer_id=1" \
  -H "Authorization: Bearer $TOKEN"

# 日期範圍查詢
curl -X GET "http://localhost:5000/api/sales/orders?order_date_from=2024-01-01&order_date_to=2024-01-31" \
  -H "Authorization: Bearer $TOKEN"
```

### 查詢訂單詳情（含客戶資料與生產進度）

```bash
curl -X GET http://localhost:5000/api/sales/orders/1 \
  -H "Authorization: Bearer $TOKEN"
```

**回應範例:**
```json
{
  "id": 1,
  "order_number": "ORD20240101001",
  "customer": {
    "id": 1,
    "name": "陳小姐",
    "phone": "0987654321",
    "email": "chen@example.com"
  },
  "order_date": "2024-01-01",
  "delivery_date": "2024-01-04",
  "status": "IN_PRODUCTION",
  "priority": 2,
  "total_amount": 1100.00,
  "paid_amount": 0.00,
  "order_items": [
    {
      "id": 1,
      "recipe_id": 1,
      "quantity": 1,
      "unit_price": 500.00,
      "subtotal": 500.00
    }
  ],
  "production_progress": 65.5,
  "notes": null
}
```

### 新增訂單

```bash
curl -X POST http://localhost:5000/api/sales/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "delivery_date": "2024-12-28",
    "priority": 2,
    "notes": "聖誕節訂單",
    "order_items": [
      {
        "recipe_id": 1,
        "quantity": 2,
        "unit_price": 500.00,
        "subtotal": 1000.00,
        "special_requirements": "不要加堅果"
      },
      {
        "recipe_id": 2,
        "quantity": 1,
        "unit_price": 600.00,
        "subtotal": 600.00
      }
    ]
  }'
```

### 更新訂單優先級（排序功能）

```bash
curl -X PATCH http://localhost:5000/api/sales/orders/1/priority \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "priority": 4
  }'
```

### 更新訂單狀態

```bash
curl -X PATCH http://localhost:5000/api/sales/orders/1/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "IN_PRODUCTION"
  }'
```

### 銷售統計摘要

```bash
curl -X GET http://localhost:5000/api/sales/statistics/sales-summary \
  -H "Authorization: Bearer $TOKEN"
```

**回應範例:**
```json
{
  "monthly_revenue": 85000.00,
  "monthly_order_count": 15,
  "pending_orders": 5,
  "completed_orders": 10
}
```

## 🏭 生產管理 (Production)

### 查詢生產批次

```bash
curl -X GET http://localhost:5000/api/production/batches \
  -H "Authorization: Bearer $TOKEN"
```

### 建立生產批次

```bash
curl -X POST http://localhost:5000/api/production/batches \
  -H "Authorization: Bearer $TOKEN"
```

### 查詢每日產能

```bash
curl -X GET http://localhost:5000/api/production/daily-capacity \
  -H "Authorization: Bearer $TOKEN"
```

**回應範例:**
```json
[
  {
    "date": "2024-01-20",
    "max_cakes": 100,
    "scheduled_cakes": 45,
    "available": 55,
    "utilization": 45.0
  },
  {
    "date": "2024-01-21",
    "max_cakes": 100,
    "scheduled_cakes": 80,
    "available": 20,
    "utilization": 80.0
  }
]
```

### 完成生產項目

```bash
curl -X PATCH http://localhost:5000/api/production/items/1/complete \
  -H "Authorization: Bearer $TOKEN"
```

## 🔬 研發管理 (R&D)

### 查詢食譜列表（快速查詢）

```bash
# 所有食譜
curl -X GET http://localhost:5000/api/rd/recipes \
  -H "Authorization: Bearer $TOKEN"

# 按分類篩選
curl -X GET "http://localhost:5000/api/rd/recipes?category=CAKE" \
  -H "Authorization: Bearer $TOKEN"

# 按狀態篩選
curl -X GET "http://localhost:5000/api/rd/recipes?status=ACTIVE" \
  -H "Authorization: Bearer $TOKEN"

# 搜尋食譜
curl -X GET "http://localhost:5000/api/rd/recipes?search=巧克力" \
  -H "Authorization: Bearer $TOKEN"
```

### 查詢食譜詳情（含材料配方）

```bash
curl -X GET http://localhost:5000/api/rd/recipes/1 \
  -H "Authorization: Bearer $TOKEN"
```

**回應範例:**
```json
{
  "id": 1,
  "code": "CAKE001",
  "name": "經典巧克力蛋糕",
  "category": "蛋糕",
  "status": "使用中",
  "version": "1.0",
  "description": "濃郁巧克力風味",
  "instructions": "1. 混合乾性材料...",
  "preparation_time": 30,
  "baking_time": 45,
  "serving_size": 8,
  "difficulty_level": 3,
  "selling_price": 500.00,
  "materials": [
    {
      "id": 1,
      "name": "高筋麵粉",
      "quantity": 0.5,
      "unit": "公斤",
      "unit_price": 50.00,
      "subtotal": 25.00,
      "notes": null
    },
    {
      "id": 4,
      "name": "巧克力",
      "quantity": 0.3,
      "unit": "公斤",
      "unit_price": 300.00,
      "subtotal": 90.00,
      "notes": "使用黑巧克力"
    }
  ],
  "total_material_cost": 165.00,
  "estimated_profit": 335.00,
  "developer": {
    "id": 3,
    "name": "王研發"
  }
}
```

### 新增食譜

```bash
curl -X POST http://localhost:5000/api/rd/recipes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "CAKE003",
    "name": "檸檬塔",
    "category": "TART",
    "status": "ACTIVE",
    "version": "1.0",
    "description": "清爽檸檬風味",
    "instructions": "1. 製作塔皮\n2. 製作檸檬餡\n3. 組合烘烤",
    "preparation_time": 45,
    "baking_time": 30,
    "serving_size": 6,
    "difficulty_level": 4,
    "selling_price": 450.00,
    "materials": [
      {
        "material_id": 1,
        "quantity": 0.3,
        "notes": "用於塔皮"
      },
      {
        "material_id": 2,
        "quantity": 3,
        "notes": "用於檸檬餡"
      }
    ]
  }'
```

### 快速搜尋食譜

```bash
curl -X GET "http://localhost:5000/api/rd/recipes/search?q=巧克力" \
  -H "Authorization: Bearer $TOKEN"
```

## 📊 Python 腳本範例

### 完整工作流程範例

```python
import requests
import json

# API 基礎 URL
BASE_URL = "http://localhost:5000/api"

# 1. 登入
def login(username, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": username, "password": password}
    )
    return response.json()["access_token"]

# 2. 建立 API 客戶端
class BakeryAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def get_orders(self, status=None):
        params = {"status": status} if status else {}
        response = requests.get(
            f"{BASE_URL}/sales/orders",
            headers=self.headers,
            params=params
        )
        return response.json()
    
    def create_order(self, order_data):
        response = requests.post(
            f"{BASE_URL}/sales/orders",
            headers=self.headers,
            json=order_data
        )
        return response.json()
    
    def get_profit_loss(self):
        response = requests.get(
            f"{BASE_URL}/finance/reports/profit-loss",
            headers=self.headers
        )
        return response.json()

# 使用範例
if __name__ == "__main__":
    # 登入
    token = login("emp001", "password123")
    api = BakeryAPI(token)
    
    # 查詢待確認訂單
    pending_orders = api.get_orders(status="PENDING")
    print(f"待確認訂單數: {len(pending_orders)}")
    
    # 新增訂單
    new_order = {
        "customer_id": 1,
        "delivery_date": "2024-12-28",
        "priority": 2,
        "order_items": [
            {
                "recipe_id": 1,
                "quantity": 1,
                "unit_price": 500.00,
                "subtotal": 500.00
            }
        ]
    }
    order = api.create_order(new_order)
    print(f"訂單已建立: {order['order_number']}")
    
    # 查詢損益
    report = api.get_profit_loss()
    print(f"本月利潤: ${report['profit']:.2f}")
```

## 🔗 使用 Postman

1. 匯入 OpenAPI 規格: http://localhost:5000/openapi.json
2. 建立環境變數:
   - `base_url`: http://localhost:5000/api
   - `token`: (登入後取得的 access_token)
3. 在請求中使用 `{{base_url}}` 和 `{{token}}`

## 📱 前端整合範例 (JavaScript)

```javascript
// API 客戶端
class BakeryClient {
  constructor(baseURL = 'http://localhost:5000/api') {
    this.baseURL = baseURL;
    this.token = null;
  }

  async login(username, password) {
    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    this.token = data.access_token;
    return data;
  }

  async getOrders(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(
      `${this.baseURL}/sales/orders?${params}`,
      {
        headers: { 'Authorization': `Bearer ${this.token}` }
      }
    );
    return response.json();
  }

  async createOrder(orderData) {
    const response = await fetch(`${this.baseURL}/sales/orders`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderData)
    });
    return response.json();
  }
}

// 使用範例
const client = new BakeryClient();
await client.login('emp001', 'password123');
const orders = await client.getOrders({ status: 'PENDING' });
console.log('待處理訂單:', orders);
```

---

**提示**: 所有範例都假設服務運行在 `localhost:5000`。生產環境請替換為實際的 API URL。