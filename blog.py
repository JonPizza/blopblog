#!/usr/bin/python3
from sys import argv
import subprocess as sp
from glob import glob
import webbrowser

def display_help():
    commands = [
        ('-n', 'Create a new post', '-n <POST ID>'),
        ('-a', 'Add idea to a post', '-a <IDEA> <POST ID>'),
        ('-e', 'Edit a post', '-e <POST ID>'),
        ('-l', 'Add link to a post', '-l <URL> <POST ID>'),
        ('--list/-i', 'List all posts', '--list'),
        ('-r', 'Read a post', '-r <POST ID>'),
        ('-x/-e', 'Export a post to https://jon.network', '-x <POST ID>'),
        ('-h', 'Help', '-h')]
    for command in commands:
        print(
            f'COMMAND: {command[0].center(10)} | USAGE: "blog.py {command[2]}" | {command[1]}')


def add_link(post=None, link=None):
    try:
        link = argv[2] if not link else link
        post = argv[3] if not post else post
    except IndexError:
        display_help()
        print(
            '\nYou did not supply a post id or a link!\nUSAGE: blog.py -l <URL> <POST ID>')
        return
    with open(f'posts/{post}.txt', 'a') as f:
        f.write(f'\nA link I found helpful: [{link}]({link})\n')


def add_post_idea(post=None, idea=None):
    try:
        idea = argv[2] if not idea else idea
        post = argv[3] if not post else post
    except IndexError:
        display_help()
        print(
            '\nYou did not supply a post id or a idea!\nUSAGE: blog.py -a <IDEA> <POST ID>')
        return
    if post not in [p.replace('posts/', '').replace('.txt', '') for p in glob('posts/*')]:
        print(f'Warning: Post {post} did not exsist before')

    with open(f'posts/{post}.txt', 'a') as f:
        f.write(f'\n{idea}\n')
    read(post)


def add_new_post(post=None):
    try:
        post = argv[2] if not post else post
    except IndexError:
        display_help()
        print('\nYou did not supply a post id! (a post ID is a short, memorable string to access your posts with)\nUSAGE: blog.py -n <POST ID>')
        return
    sp.call(['touch', f'posts/{post}.txt'])


def edit_post(post=None):
    try:
        post = argv[2] if not post else post
    except IndexError:
        display_help()
        print('\nYou did not supply a post id!\nUSAGE: blog.py -e <POST ID>')
        return
    sp.call(['nano', f'posts/{post}.txt'])


def list_posts():
    filenames = glob('posts/*')
    if len(filenames) == 0:
        print('None yet!')
    for filename in filenames:
        filename = filename.replace('.txt', '').replace('posts/', '')
        print(filename)


def read(post=None):
    try:
        post = argv[2] if not post else post
    except IndexError:
        display_help()
        print('\nYou did not supply a post id!\nUSAGE: blog.py -a <POST ID>')
        return
    with open(f'posts/{post}.txt', 'r') as f:
        print(f.read())


def export_to_jonnetwork(post=None):
    try:
        post = argv[2] if not post else post
    except IndexError:
        display_help()
        print('\nYou did not supply a post id!\nUSAGE: blog.py -x <POST ID>')
        return
    with open(f'posts/{post}.txt') as p:
        body = p.read().replace('\n', '%0A').replace(' ', '%20').replace('#', '%23').replace('?', '%3F')
    webbrowser.open(f'https://jon.network/programming/share/?body={body}', new=2)
    


def main():
    try:
        command = argv[1]
    except IndexError:
        display_help()
        return

    if command == '-h':
        display_help()
    elif command == '-a':
        add_post_idea()
    elif command == '-n':
        add_new_post()
    elif command == '-e':
        edit_post()
    elif command == '-l':
        add_link()
    elif command == '-r':
        read()
    elif command == '-e' or command == '-x':
        export_to_jonnetwork()
    elif command == '--list' or command == '-i':
        list_posts()
    else:
        display_help()
        print(f'\nUnknown Option: {command}')


if __name__ == '__main__':
    main()
