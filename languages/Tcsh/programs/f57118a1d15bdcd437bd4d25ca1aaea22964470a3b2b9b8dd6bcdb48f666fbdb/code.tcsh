#!/bin/tcsh
set prompt="%n@%m:%~%# "
set time=(8 "CPU %U USER %S SYSTEM %E ELAPSED %P RATIO")
set history=1000
set savehist=(1000 merge)
set autolist=ambiguous
set autoexpand
set autorehash
set mail=/var/mail/$USER
set correct=cmd
set filec

# System information display
echo "System Information:"
echo "----------------"
echo "Hostname: `hostname`"
echo "OS: `uname -s`"
echo "Kernel: `uname -r`"
echo "Architecture: `uname -m`"
echo "Current User: $USER"
echo "Shell: $shell"
echo "Home Directory: $home"
echo "Current Directory: $cwd"

# Load average
echo "\nSystem Load:"
uptime