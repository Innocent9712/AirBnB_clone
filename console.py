#!/usr/bin/python3

import cmd
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


class HBNBCommand(cmd.Cmd):
    """command line terminal for HBNB"""

    prompt = '(hbnb) '
    MODELS = [Amenity, BaseModel, City, Place, Review, State, User]

    def do_quit(self, line):
        """command to exit the command line"""
        return True

    def do_EOF(self, line):
        """command passes End Of File command
        to exit the command line"""
        return True

    def emptyline(self):
        """command to handle empty line"""
        pass

    def check_for_id(self, id_dict, id_instance):
        for id in id_dict:
            if id_instance == id.split(".")[1]:
                return 1
        else:
            return 0

    def do_create(self, line):
        """create class instance based on class name
        Ex: create BaseModel"""

        if (len(line) == 0):
            print('** class name missing **')
            return
        class_name = line.split()[0]
        for model in self.MODELS:
            if class_name == model.__name__:
                model_instance = model()
                print(model_instance.id)
                model_instance.save()
                return
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Print string representation of a particular
        instance based on class name and id
        Ex: show BaseModel 1234-1234-1234"""
        if (len(line) == 0):
            print('** class name missing **')
            return
        split_line = line.split()
        class_name = split_line[0]
        if len(split_line) > 1:
            model_id = split_line[1]
        else:
            print("** instance id missing **")
            return

        for model in self.MODELS:
            if class_name == model.__name__:
                storage.reload()
                files = storage.all()
                for k in files:
                    split_key = k.split(".")
                    if split_key[0] == class_name and split_key[1] == model_id:
                        model_instance = model(**files[k].to_dict())
                        print(model_instance)
                        return
                else:
                    print("** no instance found **")
                    return
        else:
            print("** class doesn't exist **")

    def do_destroy(self, line):
        """Delete instance based on class name and id
        Ex: destroy BaseModel 1234-1234-1234"""
        if (len(line) == 0):
            print('** class name missing **')
            return
        split_line = line.split()
        class_name = split_line[0]
        if len(split_line) > 1:
            model_id = split_line[1]
        else:
            print("** instance id missing **")
            return

        for model in self.MODELS:
            if class_name == model.__name__:
                storage.reload()
                files = storage.all()
                filter = dict()
                if self.check_for_id(files.keys(), model_id):
                    for k in files.keys():
                        if model_id not in k:
                            filter[k] = files[k].to_dict()
                    with open("file.json", mode='w') as json_file:
                        json.dump(filter, json_file)
                else:
                    print("** no instance found **")
                return
        else:
            print("** class doesn't exist **")

    def do_all(self, line):
        """Print string representation of all
        instance based or not on class name
        Ex: all BaseModel or all"""
        my_list = []
        storage.reload()
        files = storage.all()
        if line:
            class_name = line.split()[0]
            for model in self.MODELS:
                if class_name == model.__name__:
                    for item in files:
                        sub_items = files[item].to_dict()
                        if sub_items["__class__"] == class_name:
                            sub_instance = model(**sub_items)
                            my_list.append(str(sub_instance))
                    print(my_list)
                    return
            else:
                print("** class doesn't exist **")
        else:
            for item in files:
                sub_items = files[item].to_dict()
                for model in self.MODELS:
                    if sub_items["__class__"] == model.__name__:
                        sub_instance = model(**sub_items)
                        my_list.append(str(sub_instance))
            print(my_list)

    def do_update(self, line):
        """update an instance based on class name and id
        updating existing attributes or adding new ones
        Ex: update BaseModel 1234-1234-1234 email 'aibnb@mail.com'"""
        if (len(line) == 0):
            print('** class name missing **')
            return
        split_line = line.split()
        class_name = split_line[0]
        if len(split_line) > 1:
            model_id = split_line[1]
        else:
            print("** instance id missing **")
            return

        for model in self.MODELS:
            if class_name == model.__name__:
                # storage.reload()
                files = storage.all()
                for k in files:
                    split_key = k.split(".")
                    if split_key[0] == class_name and split_key[1] == model_id:
                        model_instance = model(**files[k].to_dict())
                        if len(split_line) > 2:
                            attr = split_line[2]
                        else:
                            print("** attribute name missing **")
                            return
                        print(len(split_line))
                        if len(split_line) > 3:
                            value = split_line[3]
                        else:
                            print("** value missing **")
                            return
                        setattr(model_instance, attr, value)

                        storage.reload()
                        files = storage.all()
                        update = dict()
                        for k in files.keys():
                            if model_instance.id in k:
                                update[k] = model_instance.to_dict()
                            else:
                                update[k] = files[k].to_dict()
                        with open("file.json", mode='w') as json_file:
                            json.dump(update, json_file)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
