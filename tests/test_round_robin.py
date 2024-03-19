import sys
sys.path.append('..\\')
import tournament

def test_make_round_robin():
    game_queue,round_robin = tournament.make_round_robin('/video_processing/jjk_images/S1_(1)',num_rounds=7,debug=True)
    print('num of fighters: ', len(round_robin))
    for name,competitor in round_robin.items():
        print(competitor)
    print(game_queue)