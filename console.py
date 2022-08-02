#!/usr/bin/python3

import cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """command line terminal for HBNB"""

    prompt = '(hbnb) '
    MODELS = [BaseModel]

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
        pass

    def do_all(self, line):
        """Print string representation of all
        instance based or not on class name
        Ex: all BaseModel or all"""
        pass

    def do_update(self, line):
        """update an instance based on class name and id
        updating existing attributes or adding new ones
        Ex: update BaseModel 1234-1234-1234 email 'aibnb@mail.com'"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
