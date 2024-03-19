
import sys
# setting path
sys.path.append('..\\')
import battle
from cnn import ImageCompressor
from PIL import Image
import os.path
from gensim.matutils import unitvec
from gensim.models import Word2Vec
from matplotlib import pyplot as plt
import numpy as np
tp_ff = ImageCompressor()

fighter_1 = Image.open("%s/../video_processing/jjk_images/S1_(2)/frame1248.png" % os.path.dirname(__file__))
imageData = battle.imgToTensor(fighter_1)
fighter_1_vec = unitvec(np.array(tp_ff(imageData)))

fighter_2 = Image.open("%s/../video_processing/jjk_images/S1_(5)/frame11962.png" % os.path.dirname(__file__))
imageData = battle.imgToTensor(fighter_2)
fighter_2_vec = unitvec(np.array(tp_ff(imageData)))
print('matchup: fighter1\n', len(fighter_1_vec),'\nfighter2\n',len(fighter_2_vec))

def simple_console_log_tests():
    print('Starting the test suite')
    print('outcome of the game, simple :', battle.simulate_game_without_pgn(fighter_1_vec,fighter_2_vec))
    # print('outcome of the game, simple with stockfish intervention :', battle.simulate_game_without_pgn_with_stockfish_intervention(fighter_1_vec,fighter_2_vec,20))

def test_pgn_out():
    print('Starting the game')
    winner, num_moves, pgn_game = battle.simulate_game_with_pgn(fighter_1_vec,fighter_2_vec)
    print('outcome of the game: %s after %d moves' % (winner,num_moves))
    battle.writeback_pgn(pgn_game,'./test_pgn.pgn','ep_2_frame1248.png','ep_2_frame11962.png')

def test_stockfish_analysis():
    print('Starting the game')
    winner, num_moves, pgn_game, adv, mating = battle.simulate_game_with_stockfish_analysis(fighter_1_vec,fighter_2_vec)
    print('outcome of the game: ', winner)
    # battle.writeback_pgn(pgn_game,'test_game.pgn')
    battle.plot_advantage_and_mating_of_game(adv,mating)


test_pgn_out()
# test_stockfish_analysis()