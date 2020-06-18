"""
File to handle user related API resources
"""


class UserModel:
    """
    Simple user class model
    """
    def __init__(self, _id, username, password):
        """
        :param _id: int
        :param username: str
        :param password: str
        """
        self.id = _id
        self.username = username
        self.password = password
