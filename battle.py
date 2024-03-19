#for simulating the battles between two chess engines in 300 dimension vector form

import chess
import chess.pgn
import numpy as np
import random
from matplotlib import pyplot as plt
import os.path
from datetime import datetime
########################################
from gensim.matutils import unitvec
from gensim.models import Word2Vec
import nltk
nltk.download('punkt',quiet=True)
model = Word2Vec.load('%s/gensim_models/chess_model_2.bin' % os.path.dirname(__file__))
########################################
from torchvision import transforms
imgToTensor = transforms.ToTensor()
tensorToimg = transforms.ToPILImage()
########################################
# stock fish is not to be used as a board, as it can be written over in any function
from stockfish import Stockfish
stockfish = Stockfish("%s/chess-engines/stockfish/stockfish-windows-x86-64-avx2.exe" % os.path.dirname(__file__))
stockfish.set_elo_rating(3100)
########################################

########################################
#         timing decorator             #
########################################
from time import time
def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func

########################################

@timer_func
def simulate_game_without_pgn(fighter_1:np.array,fighter_2:np.array, verbose:bool=False) -> tuple[str,int]:
    """most basic form of simulating games between two arrays

    Args:
        fighter_1 (np.array): the first 300 element array
        fighter_2 (np.array): the second 300 element array
        verbose (bool, optional): Prints more info to the console. Defaults to False.

    Returns:
        tuple[str,int]: (outcome of the match, number of moves)
    """
    board = init_game()
    first_move = True
    num_moves = 1
    while not board.is_game_over():
        #assuming that white is always fighter_1, we can use the mapping of board.turn (True -> White, False -> Black)
        move = find_optimal_move_given_array(board,fighter_1) if board.turn else find_optimal_move_given_array(board,fighter_2)
        board.push(move)
        num_moves += 1 if board.turn else 0
        if verbose:
            print('board state: ', board.fen())
    result = board.result()
    if verbose:
        print('outcome of the game: ',result)
    outcome = 'W' if result=='1-0' else 'B' if result =='0-1' else 'D'
    return (outcome, num_moves)

@timer_func
def simulate_game_with_pgn(fighter_1:np.array,fighter_2:np.array, verbose:bool=False):
    board = init_game()
    pgn_game = chess.pgn.Game()
    first_move = True
    num_moves = 1
    while not board.is_game_over():
        move = find_optimal_move_given_array(board,fighter_1) if board.turn else find_optimal_move_given_array(board,fighter_2)
        board.push(move)
        num_moves += 1 if board.turn else 0
        #make pgn
        node = pgn_game.add_variation(move) if (num_moves == 1 and not board.turn) else node.add_variation(move)
        #####################################
        if verbose:
            print('board state: ', board.fen())
    result = board.result()
    if verbose:
        print('outcome of the game: ',result)
        print(pgn_game)
    outcome = 'W' if result=='1-0' else 'B' if result =='0-1' else 'D'
    return(outcome, num_moves,pgn_game)


@timer_func
def simulate_game_without_pgn_with_stockfish_intervention(fighter_1:np.array,fighter_2:np.array, stockfish_rate: int = 6, verbose:bool=False) -> tuple[str,int]:
    """most basic form of simulating games between two arrays, will force one or both of the teams to come out ontop

    Args:
        fighter_1 (np.array): the first 300 element array
        fighter_2 (np.array): the second 300 element array
        stockfish_rate (int,optional): stockfish will make a move once every nth moves (1 means that it is only stockfish playing)
        verbose (bool, optional): Prints more info to the console. Defaults to False.

    Returns:
        tuple[str,int]: (outcome of the match, number of moves)
    """
    board = init_game()
    first_move = True
    num_moves = 1
    while not board.is_game_over():
        #stockfish moves for white every num_moves mod rate = rate//2, stockfish moves for black every num_moves mod rate = 0
        if (((num_moves % stockfish_rate) != 0) and not board.turn) or (((num_moves % stockfish_rate) != stockfish_rate//2) and board.turn):
            move = find_optimal_move_given_array(board,fighter_1) if board.turn else find_optimal_move_given_array(board,fighter_2)
            board.push(move)
        else:
            move = let_stockfish_decide_move(board)
            board.push_san(move)
        num_moves += 1 if board.turn else 0
        if verbose:
            print('board state: ', board.fen())
    result = board.result()
    if verbose:
        print('outcome of the game: ',result)
    outcome = 'W' if result=='1-0' else 'B' if result =='0-1' else 'D'
    return (outcome, num_moves)


@timer_func
def simulate_game_with_stockfish_analysis(fighter_1:np.array,fighter_2:np.array,verbose:bool=False):
    board = init_game()
    stockfish.set_fen_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    pgn_game = chess.pgn.Game()
    first_move = True
    advantage_over_time = []
    mating_chances= []
    num_moves = 1
    while not board.is_game_over():
        move = find_optimal_move_given_array(board,fighter_1) if board.turn else find_optimal_move_given_array(board,fighter_2)
        board.push(move)
        num_moves += 1 if board.turn else 0
        ################
        #stockfish
        stockfish.make_moves_from_current_position([move.uci()])
        eval = stockfish.get_evaluation()
        advantage_over_time.append(eval['value'] if eval['type'] == 'cp' else 0)
        mating_chances.append(eval['value'] if eval['type'] == 'mate' else 0)
        ###############

        #make pgn
        node = pgn_game.add_variation(move) if (num_moves == 1 and not board.turn) else node.add_variation(move)
        if verbose:
            print('board state: ', board.fen())
    result = board.result()
    if verbose:
        print('outcome of the game: ',result)
        print(pgn_game)
    outcome = 'W' if result=='1-0' else 'B' if result =='0-1' else 'D'
    return(outcome,num_moves,pgn_game,advantage_over_time,mating_chances)

@timer_func
def simulate_game_with_stockfish_analysis_and_intervention(fighter_1:np.array,fighter_2:np.array, stockfish_rate: int = 6,verbose:bool=False):
    board = init_game()
    stockfish.set_fen_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    pgn_game = chess.pgn.Game()
    first_move = True
    advantage_over_time = []
    mating_chances= []
    num_moves = 1
    while not board.is_game_over():
        if (((num_moves % stockfish_rate) != 0) and not board.turn) or (((num_moves % stockfish_rate) != stockfish_rate//2) and board.turn):
            move = find_optimal_move_given_array(board,fighter_1) if board.turn else find_optimal_move_given_array(board,fighter_2)
            board.push(move)
        else:
            move = let_stockfish_decide_move(board)
            board.push_san(move)
        num_moves += 1 if board.turn else 0
        ################
        #stockfish
        stockfish.make_moves_from_current_position([move.uci()])
        eval = stockfish.get_evaluation()
        advantage_over_time.append(eval['value'] if eval['type'] == 'cp' else 0)
        mating_chances.append(eval['value'] if eval['type'] == 'mate' else 0)
        ###############

        #make pgn
        node = pgn_game.add_variation(move) if (num_moves == 1 and not board.turn) else node.add_variation(move)
        if verbose:
            print('board state: ', board.fen())
    result = board.result()
    if verbose:
        print('outcome of the game: ',result)
        print(pgn_game)
    outcome = 'W' if result=='1-0' else 'B' if result =='0-1' else 'D'
    return(outcome,num_moves,pgn_game,advantage_over_time,mating_chances)


def init_game() ->chess.Board:
    return chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

def chose_random_move(board:chess.Board) -> chess.Move:
    return random.choice(list(board.legal_moves))

def let_stockfish_decide_move(board:chess.Board) -> str:
    stockfish.set_fen_position(board.fen())
    return stockfish.get_best_move()

# @timer_func
def get_all_fen(board:chess.Board, verbose: bool = False) -> list:
    """
    Get all of the available positions that the chess board could be in next turn
    """
    all_fen = []
    avail_moves = list(board.legal_moves)
    for cur_move in avail_moves:
        board.push(cur_move)
        cur_fen = board.fen()
        board.pop()
        all_fen.append(cur_fen)
    if verbose:
        print('Function get all fen\'s output: ')
        print('avail_moves: ', cur_move)
        print('all_fen: ', all_fen)
    return (avail_moves,all_fen)

# @timer_func
def find_optimal_move_given_array(board:chess.Board,fighter:np.array,verbose:bool=False):
    avail_moves, all_fen = get_all_fen(board)
    #retrain model to include the new fen
    model.build_vocab([all_fen], update=True)
    # model.train([all_fen], total_examples=model.corpus_count, epochs=model.epochs)
    #get the move that maxes the similarity
    max_similarity = 0
    move = ''
    for i, fen in enumerate(all_fen):
        similarity = abs(np.dot(fighter,unitvec(model.wv[fen])))
        if similarity > max_similarity:
            max_similarity = similarity
            move = avail_moves[i]
    if verbose:
        print('Function find optimal move given array\'s output: ')
        print('move: ', move,'\nmax_similarity: ', max_similarity)
    return move

def plot_advantage_and_mating_of_game(advantage_over_time:list,mating_chances:list):
    plt.plot([i for i in range(len(advantage_over_time))],advantage_over_time,[i for i in range(len(mating_chances))],mating_chances)
    plt.ylabel('Advantage (centipawns)/Number of Moves Before Mate')
    plt.xlabel('Turn #')
    plt.legend(['Advantage','Mating Chances'])
    plt.show()

def writeback_pgn(pgn_game:chess.pgn.Game,file_path:str,white:str,black:str,date:datetime=datetime.now()):
    pgn_game.headers['White'] = white
    pgn_game.headers['Black'] = black
    pgn_game.headers['Event'] = '%s vs %s' % (white, black)
    pgn_game.headers['Date'] = date.strftime("%m/%d/%Y")
    with open(file_path, "w") as pgn_file:
        pgn_file.write(str(pgn_game))