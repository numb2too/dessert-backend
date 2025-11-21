from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.sales_production_rd import Recipe, RecipeMaterial
from app.models.finance import Material

rd_bp = APIBlueprint('rd', __name__, tag='研發管理')

@rd_bp.get('/recipes')
@jwt_required()
def get_recipes():
    """取得食譜列表（快速查詢）"""
    from flask import request
    
    query = Recipe.query
    
    # 篩選條件
    if category := request.args.get('category'):
        query = query.filter_by(category=category)
    if status := request.args.get('status'):
        query = query.filter_by(status=status)
    if search := request.args.get('search'):
        search_pattern = f"%{search}%"
        query = query.filter(
            db.or_(
                Recipe.name.like(search_pattern),
                Recipe.code.like(search_pattern)
            )
        )
    
    recipes = query.order_by(Recipe.created_at.desc()).all()
    
    return [{
        'id': r.id,
        'code': r.code,
        'name': r.name,
        'category': r.category.value,
        'status': r.status.value,
        'version': r.version,
        'difficulty_level': r.difficulty_level,
        'preparation_time': r.preparation_time,
        'baking_time': r.baking_time,
        'selling_price': float(r.selling_price) if r.selling_price else None,
        'developer': r.developer.name if r.developer else None
    } for r in recipes]

@rd_bp.get('/recipes/<int:recipe_id>')
@jwt_required()
def get_recipe_detail(recipe_id):
    """取得食譜詳情（含材料配方）"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # 計算材料成本
    total_material_cost = sum(
        float(rm.material.unit_price) * float(rm.quantity)
        for rm in recipe.recipe_materials
    )
    
    return {
        'id': recipe.id,
        'code': recipe.code,
        'name': recipe.name,
        'category': recipe.category.value,
        'status': recipe.status.value,
        'version': recipe.version,
        'description': recipe.description,
        'instructions': recipe.instructions,
        'preparation_time': recipe.preparation_time,
        'baking_time': recipe.baking_time,
        'serving_size': recipe.serving_size,
        'difficulty_level': recipe.difficulty_level,
        'selling_price': float(recipe.selling_price) if recipe.selling_price else None,
        'materials': [{
            'id': rm.material.id,
            'name': rm.material.name,
            'quantity': float(rm.quantity),
            'unit': rm.material.unit.value,
            'unit_price': float(rm.material.unit_price),
            'subtotal': float(rm.material.unit_price) * float(rm.quantity),
            'notes': rm.notes
        } for rm in recipe.recipe_materials],
        'total_material_cost': round(total_material_cost, 2),
        'estimated_profit': round(float(recipe.selling_price) - total_material_cost, 2) if recipe.selling_price else None,
        'developer': {
            'id': recipe.developer.id,
            'name': recipe.developer.name
        } if recipe.developer else None
    }

@rd_bp.post('/recipes')
@jwt_required()
def create_recipe():
    """新增食譜"""
    from flask import request
    data = request.json
    
    recipe = Recipe(
        code=data['code'],
        name=data['name'],
        category=data['category'],
        status=data.get('status', 'DRAFT'),
        version=data.get('version', '1.0'),
        description=data.get('description'),
        instructions=data.get('instructions'),
        preparation_time=data.get('preparation_time'),
        baking_time=data.get('baking_time'),
        serving_size=data.get('serving_size'),
        difficulty_level=data.get('difficulty_level'),
        selling_price=data.get('selling_price'),
        developer_id=get_jwt_identity()
    )
    
    # 新增材料
    for mat_data in data.get('materials', []):
        recipe_material = RecipeMaterial(
            material_id=mat_data['material_id'],
            quantity=mat_data['quantity'],
            notes=mat_data.get('notes')
        )
        recipe.recipe_materials.append(recipe_material)
    
    db.session.add(recipe)
    db.session.commit()
    
    return {'id': recipe.id, 'code': recipe.code}, 201

@rd_bp.get('/recipes/search')
@jwt_required()
def search_recipes():
    """快速搜尋食譜"""
    from flask import request
    keyword = request.args.get('q', '')
    
    if not keyword:
        return []
    
    pattern = f"%{keyword}%"
    recipes = Recipe.query.filter(
        db.or_(
            Recipe.name.like(pattern),
            Recipe.code.like(pattern),
            Recipe.description.like(pattern)
        ),
        Recipe.status == 'ACTIVE'
    ).limit(20).all()
    
    return [{
        'id': r.id,
        'code': r.code,
        'name': r.name,
        'category': r.category.value,
        'selling_price': float(r.selling_price) if r.selling_price else None
    } for r in recipes]