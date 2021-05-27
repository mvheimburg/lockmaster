"""Endpoints module."""

from fastapi import APIRouter, Depends, Response, status, Form
from dependency_injector.wiring import inject, Provide

from containers import Container
from services import UserService, AccessService
# from services import UserService
from repositories import NotFoundError

import logging

from models import UserModel, MacListModel

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/get_users')
@inject
def get_users(
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.get_users()


@router.get('/get_user/{user_id}')
@inject
def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        return user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post('/create_user', status_code=status.HTTP_201_CREATED)
@inject
def add(
        user: UserModel,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.create_user(user.dict())


@router.post('/test_user', status_code=status.HTTP_201_CREATED)
@inject
def test_add(
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.create_test_user()



@router.delete('/delete_user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        user_service.delete_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/status')
def get_status():
    return {'status': 'OK'}


@router.post('/post_candidate_list', status_code=status.HTTP_200_OK)
@inject
def post_candidate_list(
        candidates: MacListModel,
        access_service: AccessService = Depends(Provide[Container.access_service]),
):
    print(f'got cadindates: {candidates}')
    return access_service.post_candidate_list(candidates)


@router.get('/get_access_level', status_code=status.HTTP_200_OK)
@inject
def get_access_level(
    access_service: AccessService = Depends(Provide[Container.access_service]),
):
    return access_service.get_access_level()


@router.get('/get_current_candidate_list', status_code=status.HTTP_200_OK)
@inject
def get_current_candidate_list(
    access_service: AccessService = Depends(Provide[Container.access_service]),
):
    return access_service.get_current_candidate_list()