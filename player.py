import sys
import os
import re

import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from baseball_library import crawling, path
from exception import selfException

def team():

    info_path = path(workDir="data")
    # info_path.setWorkDir(path_list=["team"])
    info_data_path = info_path.getWorkDir()
    
    team_df = pd.read_csv(os.path.join(info_data_path, "team_info.csv"), encoding="euc-kr")
    team_index_list = list(team_df["팀ID"].dropna().unique())


    player_total_path = path(workDir="data")
    player_total_path.setWorkDir(path_list=["player"])
    player_total_csv_path = player_total_path.getWorkDir()

    try:

        team_df = pd.read_csv(os.path.join(info_data_path, "team_info.csv"), encoding="euc-kr")
        team_index_list = list(team_df["팀ID"].dropna().unique())
        last_index = max(team_index_list)
        