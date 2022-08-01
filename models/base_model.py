#!/usr/bin/python3


from datetime import datetime
from models import storage
import uuid


class BaseModel:
    """ Defines the new BaseModel class

    Attributes:
        id : The BaseModel id
        created_at: The datetime at creation
        updated_at: The datetime at last update

    """

    def __init__(self, *args, **kwargs):
        """Initialize a new Base Model"""
        if kwargs is None or len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
            storage.new(self)
        else:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, time)
                elif key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """String representation of the Base Model"""
        classname = self.__class__.__name__
        return "[{:s}] [{:s}] {}".format(classname, self.id, self.__dict__)

    def save(self):
        """udates updated_at with the current time"""
        self.updated_at = datetime.utcnow()
        storage.save()

    def to_dict(self):
        """Creates a dictionary of BaseModel"""
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = type(self.__class__.__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict
