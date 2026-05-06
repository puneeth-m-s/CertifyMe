from flask import Blueprint, request, jsonify
from app import db
from app.models import Opportunity
from flask_jwt_extended import jwt_required, get_jwt_identity

opportunities_bp = Blueprint('opportunities', __name__)

@opportunities_bp.route('/', methods=['GET'])
@jwt_required()
def get_opportunities():
    admin_id = get_jwt_identity()
    opportunities = Opportunity.query.filter_by(admin_id=admin_id).all()
    result = [{'id': opp.id, 'title': opp.title, 'description': opp.description, 'created_at': opp.created_at.isoformat(), 'updated_at': opp.updated_at.isoformat()} for opp in opportunities]
    return jsonify(result), 200

@opportunities_bp.route('/', methods=['POST'])
@jwt_required()
def add_opportunity():
    admin_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({'message': 'Title and description are required'}), 400

    opportunity = Opportunity(title=title, description=description, admin_id=admin_id)
    db.session.add(opportunity)
    db.session.commit()

    return jsonify({'message': 'Opportunity added successfully', 'id': opportunity.id}), 201

@opportunities_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_opportunity(id):
    admin_id = get_jwt_identity()
    opportunity = Opportunity.query.filter_by(id=id, admin_id=admin_id).first()
    if not opportunity:
        return jsonify({'message': 'Opportunity not found'}), 404

    result = {'id': opportunity.id, 'title': opportunity.title, 'description': opportunity.description, 'created_at': opportunity.created_at.isoformat(), 'updated_at': opportunity.updated_at.isoformat()}
    return jsonify(result), 200

@opportunities_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_opportunity(id):
    admin_id = get_jwt_identity()
    opportunity = Opportunity.query.filter_by(id=id, admin_id=admin_id).first()
    if not opportunity:
        return jsonify({'message': 'Opportunity not found'}), 404

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if title:
        opportunity.title = title
    if description:
        opportunity.description = description

    db.session.commit()

    return jsonify({'message': 'Opportunity updated successfully'}), 200

@opportunities_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_opportunity(id):
    admin_id = get_jwt_identity()
    opportunity = Opportunity.query.filter_by(id=id, admin_id=admin_id).first()
    if not opportunity:
        return jsonify({'message': 'Opportunity not found'}), 404

    db.session.delete(opportunity)
    db.session.commit()

    return jsonify({'message': 'Opportunity deleted successfully'}), 200