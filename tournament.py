#for generating the tournaments for the bots
from tqdm import tqdm
import os, os.path
import random
import copy
from pprint import pprint

class fighter():
    def __init__(self, name:str):
        self.name = name
        self.matches = dict()
        self.opponents = []
    def __str__(self) -> str:
        return f'fighter: {self.name} opponents: {self.opponents} matches: {self.matches.keys()}'

class match():
    def __init__(self, opponent:str):
        self.opponent = opponent
        self.finished = False
        self.score = 0
        self.won = None
    def __str__(self) -> str:
        return f'opponent: {self.opponent}' + (('outcome: ' + ('won' if self.won else 'lost' if not self.won else 'drew')) if self.finished else 'not yet completed')

class NoMatchesLeft(Exception):
    "Raised when there are no more matches left to play"
    pass

def get_random_match(remaining_opponents:list,competitor:fighter):
    while len(remaining_opponents) > 10:
        opponent_name = random.choice(remaining_opponents)
        if opponent_name not in competitor.opponents:
            remaining_opponents.remove(opponent_name)
            competitor.matches[opponent_name] =(match(opponent_name))
            competitor.opponents.append(opponent_name)
            return opponent_name
    # print('competitor opponents: ', competitor.opponents)
    not_touched_opponents = [opp for opp in remaining_opponents if opp not in competitor.opponents]
    if len(not_touched_opponents) == 0:
        raise NoMatchesLeft
    opponent_name = random.choice(not_touched_opponents)
    remaining_opponents.remove(opponent_name)
    competitor.matches[opponent_name] =(match(opponent_name))
    competitor.opponents.append(opponent_name)
    return opponent_name

def make_round_robin(relative_path:str,num_rounds:int=3,debug:bool=False):
    images = [image for index,image in enumerate(os.listdir(os.path.dirname(__file__) + relative_path)) if (index%1000)==0]
    assert len(images)%2 == 0, 'Not even steven'
    
    #not all of the permutations are good, so we try until we get a valid round robin
    while True:
        try:
            round_robin = dict(zip(images,[fighter(image) for image in images]))
            game_queue = []
            for i in range(num_rounds):
                copy_of_images = copy.deepcopy(images)
                while len(copy_of_images) != 0:
                    #generate a random match for the competitor
                    fighter_name = copy_of_images.pop()
                    opponent_name = get_random_match(copy_of_images,round_robin[fighter_name])
                    #update the opponent
                    round_robin[opponent_name].opponents.append(fighter_name)
                    round_robin[opponent_name].matches[fighter_name] = match(fighter_name)
                    #add game to game queue
                    game_queue.append((fighter_name,opponent_name))
            break
        except NoMatchesLeft:
            print('trying again')
    return (game_queue,round_robin)


def run_round_robin():
    pass

run_round_robin()