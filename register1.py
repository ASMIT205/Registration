from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
from datetime import datetime
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add other columns as needed

# Define the UserDetails model
class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)  # Unique and compulsory field
    first_name = db.Column(db.String(100), nullable=False)  # Compulsory field
    last_name = db.Column(db.String(100), nullable=False)  # Compulsory field
    date_of_birth = db.Column(db.Date)  # Optional field
    age = db.Column(db.String(3))  # Optional field
    gender = db.Column(db.String(10))   # Optional field
    marital_status = db.Column(db.String(20))  # Optional field
    alternate_mobile_number = db.Column(db.Integer)  # Optional field
    p_house_no = db.Column(db.String(50))  # Optional field
    p_locality = db.Column(db.String(100))  # Optional field
    p_pin_code = db.Column(db.String(10))  # Optional field
    p_state = db.Column(db.String(50))  # Optional field
    p_city = db.Column(db.String(50))  # Optional field
    p_district = db.Column(db.String(50))  # Optional field
    address = db.Column(db.String(255))  # Optional field
    care_giver_first_name = db.Column(db.String(100))  # Optional field
    care_giver_last_name = db.Column(db.String(100))  # Optional field
    care_giver_mobile_number = db.Column(db.Integer)  # Optional field
    care_giver_relation = db.Column(db.String(50))  # Optional field
    c_house_no = db.Column(db.String(50))  # Optional field
    c_locality = db.Column(db.String(100))  # Optional field
    c_pin_code = db.Column(db.String(10))  # Optional field
    c_state = db.Column(db.String(50))  # Optional field
    c_city = db.Column(db.String(50))  # Optional field
    c_district = db.Column(db.String(50))  # Optional field

    # Define a relationship to the User table
    user = db.relationship('User', backref=db.backref('user_details', lazy=True))

@app.route('/create_user_details', methods=['POST'])
def create_user_detail():
    data = request.json
    
    # Generate user_id
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = str(data['phone_number'])[-5:]  # Extract last 3 digits of phone number
    user_id = f"{first_name[:2]}{last_name[:2]}{phone_number}"
    
    # Convert date_of_birth string to Python date object
    date_of_birth = datetime.strptime(data.get('date_of_birth', ''), '%Y-%m-%d').date() if 'date_of_birth' in data else None
    
    new_user_detail = UserDetails(
        user_id=user_id,
        phone_number=data['phone_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=date_of_birth,
        age=data.get('age'),
        gender=data.get('gender'),
        marital_status=data.get('marital_status'),
        alternate_mobile_number=data.get('alternate_mobile_number'),
        p_house_no=data.get('p_house_no'),
        p_locality=data.get('p_locality'),
        p_pin_code=data.get('p_pin_code'),
        p_state=data.get('p_state'),
        p_city=data.get('p_city'),
        p_district=data.get('p_district'),
        address=data.get('address'),
        care_giver_first_name=data.get('care_giver_first_name'),
        care_giver_last_name=data.get('care_giver_last_name'),
        care_giver_mobile_number=data.get('care_giver_mobile_number'),
        care_giver_relation=data.get('care_giver_relation'),
        c_house_no=data.get('c_house_no'),
        c_locality=data.get('c_locality'),
        c_pin_code=data.get('c_pin_code'),
        c_state=data.get('c_state'),
        c_city=data.get('c_city'),
        c_district=data.get('c_district')
    )
    db.session.add(new_user_detail)
    db.session.commit()
    return jsonify({'message': 'User detail created successfully', 'userName': user_id}), 201

@app.route('/user_details', methods=['GET'])
def get_all_user_details():
    user_details = UserDetails.query.all()
    result = [{'id': detail.id, 'user_id': detail.user_id, 'phone_number': detail.phone_number, 'first_name': detail.first_name, 'last_name': detail.last_name} for detail in user_details]
    return jsonify(result), 200

@app.route('/user_details/<int:user_detail_id>', methods=['GET'])
def get_user_detail(user_detail_id):
    user_detail = UserDetails.query.get_or_404(user_detail_id)
    return jsonify({'id': user_detail.id, 'user_id': user_detail.user_id, 'phone_number': user_detail.phone_number, 'first_name': user_detail.first_name, 'last_name': user_detail.last_name}), 200

@app.route('/user_details/<int:user_detail_id>', methods=['PUT'])
def update_user_detail(user_detail_id):
    user_detail = UserDetails.query.get_or_404(user_detail_id)
    data = request.json
    user_detail.phone_number = data.get('phone_number', user_detail.phone_number)
    user_detail.first_name = data.get('first_name', user_detail.first_name)
    user_detail.last_name = data.get('last_name', user_detail.last_name)
    user_detail.date_of_birth = data.get('date_of_birth', user_detail.date_of_birth)
    user_detail.age = data.get('age', user_detail.age)
    user_detail.gender = data.get('gender', user_detail.gender)
    user_detail.marital_status = data.get('marital_status', user_detail.marital_status)
    user_detail.alternate_mobile_number = data.get('alternate_mobile_number', user_detail.alternate_mobile_number)
    user_detail.p_house_no = data.get('p_house_no', user_detail.p_house_no)
    user_detail.p_locality = data.get('p_locality', user_detail.p_locality)
    user_detail.p_pin_code = data.get('p_pin_code', user_detail.p_pin_code)
    user_detail.p_state = data.get('p_state', user_detail.p_state)
    user_detail.p_city = data.get('p_city', user_detail.p_city)
    user_detail.p_district = data.get('p_district', user_detail.p_district)
    user_detail.address = data.get('address', user_detail.address)
    user_detail.care_giver_first_name = data.get('care_giver_first_name', user_detail.care_giver_first_name)
    user_detail.care_giver_last_name = data.get('care_giver_last_name', user_detail.care_giver_last_name)
    user_detail.care_giver_mobile_number = data.get('care_giver_mobile_number', user_detail.care_giver_mobile_number)
    user_detail.care_giver_relation = data.get('care_giver_relation', user_detail.care_giver_relation)
    user_detail.c_house_no = data.get('c_house_no', user_detail.c_house_no)
    user_detail.c_locality = data.get('c_locality', user_detail.c_locality)
    user_detail.c_pin_code = data.get('c_pin_code', user_detail.c_pin_code)
    user_detail.c_state = data.get('c_state', user_detail.c_state)
    user_detail.c_city = data.get('c_city', user_detail.c_city)
    user_detail.c_district = data.get('c_district', user_detail.c_district)
    db.session.commit()
    return jsonify({'message': 'User detail updated successfully'}), 200

@app.route('/user_details/<int:user_detail_id>', methods=['DELETE'])
def delete_user_detail(user_detail_id):
    user_detail = UserDetails.query.get_or_404(user_detail_id)
    db.session.delete(user_detail)
    db.session.commit()
    return jsonify({'message': 'User detail deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port='8081', debug=True)

