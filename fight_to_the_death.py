import chess
import chess.pgn
from cnn import ImageCompressor
from PIL import Image
from torchvision import transforms
import numpy as np
import random
from tqdm import tqdm
from stockfish import Stockfish
from matplotlib import pyplot as plt

########################################
import gensim
from gensim.matutils import unitvec
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
model = Word2Vec.load('./gensim_models/chess_model_2.bin')
########################################

########################################
stockfish = Stockfish("C:\\Users\\sebas\\Documents\\gojo_satoru\\chess-engines\\stockfish\\stockfish-windows-x86-64-avx2.exe")
stockfish.set_elo_rating(3100)
stockfish.get_fen_position()
########################################

imgToTensor = transforms.ToTensor()
tensorToimg = transforms.ToPILImage()

device ='cpu'
tp_ff = ImageCompressor().to(device)

fighter_1 = Image.open("C:\\Users\\sebas\\Documents\\gojo_satoru\\jjk_images\\S1_(2)\\frame1248.png")
imageData = imgToTensor(fighter_1)
fighter_1_vec = unitvec(np.array(tp_ff(imageData)))

fighter_2 = Image.open("C:\\Users\\sebas\\Documents\\gojo_satoru\\jjk_images\\S1_(5)\\frame11962.png")
imageData = imgToTensor(fighter_2)
fighter_2_vec = unitvec(np.array(tp_ff(imageData)))
print('matchup: fighter1\n',fighter_1_vec,'\nfighter2\n',fighter_2_vec)


def simulate_game(iters:int):
    outcomes = {'W':0,'B':0,'D':0}
    moves= ''
    for i in tqdm(range(iters)):
        board = init_game()
        stockfish.set_fen_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        pgn_game = chess.pgn.Game()
        first_move = True
        advantage_over_time = []
        # print('board fen: ', board.fen())
        while not board.is_game_over():
            #determine move
            if board.turn:
                move = find_optimal_move_given_fighter(board,fighter_1_vec)
            else:
                move = find_optimal_move_given_fighter(board,fighter_2_vec)
            board.push(move)
            ################
            #stockfish
            stockfish.make_moves_from_current_position([move.uci()])
            eval = stockfish.get_evaluation()
            advantage_over_time.append(eval['value'] if eval['type'] == 'cp' else 0)
            ###############

            #make pgn
            if first_move:
                # print('move: ', move)
                node = pgn_game.add_variation(move)
                first_move = False
            else:
                node = node.add_variation(move)
            print('board state: ', board.fen())
            moves += board.fen() +'\n'
        result = board.result()
        print(pgn_game)
        plt.plot([i for i in range(len(advantage_over_time))],advantage_over_time)
        plt.ylabel('Advantage (centipawns)')
        plt.xlabel('Turn #')
        plt.show()
        with open("game.pgn", "w") as pgn_file:
            pgn_file.write(str(pgn_game))
        outcomes['W' if result=='1-0' else 'B' if result =='0-1' else 'D'] += 1
    return (moves,outcomes)

def init_game():
    return chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

def chose_random_move(board:chess.Board) -> chess.Move:
    return random.choice(list(board.legal_moves))

def get_all_fen(board:chess.Board) -> list:
    """
    Get all of the available positions that the chess board could be in next turn
    """
    all_fen = []
    avail_moves = list(board.legal_moves)
    for cur_move in avail_moves:
        # print(cur_move)
        board.push(cur_move)
        # print(board.turn)
        cur_fen = board.fen()
        board.pop()
        all_fen.append(cur_fen)
    # print(board.turn)
    return (avail_moves,all_fen)

def find_optimal_move_given_fighter(board:chess.Board,fighter:np.array):
    avail_moves, all_fen = get_all_fen(board)
    model.build_vocab([all_fen], update=True)
    model.train([all_fen], total_examples=model.corpus_count, epochs=model.epochs)
    max_similarity = 0
    move = ''
    for i, fen in enumerate(all_fen):
        similarity = abs(np.dot(fighter,unitvec(model.wv[fen])))
        # print('similarity: ', similarity,'\nmax_similarity: ', max_similarity)
        if similarity > max_similarity:
            max_similarity = similarity
            move = avail_moves[i]
    return move


def test_getting_fen():
    board = init_game()
    print(get_all_fen(board))

def test_optimal_move():
    board = init_game()
    # print(get_all_fen(board))
    board.push(find_optimal_move_given_fighter(board,fighter_1_vec))
    print(board.fen())


if __name__ == '__main__':
    simulate_game(1)
    # test_optimal_move()
    # pass