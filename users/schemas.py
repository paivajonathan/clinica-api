from ninja import Schema
from ninja.types import DictStrAny
from .models import Patient
import datetime


class PatientOut(Schema):
    gender: str
    

class DoctorOut(Schema):
    code: str


class UserOut(Schema):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    

class UserRoleOut(Schema):
    user: UserOut
    patient_data: PatientOut | None
    doctor_data: DoctorOut | None
    
    @staticmethod
    def resolve_user(obj):
        return obj
    
    @staticmethod
    def resolve_patient_data(obj):
        if obj.role == "P":
            return obj.patient
    
    @staticmethod
    def resolve_doctor_data(obj):
        if obj.role == "D":
            return obj.doctor

class UserIn(Schema):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class PatientIn(Schema):
    user_data: UserIn
    birth_date: datetime.date
    gender: str
    phone: str
    address: str
    

class DoctorIn(Schema):
    user_data: UserIn
    code: str
    phone: str
    specialty_id: int
