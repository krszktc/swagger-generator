from sqlalchemy.exc import IntegrityError

from resources.generated_models import Error, HttpError


def init_error_handler(app):

    @app.errorhandler(KeyError)
    def handle_invalid_usage(err):
        error_code = 400
        return HttpError(error=Error(
            detail="Wront Sex type. Use 'F' or 'M'",
            code=str(error_code),
            title='Bad Request',
            status='Wrong Type'
        )).dict(exclude_unset=True), error_code

    @app.errorhandler(IntegrityError)
    def handle_doube_email(err):
        error_code = 409
        return HttpError(error=Error(
            detail='Mail already exist',
            code=str(error_code),
            title='Bad Request',
            status='Duplicated Value'
        )).dict(exclude_unset=True), error_code

    @app.errorhandler(AttributeError)
    def handle_not_existing_id(err):
        error_code = 404
        return HttpError(error=Error(
            detail="Patient doesn\'t exist",
            code=str(error_code),
            title='Server Error',
            status='Missing Value'
        )).dict(exclude_unset=True), error_code
