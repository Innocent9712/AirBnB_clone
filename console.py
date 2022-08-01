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
        print()

    def do_create(self, line):
        pass

    def do_show(self, line):
        pass

    def do_destroy(self, line):
        pass

    def do_all(self, line):
        pass

    def do_update(self, line):
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
