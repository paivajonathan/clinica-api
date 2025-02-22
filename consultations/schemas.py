
import datetime
from ninja import Schema, FilterSchema, Field
from typing import Optional


class AttendanceShow(Schema):
    observations: str
    consultation_id: int


class AttendanceRegister(Schema):
    observations: str
    consultation_id: int


class ConsultationFilter(FilterSchema):
    id: Optional[int] = Field(None, q="id__exact")
    patient_id: Optional[int] = Field(None, q="patient_id__exact",)
    doctor_id: Optional[int] = Field(None, q="doctor_id__exact",)
    status: Optional[str] = Field(None, q="status__iexact")


class ConsultationShow(Schema):
    id: int
    date: datetime.date
    time: datetime.time
    status: str
    observations: str
    patient_id: int
    patient_full_name: str
    doctor_id: int
    doctor_full_name: str
    
    @staticmethod
    def resolve_patient_full_name(obj):
        return obj.patient.user.get_full_name()
        
    @staticmethod
    def resolve_doctor_full_name(obj):
        return obj.doctor.user.get_full_name()
    

class ConsultationRegister(Schema):
    date: datetime.date
    time: datetime.time
    observations: str
    doctor_id: int


