# -*- coding: utf-8 -*-
from automatictime.cli import Command

if __name__ == "__main__":
    cmd = Command()
    cmd.add_arguments()
    options = cmd.parse()
    cmd.handle(options)
