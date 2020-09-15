#!/usr/bin/env python3

import sys, getopt, os
import urllib.request
from os.path import expanduser
import tempfile
from shutil import copyfile
import difflib
# from difflib_data import *
from pathlib import Path
import filecmp
import re

ACCEPT_CHANGES=False
GIT_ROOT='https://raw.githubusercontent.com/nicolascochin/setup_env/master'
GIT_CONFIG_SRC=GIT_ROOT + '/git/.gitconfig'
GIT_CONFIG_DEST=expanduser("~/.gitconfig")
ZSH_CONFIG_SRC=GIT_ROOT + '/shell/.zshrc'
ZSH_CONFIG_DEST=expanduser("~/.zshrc")
P10K_CONFIG_SRC=GIT_ROOT + '/shell/.p10k.zsh'
P10K_CONFIG_DEST=expanduser("~/.p10k.zsh")
VIM_CONFIG_SRC=GIT_ROOT + '/vim/.vimrc'
VIM_CONFIG_DEST=expanduser("~/.vimrc")

PLUGINS = {
    "common": ["jira", "zsh_reload", "catimg", "colorize", "git", "common-aliases"],
    "mac": ["dash", "osx"],
    "ruby": ["another"]
}

"""The classical usage method"""
def usage(error_code=0):
    print(f'init_env.py [options]')
    print('')
    print('Options')
    print('  -t --target <target>       One of {targets}'.format(targets=PLUGINS.keys()))
    print('  -e --email <email>         The git email to use')
    print('  -y                         Accept all changes')
    sys.exit(error_code)

"""Check the the given cadidates are all known plugins (a key in PLUGINS map)"""
def validate_params(candidates, email):
    allowed_keys = PLUGINS.keys()
    for item in candidates: 
        if item not in allowed_keys :
            print(f'{item} is not an allowed key')
            usage(1)
    if len(email) == 0: 
        print(f'email is mandatory')
        usage(1)

"""Get the params from the CLI"""
def get_params(args):
    targets=[]
    email=''
    try:
        opts, args = getopt.getopt(args,"yhe:t:",["target=", "email=", "help"])
    except getopt.GetoptError:
        usage(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        if opt in ("-y"):
            ACCEPT_CHANGES=True
        elif opt in ("-t", "--target"):
            targets.append(arg)
        elif opt in ("-e", "--email"):
            email = arg
    validate_params(targets, email)
    return targets, email

def replace_file(old, new):
    copyfile(old, new)

def retrieve_remote_file_to_tmp_file(url):
    tmp = tempfile.NamedTemporaryFile()
    print('Getting file from the repo')
    urllib.request.urlretrieve(url, tmp.name)
    return tmp

def print_file_differences(f1, f2):
    with open (f1, "r") as myfile:
        actual=myfile.readlines()
    with open (f2, "r") as myfile:
        new=myfile.readlines()
    for line in difflib.context_diff(actual, new, fromfile=f1, tofile=f2):
        sys.stdout.write(line) 
    if ACCEPT_CHANGES: 
        return true
    while True:
        user_input = input('Override the local file? (y/n)')
        if re.match(r"^y|n$", user_input):
            break
        continue
    return user_input == 'y'

def get_remote_file(url, dest_file, callback=None):
    tmp = retrieve_remote_file_to_tmp_file(url)
    if callback is not None: 
        callback(tmp)
    if not os.path.exists(dest_file):
        print(f'{dest_file} does not exists. Creating it...')
        replace_file(tmp.name, dest_file)
    else: 
        print(f'{dest_file} does exists. Checking diff...')
        if filecmp.cmp(dest_file, tmp.name, shallow=True):
            print('They are no differences')
        else: 
            if print_file_differences(dest_file, tmp.name): 
                print('Replacing the file...')
                replace_file(tmp.name, dest_file)
            else: 
                print('Skipping')

def replace_file_content(file, pattern, replacement):
    with open(file) as f:
        file_str = f.read()

    file_str = re.sub(pattern, replacement, file_str)
    with open(file, "w") as f:
        f.write(file_str)

def setup_git_config(email):
    print('=============== Setup git config ===============')
    get_remote_file(GIT_CONFIG_SRC, GIT_CONFIG_DEST, lambda tmpFile: replace_file_content(tmpFile.name, r'\bXXX\b', email))
    print('=============== Done ===============')

def setup_vim_config():
    print('=============== Setup vim config ===============')
    get_remote_file(VIM_CONFIG_SRC, VIM_CONFIG_DEST)
    print('Install Vundle')
    os.system('if [ ! -d ~/.vim/bundle/Vundle.vim ]; then git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim; fi')
    print('=============== Done ===============')


def setup_shell_config(keys):
    print('=============== Setup shell config ===============')
    print('Install Oh my ZSH')
    os.system('curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sh')
    print('Install powerlevel10k')
    os.system('git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k')
    print('Get my zshrc config')
    get_remote_file(ZSH_CONFIG_SRC, ZSH_CONFIG_DEST, lambda tmpFile: replace_file_content(tmpFile.name, r'\bPLUGINS\b', get_zsh_plugins(keys)))
    get_remote_file(P10K_CONFIG_SRC, P10K_CONFIG_DEST)
    print('=============== Done ===============')   

def get_zsh_plugins(keys):
    plugins = set()
    for key in keys: 
        plugins.update(PLUGINS[key])
    res = list(plugins)
    res.sort()
    return ' '.join(res)

def main(argv):
    keys,email = get_params(argv)
    setup_git_config(email)
    setup_shell_config(keys)
    setup_vim_config()

if __name__ == "__main__":
   main(sys.argv[1:])
