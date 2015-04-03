#!/usr/bin/env python
import os
import sys

appendedpath = r"../../.." # include django_wsgiserver on the path"
sys.path.append(appendedpath)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdjango.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
