#!/usr/bin/python3

import cmd

class HBNBCommand(cmd.Cmd):
    """command line terminal for HBNB"""

    prompt = '(hbnb) '

    def do_quit(self, line):
        """command to exit the command line"""
        return True

    def do_EOF(self, line):
        """command passes End Of File command
        to exit the command line"""
        return True
    
    def do_emptyline(self):
        """command to handle empty line"""
        print()

    def do_create(self, line):
        """create class instance based on class name
        Ex: create BaseModel"""
        pass

    def do_show(self, line):
        """Print string representation of a particular
        instance based on class name and id
        Ex: show BaseModel 1234-1234-1234"""
        pass

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
