"""Containers module."""

from dependency_injector import containers, providers


from database import Database
from repositories import UserRepository
from services import UserService, AccessService, DoorService, BellService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


    db = providers.Singleton(Database)


    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    door_service = providers.Singleton(
        DoorService, 
        doors_cfg=config.doors
    )

    bell_service = providers.Singleton(
        BellService, 
        bell_cfg=config.bell
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    access_service = providers.Singleton(
        AccessService,
        user_repository=user_repository,
    )