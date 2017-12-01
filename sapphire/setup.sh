#!/usr/bin/env bash

if [[ -z "$1" ]]
then
    echo "Usage: setup.sh PASSWORD"
    echo "       where PASSWORD is the Django app password"
    exit
fi

pword=$1

if [ -f "$HOME/.bash_profile" ]
then
    file="$HOME/.bash_profile"
elif [ -f "$HOME/.bashrc" ]
then
    file="$HOME/.bashrc"
else
    echo "Could not find .bash_profile or .bashrc files!"
    exit
fi

echo "export SKEY=\"${pword}\"" >> $file
echo "Added ENV Variable to $file"
