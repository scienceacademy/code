import random
import os
import sys
import glob
from itertools import combinations

save_file = "bot_results.csv"

if len(sys.argv) != 2:
    sys.exit("Usage: python pig_contest.py N")
N = int(sys.argv[1])

class Bot:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.score = 0
        self.round_score = 0
    def __repr__(self):
        return self.name

# files = [os.path.splitext(f)[0] for f in glob.glob("bot*.py")]
bot_path = "/Users/chris/tmp/pig_bots"
sys.path.append(bot_path)
files = [os.path.splitext(f)[0].split("/")[-1] for f in glob.glob(f"{bot_path}/bot*.py")]
bots = []

for f in files:
    bots.append(Bot(f[4:], __import__(f)))

# print(sorted([bot.name for bot in bots]))
# exit()

print(f"{len(bots)} bots loaded")

# Test all bots
for player in bots:
    try:
        result = player.code.choice(2, 0, 0)
        result = player.code.choice(2, 90, 0)
        result = player.code.choice(10, 90, 50)
    except Exception as e:
        # sys.exit(f"Error in: {player.name}, {i}")
        print(f"Error in: {player.name}, {e} - removed")
        bots.remove(player)

def show_scores(players):
    # Call this to print out the scores
    print("-" * 20)
    print(f"{players[0].name}: {players[0].score}")
    print(f"{players[1].name}: {players[1].score}")
    print("-" * 20)

def player_choice(player, opp):
    # TODO: return True if the player wants to roll again
    #       return False if the player wants to hold
    result = player.code.choice(player.round_score, player.score, opp)
    return result

def take_turn(player, opp_score):
    player.round_score = 0
    while True:
        # TODO: implement the rules of the game (see instructions)
        roll = random.randint(1, 6)
        # print(f"Roll: {roll}")
        if roll == 1:
            player.round_score = 0
            break
        else:
            player.round_score += roll
            # print(f"Points earned this turn: {round_score}")
            if not player_choice(player, opp_score):
                break
    player.score += player.round_score
    # print(f"Points earned this turn: {player.round_score}")
    # input("Turn is over. Press <Enter> to continue.")


#This loop will alternate between players taking turns
def play_game(p1, p2):
    turn = 0
    players = [p1, p2]
    p1.score, p2.score = 0, 0
    playing = True  # set this to False when the game ends
    n = 1
    while playing:
        # os.system("clear")
        # show_scores(players)
        take_turn(players[turn], players[1 if turn==0 else 0].score)
        if players[turn].score > 100:
            playing = False
        turn = 1 if turn == 0 else 0
        n += 1
        if n >= 1000:
            print(f"timeout: {p1.name}: {p1.score}, {p2.name}: {p2.score}")
            playing = False
    # print("Final scores:")
    # show_scores(players)

#load win_record here
win_record = {}
try:
    with open(save_file, "r") as f:
        for line in f:
            name, w, l = line.split(",")
            win_record[name] = [int(w), int(l)]
except FileNotFoundError:
    pass

# win_record = {bot.name: [0, 0] for bot in bots}
combs = list(combinations(bots, 2))
for i in range(N):
    for a, b in combs:
        if random.random() > 0.5:
            b, a = a, b
        if a.name not in win_record:
            win_record[a.name] = [0, 0]
        if b.name not in win_record:
            win_record[b.name] = [0, 0]
        play_game(a, b)
        if a.score > b.score:
            win_record[a.name][0] += 1
            win_record[b.name][1] += 1
        elif b.score > a.score:
            win_record[a.name][1] += 1
            win_record[b.name][0] += 1


# print(win_record)
with open(save_file, "w") as f:
    for name in win_record:
        w, l = win_record[name]
        f.write(f"{name},{w},{l}\n")