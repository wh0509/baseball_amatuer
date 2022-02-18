import sys
import os
import re

import pandas as pd
from bs4 import BeautifulSoup as bs

from baseball_library import crawling, path

def main():

    team_path = path(workDir="data")
    team_path.setWorkDir(path_list=["team"])
    team_data_path = team_path.getWorkDir()

    team_df = pd.read_csv(os.path.join(team_data_path, "team_info.csv"), encoding="euc-kr")
    team_index_list = list(team_df["팀ID"].dropna().unique())

    try:

        for year in [2020]:

            for index in team_index_list:
                
                team_name = team_df.loc[(team_df['팀ID']==index), '팀명'].values[0]
                team_folder = "{}_{}".format(team_name, index)
                
                url = "http://www.korea-baseball.com/info/team/team_player?club_idx={}&season={}".format(index, year)
                crawler = crawling(url, 0)
                crawler.set_driver()



    except:


if __name__=="__main__":

    main()