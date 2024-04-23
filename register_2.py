from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import UniqueConstraint
import re
import qrcode
from google.cloud import storage 
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model

# Define the Doctor model
def calculate_age(birth_date):
    # Get the current date
    current_date = datetime.now()
    
    # Calculate the difference between current date and birth date
    age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    
    return age   

#def QR_GENERATOR(doctor_id):
    #myqr = qrcode.make(doctor_id)
    #myqr.save(f'QR/{doctor_id}.png')
    #unique_file_path_name = f'QR/{doctor_id}.png'
    #upload_to_bucket(unique_file_path_name,unique_file_path_name,'extraction_medi')



def QR_GENERATOR(doctor_id,full_name,name_of_hospital):
    data ={
            "doctor_id":doctor_id,
            "full_name":full_name,
            "name_of_hospital": name_of_hospital
    }
    json_data = json.dumps(data)
    #myqr = qrcode.make(doctor_id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json_data)
    qr.make(fit=True)
    #qr.save(f'QR/{doctor_id}.png')
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image
    unique_file_path_name = f'QR/{doctor_id}.png'
    img.save(unique_file_path_name)
    
    upload_to_bucket(unique_file_path_name,unique_file_path_name,'extraction_medi')

storage_client = storage.Client.from_service_account_json('project1-419908-856d7a3f35c7.json')

my_bucket = storage_client.get_bucket('extraction_medi')

def upload_to_bucket(blob_name,file_path,bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False
    

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False) 
    date_of_birth = db.Column(db.Date,nullable=False) 
    age = db.Column(db.Integer, nullable=False) 
    #personal _qualification
    First_qualification = db.Column(db.String(10),nullable=False)
    year_of_passing = db.Column(db.Integer, nullable=False)

    gender = db.Column(db.String(10),nullable=False)
    name_of_hospital = db.Column(db.String(100),nullable=False )
    Designation = db.Column(db.String(10),nullable=False)
    medical_council_member = db.Column(db.Integer,nullable=False)
    certificate = db.Column(db.String(255),nullable=False)
    speciality = db.Column(db.String(10),nullable=False)
    About_the_doctor = db.Column(db.String(255))
    patients = db.relationship('UserDetails', secondary='doctor_patient_association', backref=db.backref('doctors', lazy='dynamic'))

# class NewTable(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
    
# class DoctorDetails(db.Model):
#     id = db.Column(db.Integer, primary_key =True)
#     user_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
#     phone_number = db.Column(db.Integer, unique=True, nullable=False)
#     first_name = db.Column(db.String(100), nullable=False)
#     last_name = db.Column(db.String(100), nullable=False) 
#     date_of_birth = db.Column(db.Date,nullable=False) 
#     age = db.Column(db.Integer, nullable=False) 
#     #personal _qualification
#     First_qualification = db.Column(db.String(10),nullable=False)
#     year_of_passing = db.Column(db.Integer, nullable=False)

#     gender = db.Column(db.String(10),nullable=False)
#     name_of_hospital = db.Column(db.String(100),nullable=False )
#     Designation = db.Column(db.String(10),nullable=False)
#     medical_council_member = db.Column(db.Integer,nullable=False)
#     certificate = db.Column(db.String(255),nullable=False)
#     speciality = db.Column(db.String(10),nullable=False)
#     About_the_doctor = db.Column(db.String(255))

#     # Define a relationship to the Doctor Table
#     doctor = db.relationship('Doctor',backref= db.backref('doctor_details',lazy=True))


@app.route('/doctor', methods = ['POST'])
def create_doctor_details():
    data = request.json

    if 'first_name' not in data:
        return jsonify({'error': 'First name is required'}), 400
    elif 'phone_number' not in data:
        return jsonify({'error': 'Phone number is required'}), 400
    elif 'last_name' not in data:
        return jsonify({'error': 'Last name is required'}), 400
    elif 'date_of_birth' not in data:
        return jsonify({'error': 'Date of birth is required'}), 400
    elif 'First_qualification' not in data:
        return jsonify({'error': 'First qualification  is required'}), 400
    elif 'year_of_passing' not in data:
        return jsonify({'error': 'Year_of_passing is required'}), 400
    elif 'gender' not in data:
        return jsonify({'error': 'Gender is required'}), 400
    elif 'name_of_hospital' not in data:
        return jsonify({'error':'Name of hospital is required'})
    elif 'Designation' not in data:
        return jsonify({'error': 'Designation  is required'}), 400
    elif 'medical_council_member' not in data:
        return jsonify({'error': 'Medical_council_member is required'}), 400
    elif 'certificate' not in data:
        return jsonify({'error': 'Certificate is required'}), 400
    elif 'speciality' not in data:
        return jsonify({'error': 'Speciality  is required'}), 400
    

    first_name = data['first_name']
    last_name = data['last_name']
    name_of_hospital = data['name_of_hospital']
    phone_number = str(data['phone_number'])[-5:]  # Extract last 3 digits of phone number
    if not re.match(r'^\d+$', str(data['phone_number'])):
         return jsonify({'error': 'Invalid phone number format. Must contain 10 numeric digits.'}), 400
    elif len(str(data['phone_number'])) > 10:
         return jsonify({'error': 'Invalid phone number length. Entered number is greater than 10 digits.'}), 400
    elif len(str(data['phone_number'])) < 10:
         return jsonify({'error': 'Invalid phone number length. Entered number is less than 10 digits.'}), 400
   
    user_id = f"{first_name[:2]}{last_name[:2]}{phone_number}"
    #QR_GENERATOR(user_id)
    QR_GENERATOR(user_id,first_name+' '+last_name,name_of_hospital)
    #Convert date_of_birth string to Python date
    # date_of_birth = datetime.datetime.strptime(data.get('date_of_birth', ''), '%Y-%m-%d').date() if 'date_of_birth' in data else None
    date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
    age= calculate_age(date_of_birth)

    new_doctor_details = Doctor(
        user_id=user_id,
        phone_number=data['phone_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=date_of_birth,
        age = age,
        First_qualification = data['First_qualification'],
        year_of_passing = data['year_of_passing'],
        gender=data['gender'],
        name_of_hospital = data['name_of_hospital'],
        Designation = data['Designation'],
        medical_council_member = data['medical_council_member'],
        certificate = data['certificate'],
        speciality = data['speciality'],
        About_the_doctor = data.get('About_the_doctor')

     )
    try:
       db.session.add(new_doctor_details)
       db.session.commit()
       return jsonify({'message':'User detail created successfully', 'userName':user_id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Phone number already exists'}), 400


@app.route('/doctor',methods=['GET'])
def get_all_doctor_details():
    doctor_details = Doctor.query.all()
    result = [{'id': detail.id, 'doctor_id': detail.user_id, 'phone_number': detail.phone_number, 'first_name': detail.first_name, 'last_name': detail.last_name,'age':detail.age,'gender':detail.gender,'speciality':detail.speciality} for detail in doctor_details]
    return jsonify(result), 200
@app.route('/doctor/<int:doctor_detail_id>',methods=['GET'])
def get_doctor_detail(doctor_detail_id):
    doctor_detail = Doctor.query.get_or_404(doctor_detail_id)
    return jsonify({'id': doctor_detail.id, 'user_id': doctor_detail.user_id, 'phone_number': doctor_detail.phone_number, 'first_name': doctor_detail.first_name, 'last_name': doctor_detail.last_name,'age':doctor_detail.age,'gender':doctor_detail.gender,'speciality':doctor_detail.speciality}), 200
@app.route('/doctor/<int:doctor_detail_id>',methods=['PUT'])
def update_doctor_detail(doctor_detail_id):
     doctor_detail = Doctor.query.get_or_404(doctor_detail_id)
     data = request.json
     doctor_detail.phone_number=data.get('phone_number', doctor_detail.phone_number)
     doctor_detail.first_name=data.get('first_name', doctor_detail.first_name)
     doctor_detail.last_name=data.get('last_name', doctor_detail.last_name)
     date_of_birth_str = data.get('date_of_birth')  # Assuming 'date_of_birth' is in "YYYY-MM-DD" format
     if date_of_birth_str:
    # Convert date string to Python date object
        date_of_birth_obj = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
     else:
       date_of_birth_obj = doctor_detail.date_of_birth  # Keep the existing date if not provided in the data

     doctor_detail.date_of_birth = date_of_birth_obj
     doctor_detail.First_qualification = data.get('First_qualification',doctor_detail.First_qualification)
     doctor_detail.year_of_passing = data.get('year_of_passing',doctor_detail.year_of_passing)
     doctor_detail.gender=data.get('gender', doctor_detail.gender)
     doctor_detail.Designation = data.get('Designation',doctor_detail.Designation)
     doctor_detail.medical_council_member = data.get('medical_council_member',doctor_detail.medical_council_member)
     doctor_detail.certificate = data.get('certificate',doctor_detail.certificate)
     doctor_detail.speciality = data.get('speciality',doctor_detail.speciality)
     doctor_detail.About_the_doctor = data.get('About_the_doctor',doctor_detail.About_the_doctor)
     db.session.commit()
     return jsonify({'message': 'Doctor detail updated successfully'}), 200
@app.route('/doctor/<int:doctor_detail_id>',methods =['DELETE'])
def delete_user_details(doctor_detail_id):
    doctor_detail = Doctor.query.get_or_404(doctor_detail_id)
    db.session.delete(doctor_detail)
    db.session.commit()
    return jsonify({'message': 'Doctor detail deleted successfully'}), 200

    
# Define association table for Doctor-Patient relationship
doctor_patient_association = db.Table('doctor_patient_association',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id')),
    db.Column('user_details_id', db.Integer, db.ForeignKey('user_details.user_id'))
)


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
    age = db.Column(db.Integer,nullable=False)
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




@app.route('/patient', methods=['POST'])
def create_user_detail():
    data = request.json
    
    # Generate user_id
    if 'first_name' not in data:
        return jsonify({'error': 'First name is required'}), 400
    elif 'phone_number' not in data:
        return jsonify({'error': 'Phone number is required'}), 400
    elif 'last_name' not in data:
        return jsonify({'error': 'Last name is required'}), 400
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = str(data['phone_number'])[-5:]  # Extract last 3 digits of phone number
    if not re.match(r'^\d+$', str(data['phone_number'])):
         return jsonify({'error': 'Invalid phone number format. Must contain 10 numeric digits.'}), 400
    elif len(str(data['phone_number'])) > 10:
         return jsonify({'error': 'Invalid phone number length. Entered number is greater than 10 digits.'}), 400
    elif len(str(data['phone_number'])) < 10:
         return jsonify({'error': 'Invalid phone number length. Entered number is less than 10 digits.'}), 400
    user_id = f"{first_name[:2]}{last_name[:2]}{phone_number}"
    
    # Convert date_of_birth string to Python date object
    date_of_birth = datetime.strptime(data.get('date_of_birth', ''), '%Y-%m-%d').date() if 'date_of_birth' in data else None
    age=calculate_age(date_of_birth)
    
    
    new_user_detail = UserDetails(
        user_id=user_id,
        phone_number=data['phone_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=date_of_birth,
        age=age,
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
    try:
       db.session.add(new_user_detail)
       db.session.commit()
       return jsonify({'message': 'User detail created successfully', 'userName': user_id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Phone number already exists'}), 400


@app.route('/patient', methods=['GET'])
def get_all_user_details():
    user_details = UserDetails.query.all()
    result = [{'id': detail.id, 'user_id': detail.user_id, 'phone_number': detail.phone_number, 'first_name': detail.first_name, 'last_name': detail.last_name,'age':detail.age,'gender':detail.gender} for detail in user_details]
    return jsonify(result), 200

@app.route('/patient/<int:user_detail_id>', methods=['GET'])
def get_user_detail(user_detail_id):
    user_detail = UserDetails.query.get_or_404(user_detail_id)
    return jsonify({'id': user_detail.id, 'user_id': user_detail.user_id, 'phone_number': user_detail.phone_number, 'first_name': user_detail.first_name, 'last_name': user_detail.last_name,'age':user_detail.age,'gender':user_detail.gender,'speciality':user_detail.speciality}), 200

@app.route('/patient/<int:user_detail_id>', methods=['PUT'])
def update_user_detail(user_detail_id):
    user_detail = UserDetails.query.get_or_404(user_detail_id)
    data = request.json
    user_detail.phone_number = data.get('phone_number', user_detail.phone_number)
    user_detail.first_name = data.get('first_name', user_detail.first_name)
    user_detail.last_name = data.get('last_name', user_detail.last_name)
    date_of_birth_str = data.get('date_of_birth')  # Assuming 'date_of_birth' is in "YYYY-MM-DD" format

    if date_of_birth_str:
    # Convert date string to Python date object
        date_of_birth_obj = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
    else:
       date_of_birth_obj = user_detail.date_of_birth  # Keep the existing date if not provided in the data

    user_detail.date_of_birth = date_of_birth_obj
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

@app.route('/patient/<int:user_detail_id>', methods=['DELETE'])
def delete_user_detail(user_detail_id):
    user_detail = UserDetails.query.get_or_404(user_detail_id)
    db.session.delete(user_detail)
    db.session.commit()
    return jsonify({'message': 'User detail deleted successfully'}), 200

# New routes for assigning patients to doctors and for doctors to view their assigned patients
# @app.route('/create_doctor', methods=['POST'])
# def create_doctor():
#     data = request.json
#     name = data.get('name')

#     new_doctor = Doctor(name=name)
#     db.session.add(new_doctor)
#     db.session.commit()

#     return jsonify({'message': 'Doctor created successfully', 'doctor_id': new_doctor.id}), 201

@app.route('/doctor/patient', methods=['POST'])
def assign_patient_to_doctor():
    data = request.json
    doctor_id = data.get('doctor_id')
    patient_id = data.get('patient_id')

    doctor = Doctor.query.get(doctor_id)
    if doctor is None:
        return jsonify({'error': 'Doctor not found'}), 404

    patient = UserDetails.query.get(patient_id)
    if patient is None:
        return jsonify({'error': 'Patient not found'}), 404

    doctor.patients.append(patient)
    db.session.commit()
    return jsonify({'message': 'Patient assigned to doctor successfully'}), 200

@app.route('/doctor/<int:doctor_id>/patients', methods=['GET'])
def get_doctor_patients(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor is None:
        return jsonify({'error': 'Doctor not found'}), 404

    patients = doctor.patients
    result = [{'id': patient.id, 'user_id': patient.user_id, 'phone_number': patient.phone_number, 'first_name': patient.first_name, 'last_name': patient.last_name} for patient in patients]
    return jsonify(result), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port='8081', debug=True)
