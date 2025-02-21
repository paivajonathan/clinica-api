from ninja import Swagger
from ninja_extra import NinjaExtraAPI

from auth.controllers import AuthController
from users.controllers import UserController
from consultations.controllers import AttendanceController, ConsultationController


api = NinjaExtraAPI(
    title="API",
    docs=Swagger(
        settings={
            "docExpansion": "none",
            "tagsSorter": "alpha",
            "filter": True,
            "syntaxHighlight": {
                "activate": True,
                "theme": "nord",
            },
            "persistAuthorization": True,
        }
    ),
)

api.register_controllers(
    AuthController,
    UserController,
    ConsultationController,
    AttendanceController,
)