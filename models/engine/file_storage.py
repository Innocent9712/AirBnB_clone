#!/usr/bin/python3
"""File Storage for AirBnb Console"""
import json
from os.path import exists
from ..base_model import BaseModel


class FileStorage():
    """Defines a Class for Filestorage"""

    __file_path = "file.json"
    __objects = dict()

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        self.__objects[obj.__clas__.__name__ + "." + obj.id] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path  
        """
        temp = dict()
        for keys in self.__objects.keys():
            temp[keys] = self.__objects[keys].dict()
        with open(self.__file_path, mode='w') as json_file:
            json.dump(temp, json_file)

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file (__file_path) 
        exists ; otherwise, do nothing. If the file doesn't exist, no exception should be raised)  
        """

        if exists(self.__file_path):
            with open(self.__file_path) as json_file:
                deserialize = json.load(json_file)
        for keys in deserialize.keys():
            if deserialize[keys]['__class__'] == 'BaseModel':
                self.__objects[keys] = BaseModel(**deserialize[keys])
