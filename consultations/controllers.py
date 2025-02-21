from typing import List, Dict, Any

from django.http import Http404
from ninja import Query
from ninja.types import DictStrAny
from ninja.pagination import paginate
from ninja_extra.ordering import Ordering, ordering
from ninja_extra import api_controller, route, status
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction

from .schemas import (
    ConsultationShow,
    ConsultationRegister,
    AttendanceShow,
    AttendanceRegister
)
from .models import Consultation, Attendance


@api_controller(
    "consultations/",
    auth=JWTAuth(),
    tags=["CONSULTATIONS"],
)
class ConsultationController:
    @route.get(
        "/",
        response=List[ConsultationShow],
        permissions=[],
    )
    def list(self):
        return Consultation.objects.all()

    @route.get(
        "/{int:id}/",
        response={
            status.HTTP_200_OK: ConsultationShow,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(Consultation, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                "message": f"{Consultation._meta.verbose_name.capitalize()} não existe."
            }

    @route.post(
        "/",
        response={
            status.HTTP_201_CREATED: ConsultationShow,
            frozenset(
                [
                    status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                ]
            ): DictStrAny,
        },
        permissions=[],
    )
    def register(self, request, payload: ConsultationRegister):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                print(payload)
                
                consultation = Consultation.objects.create(**payload, patient_id=request.user.patient.id)
                
                return status.HTTP_201_CREATED, consultation
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @route.put(
        "/{int:id}/cancel/",
        response={
            status.HTTP_200_OK: ConsultationShow,
            frozenset(
                [
                    status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                ]
            ): DictStrAny,
        },
        permissions=[],
    )
    def cancel(self, request, id: int):
        try:
            with transaction.atomic():
                consultation = get_object_or_404(Consultation, id=id)
                consultation.status = "C"
                consultation.save()
                return status.HTTP_200_OK, consultation
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                "message": f"{Consultation._meta.verbose_name.capitalize()} não existe."
            }
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}



@api_controller(
    "attendances/",
    auth=JWTAuth(),
    tags=["ATTENDANCES"],
)
class AttendanceController:
    @route.get(
        "/",
        response=List[AttendanceShow],
        permissions=[],
    )
    def list(self):
        return Attendance.objects.all()

    @route.get(
        "/{int:id}/",
        response={
            status.HTTP_200_OK: AttendanceShow,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(Attendance, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                "message": f"{Attendance._meta.verbose_name.capitalize()} não existe."
            }

    @route.post(
        "/",
        response={
            status.HTTP_201_CREATED: AttendanceShow,
            frozenset(
                [
                    status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                ]
            ): DictStrAny,
        },
        permissions=[],
    )
    def register(self, request, payload: AttendanceRegister):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                consultation_id = payload.get("consultation_id", 0)
                consultation = Consultation.objects.filter(id=consultation_id).first()
                if consultation is None:
                    return status.HTTP_404_NOT_FOUND, {"message": "Não foi possível encontrar essa consulta."}
                
                consultation.status = "F"
                consultation.save()
                
                attendance = Attendance.objects.create(**payload)
                
                return status.HTTP_201_CREATED, attendance
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}
