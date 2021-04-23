"""Containers module."""

from dependency_injector import containers, providers

from doormanager import Doormanager
# from mqttlayer import MqttLayer
from database import Database
from repositories import UserRepository
from services import UserService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    doormanager = providers.Singleton(Doormanager, doors_cfg=config)

    # mqttlayer = providers.Singleton(MqttLayer)

    db = providers.Singleton(Database)


    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )