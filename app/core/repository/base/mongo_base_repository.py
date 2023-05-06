import mongoengine
from pymongo.errors import ServerSelectionTimeoutError

from app.core.exceptions.app_exceptions import AppException
from app.core.repository.base.crud_repository_interface import CRUDRepositoryInterface


class MongoBaseRepository(CRUDRepositoryInterface):
    model: mongoengine

    def index(self):
        try:
            return self.model.objects()
        except mongoengine.OperationError:
            raise AppException.OperationError(error_message=None)

    def paginate(self, page: int, per_page: int):
        try:
            db_objs = self.model.objects.paginate(page=page, per_page=per_page)
            return db_objs.items
        except mongoengine.OperationError:
            raise AppException.OperationError(error_message=None)

    def create(self, obj_in):
        try:
            db_obj = self.model(**obj_in)
            db_obj.save()
            return db_obj
        except mongoengine.OperationError:
            raise AppException.OperationError(error_message="error create document")
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(error_message=e.details)

    def update_by_id(self, obj_id, obj_in):
        try:
            db_obj = self.find_by_id(obj_id)
            db_obj.modify(**obj_in)
            return db_obj
        except mongoengine.OperationError:
            raise AppException.OperationError(error_message="error updating document")
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(error_message=e.details)

    def update(self, filter_params, obj_in):
        try:
            db_obj = self.find(filter_params)
            db_obj.modify(**obj_in)
            return db_obj
        except mongoengine.OperationError:
            raise AppException.OperationError(error_message="error updating document")
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(error_message=e.details)

    def delete(self, query_params: dict):
        try:
            db_obj = self.find(query_params)
            db_obj.delete()
            return True
        except mongoengine.DoesNotExist:
            raise AppException.NotFoundException(
                error_message="document does not exist"
            )
        except mongoengine.OperationError:
            raise AppException.OperationError(error_message="error deleting document")
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(error_message=e.details)

    def delete_by_id(self, obj_id):
        try:
            db_obj = self.find_by_id(obj_id)
            db_obj.delete()
            return True
        except mongoengine.DoesNotExist:
            raise AppException.NotFoundException(
                error_message="document does not exist"
            )
        except mongoengine.OperationError:
            raise AppException.OperationError(error_message="error deleting document")
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(error_message=e.details)

    def find(self, filter_param):
        """
        returns an item that satisfies the data passed to it if it exists in
        the database

        :param filter_param: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        try:
            db_obj = self.model.objects.get(**filter_param)
            return db_obj
        except mongoengine.DoesNotExist:
            raise AppException.NotFoundException(error_message=None)

    def find_all(self, filter_param):
        """
        returns all items that satisfies the filter params passed to it

        :param filter_param: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.model.objects(**filter_param)
        return db_obj

    def find_by_id(self, obj_id):
        try:
            db_obj = self.model.objects.get(pk=obj_id)
            return db_obj
        except mongoengine.DoesNotExist:
            raise AppException.NotFoundException(error_message=None)
        except mongoengine.OperationError:
            raise AppException.OperationError(
                error_message="error querying for document"
            )
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(error_message=e.details)
        except mongoengine.ValidationError as e:
            raise AppException.OperationError(error_message=e.args)
