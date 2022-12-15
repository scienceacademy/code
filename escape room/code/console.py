import time
from termcolor import colored
from getpass import getpass
import signal
from os import listdir, system
from os.path import isfile, join

def ctrl_c_handler(signum, frame):
    pass

system("clear")
# signal.signal(signal.SIGINT, ctrl_c_handler)

status = {
    "red": 5,
    "green": 5,
    "blue": 5,
    "black": 5
}
override_lock = 3
invalid_count = 0

override_code = "AAAA"
passwords = {
    "red": "qjka",
    "green": "flyer",
    "blue": "hands",
    "black": "iddqd"
}

messages = {
    "red": [
        "From: black\n a rubber duck is always a good way to debug a problem",
        "From: black\n I think they're onto us. Figure out a way to make it so that it takes all of us to disable the payload.",
        "From: blue\n measure the threads in imperial fashion",
    ],
    "black": [
        "From: blue\n I fixed the morse code problem",
        "From: red\n Security override will now require all 4 of us to execute",
    ],
    "green": [
        "From: red\n figured out your requested 'route' - check the file",
        "From: red\n if you follow the central strategy and count evenly, then your odds will be good"
        "From: black\n a rubber duck is always a good way to debug a problem",
    ],
    "blue": [
        "From: black\n a rubber duck is always a good way to debug a problem",
        "From: black\n That book idea was *Genius*.",
        "From: green\n you'll need a bunch of bands",
    ]
}

user = ""

def ls(cmd):
    if not user:
        print(colored("not logged in", "white", "on_red"))
        print()
        return
    print("Available files:")
    print()
    files = [f for f in listdir(f"./{user}")]
    for f in files:
        print(f)

def override(cmd):
    if not user:
        print(colored("you can't do that", "white", "on_red"))
        print()
        return

    # take input code, if wrong, 3 strikes(?)

def logout(cmd):
    global user
    if user:
        user = ""
        print("logged out")
        print()
    else:
        print(colored("not logged in", "white", "on_red"))
        print()

def login(cmd):
    global user
    if user:
        print("already logged in")
        print()
        return()
    if len(cmd) > 1:
        if cmd[1] in passwords:
            if status[cmd[1]] <= 0:
                print(colored("Account locked", "white", "on_red"))
                print()
                return
            pw = getpass("Password: ")
            if pw == passwords[cmd[1]]:
                print("hello", colored(cmd[1], attrs=["reverse"]))
                user = cmd[1]
                status[user] = 5
            else:
                status[cmd[1]] -= 1
                print("\a")
                print(colored(f"invalid pw - {status[cmd[1]]} tries remaining", "white", "on_red"))
                print()
        else:
            print(colored("invalid user", "white", "on_red"))
            print()
    else:
        print(colored("who?"))

def show(cmd):
    if len(cmd) < 2:
        print(colored("what file?", "white", "on_red"))
        return
    if not isfile(f"{user}/{cmd[1]}"):
        print(colored("invalid file", "white", "on_red"))
        return
    with open(f"{user}/{cmd[1]}") as f:
        for line in f:
            print(line.strip())
    print()

def help(cmd):
    print("Available commands (login for more): ")
    print()
    if user:
        print("msg              show messages")
        print("ls               list files")
        print("show <filename>  display file")
        print("logout           logout (duh)")
    else:
        print("login <name>     authenticate yourself")
        print("override         ", end="")
        print(colored("terminate attack", attrs=["reverse"]))
        return
    if user == "black":
        print("unlock <user>    unlock locked account")

def xyzzy(cmd):
    exit()

def msg(cmd):
    if not user:
        print(colored("not logged in", "white", "on_red"))
        return
    else:
        print()
        for msg in messages[user]:
            print(msg)
            print()

def unlock(cmd):
    if user != "black":
        return
    if len(cmd) > 1 and cmd[1] in passwords and status[cmd[1]] <= 0:
        status[cmd[1]] = 5
        print(colored("user unlocked", "white", "on_green"))
    else:
        print(colored("command failed", "white", "on_red"))


def override(cmd):
    global override_lock
    global done
    code = input("Enter override code: ")
    if code == override_code:
        if sure():
            print(colored("Attack canceled.", "green", attrs=["underline"]))
            done = True
            return
        else:
            return
    else:
        override_lock -= 1
        if override_lock <= 0:
            print(colored("Console lockout initiated", "red", "on_grey", attrs=["underline"]))
            return
        print(colored(f"Invalid override code - tries remaining: {override_lock}", "white", "on_red"))

def locked():
    print(colored(
        """



##        #######   ######  ##    ## ######## ########
##       ##     ## ##    ## ##   ##  ##       ##     ##
##       ##     ## ##       ##  ##   ##       ##     ##
##       ##     ## ##       #####    ######   ##     ##
##       ##     ## ##       ##  ##   ##       ##     ##
##       ##     ## ##    ## ##   ##  ##       ##     ##
########  #######   ######  ##    ## ######## ########



        """, "red"))

def sure():
    c = input("Are you sure you wish to cancel the attack (y/n)? ")
    if c.lower()[0] == 'y':
        return True
    return False

commands = [
    "ls",
    "override",
    "help",
    "login",
    "logout",
    "msg",
    "show",
    "unlock",
    "override",
    "xyzzy"
]

done = False
while not done:
    prompt = user + " Command: "
    cmd = input(prompt).split()
    if override_lock <= 0:
        locked()
        continue
    try:
        if cmd[0] in commands:
            globals()[cmd[0]](cmd)
            print()
        else:
            print(colored("invalid command", "white", "on_red"))
            invalid_count += 1
            if invalid_count > 5:
                print(colored("try 'help' :)", "white", "on_magenta"))
                invalid_count = 0
            print()
    except Exception as e:
        print(repr(e))
        pass

