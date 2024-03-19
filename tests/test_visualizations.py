import os
import os.path
dir_name = os.path.dirname(__file__)
os.environ["PATH"] += os.pathsep + '%s/../Graphviz-10.0.1-win64/bin/' % os.path.dirname(__file__)

from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.custom import Custom

graph_attr = {
    "fontsize": "45",
}



with Diagram("episode 1 graph",graph_attr=graph_attr):
    
    fighter_1 = Custom('1','%s/../video_processing/jjk_images/S1_(1)/frame9.png' % dir_name)
    fighter_2 = Custom('2','%s/../video_processing/jjk_images/S1_(1)/frame342.png' % dir_name)
    final_contestor_1 = Custom('2','%s/../video_processing/jjk_images/S1_(1)/frame342.png' % dir_name)
    fighter_3 = Custom('3','%s/../video_processing/jjk_images/S1_(1)/frame5670.png' % dir_name)
    fighter_4 = Custom('4','%s/../video_processing/jjk_images/S1_(1)/frame1234.png' % dir_name)
    final_contestor_2 = Custom('4','%s/../video_processing/jjk_images/S1_(1)/frame1234.png' % dir_name)
    eval('[fighter_1,fighter_2] >> final_contestor_1')
    eval('[fighter_3,fighter_4] >> final_contestor_2')