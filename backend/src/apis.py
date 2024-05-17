from flask import Blueprint, request
from datetime import datetime
from src.models import User, Organization, Requirement
from src.schemas import RegisterRequestSchema, LoginRequestSchema, organizations_schema, organization_schema, requirement_schema, requirements_schema
from src.helpers import generate_access_token, construct_response, log
from src.decorators import validate_marshmallow_schema, jwt_required

## Blueprints ##
root_blueprint = Blueprint('root', __name__)
user_blueprint = Blueprint('users', __name__, url_prefix='/user')
organization_blueprint = Blueprint('organization', __name__, url_prefix='/organization')
requirement_blueprint = Blueprint('requirement', __name__, url_prefix='/requirement')

## Routes ##
@user_blueprint.route('/register', methods=['POST'])
@validate_marshmallow_schema(RegisterRequestSchema())
def register_user():
    try:
        data = request.get_json()
        name, email, password, is_organization = data['name'], data['email'], data['password'], data.get('is_organization', False)

        # Check if user already exists
        user = User(name=name, email=email, password=password, is_organization=is_organization)
        if user.exists():
            return construct_response('User already exists', 400)
        user.save()
        return construct_response('User registered successfully', 201, user.serialize())
    except Exception as e:
        log(e)
        return construct_response("User registration failed", 500, e)

@user_blueprint.route('/login', methods=['POST'])
@validate_marshmallow_schema(LoginRequestSchema())
def login_user():
    try:
        data = request.get_json()
        email, password = data['email'], data['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
            return construct_response('Invalid email or password', 400)
        return construct_response('Login successful', 200, {
            'access_token': generate_access_token(user.id),
            'user': user.serialize()
        })
    except Exception as e:
        log(e)
        return construct_response("Login failed", 500, e)
    
### Orgnization Routes ###

@organization_blueprint.route('/', methods=['POST'])
@validate_marshmallow_schema(organization_schema)
@jwt_required
def create_organization(user_id):
    try:
        # check of user is an organization
        if not User.query.get_or_404(user_id).is_organization:
            return construct_response('You are not authorized to create an organization', 401)
        data = request.get_json()
        new_organization = Organization(
            name=data['name'],
            description=data['description'],
            website=data.get('website'),
            phone=data.get('phone'),
            email=data['email'],
            logo=data.get('logo'),
            created_by=user_id
        )
        if new_organization.exists():
            return construct_response('Organization already exists', 400)
        new_organization.save()
        return construct_response('Organization created successfully', 201, organization_schema.dump(new_organization))
    except Exception as e:
        log(e)
        return construct_response("Organization creation failed", 500, e)

@organization_blueprint.route('/', methods=['GET'])
def get_organizations():
    try:
        created_by = request.args.get('created_by')
        if created_by:
            organizations = Organization.query.filter_by(created_by=created_by).all()
        else:
            organizations = Organization.query.all()
        return construct_response('Organizations retrieved successfully', 200, organizations_schema.dump(organizations))

    except Exception as e:
        log(e)
        return construct_response("Organization retrieval failed", 500, e)

@organization_blueprint.route('/<int:id>', methods=['PUT'])
@validate_marshmallow_schema(organization_schema)
@jwt_required
def update_organization(user_id, id):
    try:
        organization = Organization.query.get_or_404(id)
        if organization.created_by != user_id:
            return construct_response('You are not authorized to update this organization', 401)
        
        data = request.get_json()
        organization.description = data['description']
        organization.website = data.get('website')
        organization.phone = data.get('phone')
        organization.email = data['email']
        organization.logo = data.get('logo')
        organization.updated_at = datetime.utcnow()

        organization.save()

        return construct_response('Organization updated successfully', 200, organization_schema.dump(organization))
    except Exception as e:
        log(e)
        return construct_response("Organization update failed", 500, e)


### Requirement Routes ###
@requirement_blueprint.route('/', methods=['POST'])
@validate_marshmallow_schema(requirement_schema)
@jwt_required
def create_requirement():
    try:
        data = requirement_schema.load(request.get_json())
        new_requirement = Requirement(**data)
        new_requirement.save()
        return construct_response('Requirement created successfully', 201, requirement_schema.dump(new_requirement))
    except Exception as e:
        log(e)
        return construct_response("Requirement creation failed", 500, e)
    
@requirement_blueprint.route('/', methods=['GET'])
def get_requirements():
    try:
        org_id = request.args.get('organization')
        if org_id:
            requirements = Requirement.query.filter_by(organization_id=org_id).all()
        else:
            requirements = Requirement.query.all()
        return construct_response('Requirements retrieved successfully', 200, requirements_schema.dump(requirements))
    except Exception as e:
        log(e)
        return construct_response("Requirement retrieval failed", 500, e)
    
@requirement_blueprint.route('/<int:id>', methods=['PUT'])
@validate_marshmallow_schema(requirement_schema)
@jwt_required
def update_requirement(user_id, id):
    try:
        requirement = Requirement.query.get_or_404(id)
        if Organization.query.get_or_404(requirement.organization_id).created_by != user_id:
            return construct_response('You are not authorized to update this requirement', 401)
        
        data = requirement_schema.load(request.get_json())
        requirement.description = data['description']
        requirement.quantity = data['quantity']
        requirement.updated_at = datetime.utcnow()

        requirement.save()

        return construct_response('Requirement updated successfully', 200, requirement_schema.dump(requirement))
    except Exception as e:
        log(e)
        return construct_response("Requirement update failed", 500, e)
    
@requirement_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_requirement(user_id, id):
    try:
        requirement = Requirement.query.get_or_404(id)
        if Organization.query.get_or_404(requirement.organization_id).created_by != user_id:
            return construct_response('You are not authorized to delete this requirement', 401)
        
        requirement.delete()
        return construct_response('Requirement deleted successfully', 200)
    except Exception as e:
        log(e)
        return construct_response("Requirement deletion failed", 500, e)

