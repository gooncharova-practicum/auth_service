from pydantic import UUID4
from src.core import logger
from src.db.models import Role
from src.services.db_manager import Cursor
from src.services.models import ServiceResult


def get_roles_list() -> ServiceResult:
    cur = Cursor()
    all_roles = cur.get_all_items(Role)

    return ServiceResult(success=True, data=all_roles)


def get_roles_info(role_id: UUID4) -> ServiceResult:
    cur = Cursor()
    first_role = cur.get_first_match(Role, Role.uid, role_id)
    if not first_role:
        error_message = f"Role with uuid={role_id} is not exist"
        return ServiceResult(success=False, error_message=error_message)

    return ServiceResult(success=True, data=first_role)


def create_role(name: str, description: str | None) -> ServiceResult:
    cur = Cursor()

    first_role = cur.get_first_match(Role, Role.name, name)
    if first_role:
        error_message = f"Role with name={name} already exist"
        logger.info(f"Not possible to create role with name {name}, already exist")
        return ServiceResult(success=False, error_message=error_message)

    role = Role(name=name, description=description)
    cur.add(role)

    new_role = cur.get_first_match(Role, Role.name, name)
    logger.info(f"Role {new_role.uid} was created")

    return ServiceResult(success=True, data=new_role)


def update_role(role_id: UUID4, name: str | None, description: str | None) -> ServiceResult:
    cur = Cursor()

    first_role = cur.get_first_match(Role, Role.uid, role_id)
    if not first_role:
        error_message = f"Role with uuid={role_id} is not exist"
        return ServiceResult(success=False, error_message=error_message)

    if first_role.name == name:
        error_message = f"Role with name={name} alresdy exist"
        return ServiceResult(success=False, error_message=error_message)

    update_dict = {"name": name, "description": description}
    cur.update(Role, Role.uid, role_id, update_dict)

    updated_role = cur.get_first_match(Role, Role.uid, role_id)
    logger.info(f"Role {updated_role.uid} was updated")

    return ServiceResult(success=True, data=updated_role)


def delete_role(role_id: UUID4) -> ServiceResult:
    cur = Cursor()

    first_role = cur.get_first_match(Role, Role.uid, role_id)
    if not first_role:
        error_message = f"Role with uuid={role_id} is not exist"
        return ServiceResult(success=False, error_message=error_message)

    cur.delete(Role, Role.uid, role_id)
    return ServiceResult(success=True)
