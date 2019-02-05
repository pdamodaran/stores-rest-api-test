from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
    Function that gets called when the user calls the /auth endpoing
    with their username and password
    :param username: username in string format
    :param password: un-encrypted password in string format
    :return: A UserModel object if authentication was successful, None otherwise
    """

    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user
    return None


def identity(payload):
    """
    Function that gets called when user has already authenticated, and Flask-JWT
    verified their authentication header is correct
    :param payload: a dictionary with 'identity' key, which is the user id
    :return: a UserModel objec
    """

    user_id = payload['identity']
    return UserModel.find_by_id(user_id)