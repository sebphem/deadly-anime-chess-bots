import random
from stockfish import Stockfish
from tqdm import tqdm
stockfish = Stockfish("C:\\Users\\sebas\\Documents\\gojo_satoru\\chess-engine-tests\\stockfish\\stockfish-windows-x86-64-avx2.exe")
stockfish.set_elo_rating(3600)
stockfish.get_fen_position()


def make_move(game_num: int = 0,fen: str = ''):
    if fen != '':
        if stockfish.is_fen_valid(fen):
            stockfish.set_fen_position(fen)
        else:
            raise "fen is not valid"
    else:
        stockfish.set_fen_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    legal_moves = stockfish.get_top_moves(15)
    if legal_moves == None:
        print('game ended')
        return
    move_index = random.randint(0, len(legal_moves)-1)
    move_string = legal_moves[move_index]['Move']
    # print('move: ', move_index,' ', [move_string])
    stockfish.make_moves_from_current_position([move_string])
    fen_pos = stockfish.get_fen_position()
    with open('./seb_positions.txt','a') as f:
        f.write(fen_pos+'\n')
    make_move(game_num,fen_pos)

for i in tqdm(range(1000)):
    make_move(i)