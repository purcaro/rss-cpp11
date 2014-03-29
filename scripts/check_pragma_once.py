#!/usr/bin/python

import os

cwd = os.getcwd()
path = "~/weng-lab/"
path = os.path.expanduser(path)
os.chdir(path)

regex = '-regex ".*\.[hH]\(pp\)?"'
exclude = '-not -path "*/external/*" -not -name "*#*"'
cmd = 'find  {p} {r} {e} -exec head -n 1 {{}} \;'.format(p=path, e=exclude, r=regex)

print cmd

os.system(cmd)

os.chdir(cwd)
