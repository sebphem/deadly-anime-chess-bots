import gensim
from gensim.matutils import unitvec
# model = api.load('word2vec-google-news-300')
# print(model.wv['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'])

from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')



model = Word2Vec(sentences, vector_size=300, window=5, min_count=1, workers=4)
word_vector = model.wv['rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR']
print("Vector representation:", word_vector)
# Update the vocabulary with new tokenized data
model.build_vocab([tokenized_fen], update=True)

# Continue training the model with the new data
model.train([tokenized_fen], total_examples=model.corpus_count, epochs=model.epochs)



import chess
board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
print(board.is_checkmate())


from stockfish import Stockfish
stockfish = Stockfish("C:\\Users\\sebas\\Documents\\gojo_satoru\\chess-engine-tests\\stockfish\\stockfish-windows-x86-64-avx2.exe")
stockfish.set_elo_rating(3600)
stockfish.set_fen_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
legal_moves = stockfish.get_top_moves(255)
for move in legal_moves:
    stockfish.set_fen_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    stockfish.make_moves_from_current_position([move['Move']])
    fen_pos = stockfish.get_fen_position()
    print('fen position for move %s : %s'%(move['Move'],fen_pos))
print(stockfish.get_wdl_stats())