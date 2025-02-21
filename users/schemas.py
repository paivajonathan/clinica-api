from ninja import Schema, Field, FilterSchema
from typing import Optional
from ninja.types import DictStrAny
from .models import Patient
import datetime


class UserFilter(FilterSchema):
    id: Optional[int] = Field(None, q="id__exact")
    role: Optional[str] = Field(None, q="role__iexact",)


class DoctorFilter(FilterSchema):
    id: Optional[int] = Field(None, q="id__exact")


class PatientOut(Schema):
    id: int
    full_name: str
    birth_date: datetime.date
    gender: str
    phone: str
    address: str
    
    @staticmethod
    def resolve_full_name(obj):
        return obj.user.get_full_name()
    

class DoctorOut(Schema):
    id: int
    full_name: str
    code: str
    phone: str
    specialty: str
    
    @staticmethod
    def resolve_full_name(obj):
        return obj.user.get_full_name()

    @staticmethod
    def resolve_specialty(obj):
        return obj.specialty.description


class UserOut(Schema):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    

class UserRoleOut(Schema):
    user: UserOut
    patient: PatientOut | None
    doctor: DoctorOut | None
    
    @staticmethod
    def resolve_user(obj):
        return obj
    
    @staticmethod
    def resolve_patient(obj):
        if obj.role == "P":
            return obj.patient
    
    @staticmethod
    def resolve_doctor(obj):
        if obj.role == "D":
            return obj.doctor

class UserIn(Schema):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class PatientIn(Schema):
    birth_date: datetime.date
    gender: str
    phone: str
    address: str
    

class UserPatientIn(Schema):
    user: UserIn
    patient: PatientIn
    

class DoctorIn(Schema):
    code: str
    phone: str
    specialty_id: int


class UserDoctorIn(Schema):
    user: UserIn
    doctor: DoctorIn
