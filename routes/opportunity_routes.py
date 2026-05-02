from flask import Blueprint, request, session, jsonify
from models import Opportunity
from extensions import db

opp_bp = Blueprint('opp', __name__)

# ===================== GET ALL =====================
@opp_bp.route('/opportunities', methods=['GET'])
def get_opportunities():
    admin_id = session.get('admin_id')

    if not admin_id:
        return {"error": "Unauthorized"}, 401

    opportunities = Opportunity.query.filter_by(admin_id=admin_id).all()

    return [{
        "id": o.id,
        "name": o.name,
        "category": o.category,
        "duration": o.duration,
        "start_date": o.start_date,
        "description": o.description,
        "skills": o.skills,
        "future_opportunities": o.future_opportunities,
        "max_applicants": o.max_applicants
    } for o in opportunities]


# ===================== ADD =====================
@opp_bp.route('/opportunities', methods=['POST'])
def add_opportunity():
    data = request.json
    admin_id = session.get('admin_id')

    if not admin_id:
        return {"error": "Unauthorized"}, 401

    required_fields = [
        "name",
        "duration",
        "start_date",
        "description",
        "skills",
        "category",
        "future_opportunities"
    ]

    if not all(data.get(field) for field in required_fields):
        return {"error": "All required fields must be filled"}, 400

    # ✅ FIX skills (string/list safe)
    skills = data.get('skills')
    if isinstance(skills, list):
        skills = ",".join(skills)

    new_opportunity = Opportunity(
        name=data['name'],
        duration=data['duration'],
        start_date=data['start_date'],
        description=data['description'],
        skills=skills,
        category=data['category'],
        future_opportunities=data['future_opportunities'],
        max_applicants=data.get('max_applicants'),
        admin_id=admin_id   # ✅ IMPORTANT FIX
    )

    db.session.add(new_opportunity)
    db.session.commit()

    return {"message": "Created successfully"}, 201


# ===================== VIEW ONE =====================
@opp_bp.route('/opportunities/<int:id>', methods=['GET'])
def get_one(id):
    admin_id = session.get('admin_id')

    if not admin_id:
        return {"error": "Unauthorized"}, 401

    o = Opportunity.query.filter_by(id=id, admin_id=admin_id).first()

    if not o:
        return {"error": "Not found"}, 404

    return {
        "id": o.id,
        "name": o.name,
        "duration": o.duration,
        "start_date": o.start_date,
        "description": o.description,
        "skills": o.skills,
        "category": o.category,
        "future_opportunities": o.future_opportunities,
        "max_applicants": o.max_applicants
    }


# ===================== UPDATE =====================
@opp_bp.route('/opportunities/<int:id>', methods=['PUT'])
def update(id):
    data = request.json
    admin_id = session.get('admin_id')

    if not admin_id:
        return {"error": "Unauthorized"}, 401

    o = Opportunity.query.filter_by(id=id, admin_id=admin_id).first()

    if not o:
        return {"error": "Not found"}, 404

    # ✅ Update safely (your logic but controlled)
    o.name = data.get('name', o.name)
    o.duration = data.get('duration', o.duration)
    o.start_date = data.get('start_date', o.start_date)
    o.description = data.get('description', o.description)

    skills = data.get('skills', o.skills)
    if isinstance(skills, list):
        skills = ",".join(skills)
    o.skills = skills

    o.category = data.get('category', o.category)
    o.future_opportunities = data.get('future_opportunities', o.future_opportunities)
    o.max_applicants = data.get('max_applicants', o.max_applicants)

    db.session.commit()

    return {"message": "Updated successfully"}


# ===================== DELETE =====================
@opp_bp.route('/opportunities/<int:id>', methods=['DELETE'])
def delete(id):
    admin_id = session.get('admin_id')

    if not admin_id:
        return {"error": "Unauthorized"}, 401

    o = Opportunity.query.filter_by(id=id, admin_id=admin_id).first()

    if not o:
        return {"error": "Not found"}, 404

    db.session.delete(o)
    db.session.commit()

    return {"message": "Deleted successfully"}