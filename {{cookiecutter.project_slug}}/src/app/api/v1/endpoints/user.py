from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Params

from app import crud
from app.api import deps
from app.deps import user_deps
from app.models import User
from app.models.role_model import Role
from app.schemas.common_schema import IOrderEnum
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import IUserCreate, IUserRead, IUserUpdate
from app.utils.exceptions import IdNotFoundException, UserSelfDeleteException

router = APIRouter()


@router.get("")
async def get_my_data(
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IUserRead]:
    """
    Gets my user profile information
    """
    return create_response(data=current_user)


@router.put("")
async def update_self_user(
    user: IUserUpdate,
    current_user: User = Depends(deps.get_current_user()),
) -> IPutResponseBase[IUserRead]:
    """
    Update self user parameter
    """
    if current_user.email != user.email:
        await user_deps.email_exists(user=user)
    if current_user.username != user.username:
        await user_deps.username_exists(user=user)

    user_updated = await crud.user.update(obj_new=user, obj_current=current_user)
    return create_response(data=user_updated)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: IUserCreate = Depends(user_deps.user_exists),
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin])),
) -> IPostResponseBase[IUserRead]:
    """
    Creates a new user
    """
    role = await crud.role.get(id=user.role_id)
    if not role:
        raise IdNotFoundException(Role, id=user.role_id)

    user = await crud.user.create_with_role(obj_in=user)
    return create_response(data=user)


@router.get("/list")
async def read_users_list(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IUserRead]:
    """
    Retrieve users. Requires admin or manager role
    """
    users = await crud.user.get_multi_paginated(params=params)
    return create_response(data=users)


@router.get("/list/by_created_at")
async def get_user_list_order_by_created_at(
    order: IOrderEnum
    | None = Query(
        default=IOrderEnum.ascendent,
        description="It is optional. Default is ascendent",
    ),
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IUserRead]:
    """
    Gets a paginated list of users ordered by created datetime
    """
    users = await crud.user.get_multi_paginated_ordered(
        params=params,
        order=order,
        order_by="created_at",
    )
    return create_response(data=users)


@router.get("/{user_id}")
async def get_user_by_id(
    user: User = Depends(user_deps.is_valid_user),  # user_id
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IUserRead]:
    """
    Gets a user by his/her id
    """
    return create_response(data=user)


@router.put("/{user_id}")
async def update_user_by_id(
    user: IUserUpdate,
    updated_user: User = Depends(user_deps.is_valid_user),  # user_id
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin])),
) -> IPutResponseBase[IUserRead]:
    """
    Update a user by his/her id
    """
    if updated_user.email != user.email:
        await user_deps.email_exists(user=user)
    if updated_user.username != user.username:
        await user_deps.username_exists(user=user)

    user_updated = await crud.user.update(obj_new=user, obj_current=updated_user)
    return create_response(data=user_updated)


@router.delete("/{user_id}")
async def remove_user_by_id(
    user: User = Depends(user_deps.is_valid_user),  # user_id
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin])),
) -> IDeleteResponseBase[IUserRead]:
    """
    Delete a user by his/her id
    """
    if current_user.id == user.id:
        raise UserSelfDeleteException()

    user = await crud.user.remove(id=user.id)
    return create_response(data=user, message="User removed")
