from typing import Optional

from ninja import Field, Schema
from ninja.types import DictStrAny
from ninja_jwt.schema import TokenObtainPairInputSchema
from users.schemas import PatientOut, UserOut, UserRoleOut


class CustomTokenObtainOutSchema(Schema):
    token: str
    user_role: UserRoleOut


class CustomTokenObtainSchema(TokenObtainPairInputSchema):
    """
    Schema responsável por tratar o Schema (modelo Pydantic) de entrada para o login.
    """

    def output_schema(self) -> CustomTokenObtainOutSchema:
        token = self.to_response_schema().access
        return CustomTokenObtainOutSchema(token=token, user_role=self._user)
