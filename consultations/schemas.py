
import datetime
from ninja import Schema


class ConsultationShow(Schema):
    date: datetime.date
    time: datetime.time
    status: str
    observations: str
    patient_id: int
    doctor_id: int


class ConsultationRegister(Schema):
    date: datetime.date
    time: datetime.time
    observations: str
    doctor_id: int


class AttendanceShow(Schema):
    observations: str
    consultation_id: int


class AttendanceRegister(Schema):
    observations: str
    consultation_id: int
