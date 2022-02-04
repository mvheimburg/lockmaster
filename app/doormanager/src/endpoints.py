"""Endpoints module."""

from fastapi import APIRouter, Depends, Response, status, Form, Body
from dependency_injector.wiring import inject, Provide

from containers import Container
from services import UserService, AccessService, BellService
# from services import UserService
from repositories import NotFoundError

import logging

from models import UserModel

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/get_users/')
@inject
async def get_users(
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    print('/get_users/')
    return user_service.get_users()


@router.get('/get_user/{user_id}')
@inject
async def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    print('/get_user/id')   
    try:
        return user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post('/create_user/', status_code=status.HTTP_201_CREATED)
@inject
async def add(
        user: UserModel,
        user_service: UserService = Depends(Provide[Container.user_service]),
        access_service: AccessService = Depends(Provide[Container.access_service])
):
    print('/create_user/')
    new_user = user_service.create_user(user.dict())
    if new_user:
        access_service.user_created(new_user)
    return new_user


@router.post('/test_user/', status_code=status.HTTP_201_CREATED)
@inject
async def test_add(
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    print('/test_user/')
    return user_service.create_test_user()



@router.delete('/delete_user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    print('/delete_user/id')
    try:
        user_service.delete_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/status/')
async def get_status():
    print('/status/')
    return {'status': 'OK'}


# @router.put('/post_candidate_list', status_code=status.HTTP_200_OK)
# @inject
# async def post_candidate_list(
#         candidates: BeaconListModel,
#         access_service: AccessService = Depends(Provide[Container.access_service]),
# ):
#     print('/post_candidate_list')
#     return access_service.post_candidate_list(candidates)


# @router.get('/doormanager/get_access_level', status_code=status.HTTP_200_OK)
# @inject
# async def get_access_level(
#     access_service: AccessService = Depends(Provide[Container.access_service]),
# ):
#     print('/doormanager/get_access_level')
#     return access_service.get_access_level()

@router.get('/get_access_level')
@inject
async def get_access_level(
    access_service: AccessService = Depends(Provide[Container.access_service]),
):
    print('/get_access_level')
    return access_service.get_access_level()


@router.put('/get_access_level_by_pin/')
@inject
async def get_access_level_by_pin(
    pin: int=Body(...),
    access_service: AccessService = Depends(Provide[Container.access_service]),
):
    print('/get_access_level_by_pin/')
    return access_service.get_access_level_by_pin(pin)


# @router.put('/detected_beacon/')
# @inject
# async def detected_beacon(
#     beacon: BeaconModel,
#     access_service: AccessService = Depends(Provide[Container.access_service]),
# ):
#     print('/detected_beacon/')
#     return access_service.detected_beacon(beacon)


@router.get('/get_current_candidate_list/')
@inject
async def get_current_candidate_list(
    access_service: AccessService = Depends(Provide[Container.access_service]),
):
    print('/get_current_candidate_list/')
    try:
        return access_service.get_current_candidate_list()
    except Exception as e:
        return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.post('/ring_doorbell/', status_code=status.HTTP_200_OK)
@inject
async def ring_doorbell(
    bell_service: BellService = Depends(Provide[Container.bell_service]),
):
    print('/ring_doorbell/')
    return bell_service.ring_doorbell()


@router.post('/delete_db/', status_code=status.HTTP_200_OK)
@inject
async def delete_db(
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    print('/delete_db/')
    return user_service.delete_db()