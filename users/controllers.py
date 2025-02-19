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
    PatientIn,
    DoctorIn,
    UserRoleOut,
)
from .models import Patient, User


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
    def list(self):
        return User.objects.all()

    @route.get(
        "/{int:id}",
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

    @route.post(
        "/patient/register",
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
    def register_patient(self, request, payload: PatientIn):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                user_data = payload.pop("user_data", {})
                patient_data = payload
                
                user = User.objects.create_user(**user_data, role="P")
                patient = Patient.objects.create(**patient_data, user=user)
                
                return status.HTTP_201_CREATED, user
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    # @route.put(
    #     "/patient/edit",
    #     response={
    #         status.HTTP_200_OK: UserOut,
    #         frozenset(
    #             [
    #                 status.HTTP_400_BAD_REQUEST,
    #                 status.HTTP_404_NOT_FOUND,
    #                 status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             ]
    #         ): dict[str, any],
    #     },
    #     permissions=[],
    # )
    # def edit_patient(self, request, payload: PatientIn):
    #     try:
    #         with transaction.atomic():
    #             user = get_object_or_404(User, id=request.user.id)
    #             return status.HTTP_200_OK, instance
    #     except Http404:
    #         return status.HTTP_404_NOT_FOUND, {
    #             "message": f"{User._meta.verbose_name.capitalize()} não existe."
    #         }
    #     except IntegrityError as error:
    #         return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}
        
    # @route.put(
    #     "/doctor/edit",
    #     response={
    #         status.HTTP_200_OK: UserOut,
    #         frozenset(
    #             [
    #                 status.HTTP_400_BAD_REQUEST,
    #                 status.HTTP_404_NOT_FOUND,
    #                 status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             ]
    #         ): dict[str, any],
    #     },
    #     permissions=[],
    # )
    # def edit_patient(self, request, payload: PatientIn):
    #     try:
    #         with transaction.atomic():
    #             instance = User.objects.create(**payload)
    #             return status.HTTP_200_OK, instance
    #     except Http404:
    #         return status.HTTP_404_NOT_FOUND, {
    #             "message": f"{User._meta.verbose_name.capitalize()} não existe."
    #         }
    #     except IntegrityError as error:
    #         return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    # @route.delete(
    #     "/delete-account",
    #     response={
    #         status.HTTP_204_NO_CONTENT: None,
    #         frozenset(
    #             [
    #                 status.HTTP_404_NOT_FOUND,
    #                 status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             ]
    #         ): dict[str, any],
    #     },
    #     permissions=[],
    # )
    # def delete_account(self, request):
    #     try:
    #         with transaction.atomic():
    #             instance = get_object_or_404(User, id=request.user.id)
    #             instance.delete()
    #             return status.HTTP_204_NO_CONTENT, None
    #     except Http404:
    #         return status.HTTP_404_NOT_FOUND, {
    #             "message": f"{User._meta.verbose_name.capitalize()} não existe."
    #         }
    #     except IntegrityError as error:
    #         return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}
