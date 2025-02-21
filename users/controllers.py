from typing import List, Dict, Any, Optional

from django.http import Http404
from ninja import Query
from ninja.types import DictStrAny
from ninja.pagination import paginate
from ninja_extra.ordering import Ordering, ordering
from ninja_extra import api_controller, route, status
from django.db.models import Q
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction

from .schemas import (
    UserFilter,
    UserDoctorIn,
    UserPatientIn,
    UserRoleOut,
    DoctorFilter,
    DoctorOut,
    PatientOut,
)
from .models import Patient, User, Doctor


@api_controller(
    "users/",
    auth=JWTAuth(),
    tags=["USERS"],
)
class UserController:
    @route.get(
        "/",
        response=List[UserRoleOut],
        permissions=[],
    )
    def list(self, filters: UserFilter = Query(...)):
        users = User.objects.all()
        users = filters.filter(users)
        return users
    
    @route.get(
        "/doctors/",
        response={
            status.HTTP_200_OK: List[DoctorOut],
            status.HTTP_403_FORBIDDEN: DictStrAny,
        },
        permissions=[],
    )
    def list(self, request, filters: DoctorFilter = Query(...), has_pending_consultation: Optional[bool] = Query(None)):
        doctors = Doctor.objects.all()
        doctors = filters.filter(doctors)
        
        if has_pending_consultation is not None:
            if request.user.role != "P":
                return status.HTTP_403_FORBIDDEN, {"message": "Forbidden"}
            
            patient_pending_consultations = request.user.patient.consultations.filter(status="S").values_list("doctor_id", flat=True)
            
            if has_pending_consultation is True:
                doctors = doctors.filter(id__in=patient_pending_consultations)
            else:
                doctors = doctors.exclude(id__in=patient_pending_consultations)
        
        return doctors

    @route.get(
        "/{int:id}/",
        response={
            status.HTTP_200_OK: UserRoleOut,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(User, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                "message": f"{User._meta.verbose_name.capitalize()} não existe."
            }

    @route.get(
        "/doctor/{int:id}/",
        response={
            status.HTTP_200_OK: DoctorOut,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get_doctor(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(Doctor, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                "message": f"{Doctor._meta.verbose_name.capitalize()} não existe."
            }

    @route.get(
        "/patient/{int:id}/",
        response={
            status.HTTP_200_OK: PatientOut,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get_patient(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(Patient, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                "message": f"{Patient._meta.verbose_name.capitalize()} não existe."
            }

    @route.post(
        "/patient/register/",
        auth=None,
        response={
            status.HTTP_201_CREATED: UserRoleOut,
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
    def register_patient(self, request, payload: UserPatientIn):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                user_data = payload.pop("user", {})
                patient_data = payload.pop("patient", {})
                
                user = User.objects.create_user(**user_data, role="P")
                patient = Patient.objects.create(**patient_data, user=user)
                
                return status.HTTP_201_CREATED, user
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @route.put(
        "/patient/edit/",
        response={
            status.HTTP_200_OK: UserRoleOut,
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
    def edit_patient(self, request, payload: UserPatientIn):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                user_data = payload.pop("user", {})
                patient_data = payload.pop("patient", {})
                
                user = get_object_or_404(User, id=request.user.id)
                
                for k, v in user_data.items():
                    if k == "password":
                        user.set_password(v)
                        continue
                    setattr(user, k, v)    
                
                patient = user.patient
                
                for k, v in patient_data.items():
                    setattr(user, k, v)    
                
                user.save()
                patient.save()
                
                return status.HTTP_200_OK, user
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                "message": f"{User._meta.verbose_name.capitalize()} não existe."
            }
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @route.put(
        "/doctor/edit/",
        response={
            status.HTTP_200_OK: UserRoleOut,
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
    def edit_doctor(self, request, payload: UserDoctorIn):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                user_data = payload.pop("user", {})
                doctor_data = payload.pop("doctor", {})
                
                user = get_object_or_404(User, id=request.user.id)
                
                for k, v in user_data.items():
                    if k == "password":
                        user.set_password(v)
                        continue
                    setattr(user, k, v)    
                
                doctor = user.doctor
                
                for k, v in doctor_data.items():
                    setattr(user, k, v)    
                
                user.save()
                doctor.save()
                
                return status.HTTP_200_OK, user
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                "message": f"{User._meta.verbose_name.capitalize()} não existe."
            }
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @route.delete(
        "/delete-account/",
        response={
            status.HTTP_204_NO_CONTENT: None,
            frozenset(
                [
                    status.HTTP_404_NOT_FOUND,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                ]
            ): DictStrAny,
        },
        permissions=[],
    )
    def delete_account(self, request):
        try:
            with transaction.atomic():
                user = get_object_or_404(User, id=request.user.id)
                
                if user.role == "P":
                    patient = user.patient
                    patient.delete()
                elif user.role == "D":
                    doctor = user.doctor
                    doctor.delete()
                
                user.delete()
                return status.HTTP_204_NO_CONTENT, None
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                "message": f"{User._meta.verbose_name.capitalize()} não existe."
            }
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}
