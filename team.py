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

    player_total_path = path(workDir="data")
    # player_total_path.setWorkDir(path_list=["player"])
    player_total_csv_path = player_total_path.getWorkDir()

    try:

        team_df = pd.read_csv(os.path.join(info_data_path, "team_info.csv"), encoding="euc-kr")
        team_index_list = list(team_df["팀ID"].dropna().unique())
        last_index = max(team_index_list)
        
    except:

        team_df = pd.DataFrame(columns=["팀명", "년도", "구분", "지역", "창단년도", "감독", "주소", "팀ID"])
        team_index_list = []
        last_index = 1

    try:

        player_df = pd.read_csv(os.path.join(player_total_csv_path, "player_total_info.csv"), encoding='euc-kr')
    
    except:

        player_df = pd.DataFrame(columns=["선수명", "등번호", "년도", "팀", "구분", "선수ID"])

    try:

        for year in [2020]:

            for index in range(last_index,1500,1):

                # if index == 61:

                if index in team_index_list:

                    continue

                team_summary_list = []

                url = "http://www.korea-baseball.com/info/team/team_player?club_idx={}&season={}".format(index, year)
                crawler = crawling(url, 0)
                driver = crawler.set_driver()

                source_soup = bs(driver.page_source, "html.parser")
                driver.close()

                team_summary_soup = source_soup.find("div", class_="team_summary bg_gray6")
                
                team_name = team_summary_soup.find("h3")
                summary_list = team_summary_soup.find_all("td")

                if team_name == None or team_name.text == "":
                
                    continue
                
                else:
                
                    team_summary_list.append(team_name.text)
                
                team_summary_list.append(year)

                for summary in summary_list:

                    team_summary_list.append(summary.text)

                team_summary_list.append(index)

                team_df.loc[len(team_df)] = team_summary_list
                team_distribution = team_df.loc[(team_df['팀ID']==index), '구분'].values[0]

                if team_distribution == "대학부" or team_distribution == "19세 이하부":

                    # team_folder = "{}_{}".format(team_name.text, index)

                    # team_path = path(workDir="data")
                    # team_path.setWorkDir(path_list=["team", team_folder])
                    # team_path = team_path.getWorkDir()

                    team_list_soup = source_soup.find("ul", class_="team_list").find_all("li")
                    
                    if team_list_soup == None:
                    
                        continue
                    
                    else:

                        for team in team_list_soup:

                            player_url = team.find("a")['href']
                            parts = urlparse(player_url)
                            parts_dict = parse_qs(parts.query)

                            if parts_dict['gubun'][0] == 'P':

                                player_info_list = []

                                dd_list = team.findAll("dd")

                                player_number = dd_list[0].find("span", class_="number")
                                player_name = dd_list[0].find("span", class_="name")

                                player_info_list += [player_number.text.strip().replace(".",""), player_name.text, year, team_name.text, team_distribution]
                                player_info_list.append(parts_dict['person_no'][0])

                                player_df.loc[len(player_df)] = player_info_list
                
                else:
                    
                    continue
        
        # team_specific_df = team_df[(team_df["구분"]=="대학부") & (team_df["구분"]=="19세 이하부")]
        team_df = team_df.drop_duplicates('팀명')
        team_df.to_csv(os.path.join(info_data_path,"team_info.csv"), index=False, encoding='euc-kr')

        # player_specific_df = player_df[(player_df["구분"]=="대학부") & (player_df["구분"]=="19세 이하부")]
        player_df.to_csv(os.path.join(player_total_csv_path,"player_total_info.csv"), index=False, encoding='euc-kr')

    except (Exception, KeyboardInterrupt, selfException) as E:

        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno

        print("Process Exception in line {}".format(line), E)
        
        if len(team_df) > 0:

            team_df = team_df.drop(team_df.index[-1])
        
        # team_specific_df = team_df[(team_df["구분"]=="대학부") & (team_df["구분"]=="19세 이하부")]
        team_df = team_df.drop_duplicates('팀명')
        team_df.to_csv(os.path.join(info_data_path,"team_info.csv"), index=False, encoding='euc-kr')

        # player_specific_df = player_df[(player_df["구분"]=="대학부") & (player_df["구분"]=="19세 이하부")]
        player_df.to_csv(os.path.join(player_total_csv_path,"player_total_info.csv"), index=False, encoding='euc-kr')

if __name__ == "__main__":
    
    team()