from pydantic import UUID4
from src.api.v1.models import UpdateUser
from src.core import logger
from src.db.models import LoginHistory, User
from src.services.db_manager import Cursor
from src.services.models import ServiceResult

cur = Cursor()


class UserCrud:
    def get_user_info(self, user_id: UUID4):
        result = cur.get_user(User, User.uid, user_id)
        if result is None:
            error_message = "User not found"
            logger.info("User not found")
            return ServiceResult(success=False, error_message=error_message)
        logger.info("User discovered")
        return ServiceResult(success=True, data=result)

    def delete_user(self, user_id: UUID4):
        result_data = cur.get_user(User, User.uid, user_id)
        if result_data is None:
            error_message = "User not found"
            logger.info("User not found")
            return ServiceResult(success=False, error_message=error_message)
        cur.delete_user(User, User.uid, user_id, result_data)
        logger.info(f"User {result_data.first_name, result_data.last_name} deleted")
        return ServiceResult(success=True, data="Success")

    def update_user_info(self, user_id: UUID4, body: UpdateUser):
        result_data = cur.get_user(User, User.uid, user_id)
        if result_data is None:
            error_message = "User not found"
            logger.info("User not found")
            return ServiceResult(success=False, error_message=error_message)
        result = cur.update_user(User, User.uid, user_id, body, result_data)
        logger.info(f"User {result_data.first_name, result_data.last_name} updated")
        return ServiceResult(success=True, data=result)

    def get_login_history(self, user_id):
        result = cur.get_all_items_by_id(LoginHistory, LoginHistory.user_id, user_id)
        if result is None:
            error_message = ""
            logger.info("User was not logging yet")
            return ServiceResult(success=False, error_message=error_message)
        logger.info("User discovered")
        return ServiceResult(success=True, data=result)
