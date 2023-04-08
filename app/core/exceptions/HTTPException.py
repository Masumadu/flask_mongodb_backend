from flask import current_app
from werkzeug.exceptions import HTTPException as WerkzeugHttpException


class HTTPException(WerkzeugHttpException):
    def __init__(self, status_code, description=None):
        self.code = status_code
        current_app.logger.error(description)
        super(HTTPException, self).__init__(description=description)
