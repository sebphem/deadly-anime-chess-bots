import random
from tqdm import tqdm
import chess
import multiprocessing


def simulate_game():
    outcomes = {'W':0,'B':0,'D':0}
    moves= ''
    for i in tqdm(range(1000)):
        board = init_game()
        # print('board fen: ', board.fen())
        while not board.is_game_over():
            move = chose_random_move(board)
            make_move(board,move)
            # print('board state: ', board.fen())
            moves += board.fen() +'\n'
        result = board.result()
        outcomes['W' if result=='1-0' else 'B' if result =='0-1' else 'D'] += 1
    return (moves,outcomes)

def init_game():
    return chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

def chose_random_move(board:chess.Board):
    return random.choice(list(board.legal_moves))

def make_move(board:chess.Board,move_str:chess.Move):
    return board.push(move_str)

def writeback_stage(moves_array:list):
    for move_sets in moves_array:
        with open('./seb_positions.txt','a') as f:
            f.write(move_sets)


if __name__ == '__main__':
    # simulate_game()
    processes = multiprocessing.cpu_count()  # Number of CPU cores

    with multiprocessing.Pool(processes=processes) as pool:
        results = [pool.apply_async(simulate_game, ()) for i in range(processes)]
        writeback_stage([result.get()[0] for result in results])
        winners_dict = [result.get()[1] for result in results]

        main_winners_dict = {'W':0,'B':0,'D':0}
        for thread in winners_dict:
            for key,val in thread.items():
                main_winners_dict[key] += val
        print('The outcome of all the simulated games: ', main_winners_dict)
