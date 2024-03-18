import cv2
from PIL import Image
import os
import multiprocessing


def worker_function(episode_num):
    print(f"Process for episode {episode_num} is working.")
    try:
        os.mkdir('./jjk_images/S1_(%s)' % episode_num)
    except:
        pass
    jjk = cv2.VideoCapture('./jjk/Jujutsu Kaisen S1 (%s).mkv' % episode_num)
    frame_number_to_start = 13326 if episode_num == 1 else 0  # Change this to the desired frame number
    # Set the frame position
    jjk.set(cv2.CAP_PROP_POS_FRAMES, frame_number_to_start)
    success, frame = jjk.read()
    count = 0
    while success:
        cv2.imwrite("./jjk_images/S1_(%s)/frame%d.png"% (episode_num,count), frame)
        success , frame =jjk.read()
        count+= 1
    print('finished, wrote %d frames' % count)


if __name__ == '__main__':
    episodes = [1, 2, 3, 4, 5, 6]
    
    processes = []
    for episode in episodes:
        p = multiprocessing.Process(target=worker_function, args=(episode,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
