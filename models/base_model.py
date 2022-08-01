#!/usr/bin/python3


from datetime import datetime
import uuid


class BaseModel:
    """ Defines the new BaseModel class

    Attributes:
        id : The BaseModel id
        created_at: The datetime at creation
        updated_at: The datetime at last update

    """
    id = str(uuid.uuid4())
    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()

    def __init__(self):
        """Initialize a new Base Model
        """
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """String representation of the Base Model"""
        return "[{:s}] [{:s}] {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type((self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict
