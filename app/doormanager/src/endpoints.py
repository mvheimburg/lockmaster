"""Endpoints module."""

from fastapi import APIRouter, WebSocket, Depends, Response, status, Form, Body
from dependency_injector.wiring import inject, Provide

from containers import Container
from services import UserService, AccessService, BellService, DoorService
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


@router.put('/unlock_door/')
@inject
async def put_unlock_door(
    door_name: str=Body(...),
    door_service: DoorService = Depends(Provide[Container.door_service]),
):
    print('/unlock_door/')
    return door_service.unlock_door(door_name)


@router.put('/lock_door/')
@inject
async def put_lock_door(
    door_name: str=Body(...),
    door_service: DoorService = Depends(Provide[Container.door_service]),
):
    print('/unlock_door/')
    return door_service.lock_door(door_name)


@router.put('/toggle_door/')
@inject
async def put_toggle_door(
    door_name: str=Body(...),
    door_service: DoorService = Depends(Provide[Container.door_service]),
):
    print('/toggle_door/')
    return door_service.toggle_door(door_name)


@router.get('/door_state/{door_name}/')
@inject
async def get_door_state(
    door_name: str,
    door_service: DoorService = Depends(Provide[Container.door_service]),
):
    print('/unlock_door/')
    return door_service.get_door_state(door_name)



# @router.websocket_route('/ws/route_test/')
# @inject
# async def websocket_door_state(
#     websocket: WebSocket,
# ):
#     await websocket.accept()
#     c = 0
#     while True:
#         c+=1
#         await websocket.send_text(f"Message text was: {c}")

@router.websocket('/ws/door_state/{door_name}/')
@inject
async def ws_test(
    websocket: WebSocket,
    door_name: str,
    door_service: DoorService = Depends(Provide[Container.door_service]),
):
    await websocket.accept()
    x = door_service.get_door_state(door_name)
    websocket.send(x)
    while True:
        x = await door_service.async_get_door_state(door_name)
        websocket.send(x)



@router.websocket('/ws/test/')
@inject
async def ws_test(
    websocket: WebSocket,
):
    await websocket.accept()
    c = 0
    while True:
        c+=1
        await websocket.send_text(f"Message text was: {c}")