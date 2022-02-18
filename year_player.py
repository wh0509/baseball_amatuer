import sys
import os
import re

import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from baseball_library import crawling, path
from exception import selfException

def year_player(input_year):

    # team_df = pd.read_csv(os.path.join(os.getcwd(), "team_info.csv"), encoding="euc-kr")
    # team_index_list = list(team_df["팀ID"].dropna().unique())
        
    year = input_year
    try:

        for kind_cd in ["31", "41"]:
        
            if kind_cd == "31":

                kind = "19세_이하부"
                
            elif kind_cd == "41":

                kind = "대학부"

            year_team_path = path(workDir="data")
            year_team_path.setWorkDir(path_list=[year, kind])
            year_team_csv_path = year_team_path.getWorkDir()

            year_team_df = pd.read_csv(os.path.join(year_team_csv_path, "{}_info_list.csv".format(kind)), encoding='euc-kr')

            year_team_index_list = list(year_team_df["팀ID"].dropna().unique())

            year_player_df =  pd.DataFrame(columns=["팀명", "구분", "선수명", "등번호", "포지션", "학년", "신장", "체중", "투", "타", "선수ID"])

            for index in year_team_index_list:

                # http://www.korea-baseball.com/info/team/team_player?club_idx=166&season=2020&kind_cd=41&sports_club=F
                url = "http://www.korea-baseball.com/info/team/team_player?club_idx={}&kind_cd={}&season={}".format(index, kind_cd, year)
                team = year_team_df.loc[(year_team_df['팀ID']==index), '팀명'].values[0]
                distribution = year_team_df.loc[(year_team_df['팀ID']==index), '팀구분'].values[0]

                crawler = crawling(url, 0)
                driver = crawler.set_driver()

                source_soup = bs(driver.page_source, "html.parser")
                driver.close()
                
                player_list_soup = source_soup.find("ul", class_="team_list").find_all("li")
                
                if player_list_soup == None:
                
                    continue
                
                else:

                    for player in player_list_soup:
                        
                        player_url = player.find("a")['href']
                        parts = urlparse(player_url)
                        parts_dict = parse_qs(parts.query)

                        player_info_list = []

                        dd_list = player.findAll("dd")
                        dt_list = player.findAll("dt")

                        player_distribution = parts_dict['gubun'][0]
                        
                        if player_distribution != "P":

                            continue
                        
                        for dt, dd in zip(dt_list, dd_list):

                            if dt.text == "백넘버 / 성명":

                                if dd.text == "":

                                    player_number = ""
                                    player_name = ""
                                
                                else:

                                    player_number = dd_list[0].find("span", class_="number").text
                                    player_name = dd_list[0].find("span", class_="name").text

                            elif dt.text == "선수구분":

                                if dd.text =="":

                                    player_position = ""
                                
                                else:

                                    player_position = dd.text
                            
                            elif dt.text == "학년":

                                if dd.text == "":

                                    player_grade = ""
                                
                                else:

                                    player_grade = re.findall(r'\d+', dd.text)[0]
                            
                            elif dt.text == "신장 / 체중":

                                if dd.text == "":

                                    player_height = ""
                                    player_weight = ""
                                
                                else:

                                    player_body = re.findall(r'\d+', dd.text)
                                    
                                    if len(player_body) == 0:
                                        player_height = ""
                                        player_weight = ""
                                    
                                    else:
                                        try:
                                            player_height = player_body[0]
                                        except IndexError:
                                            player_height = ""

                                        try:
                                            player_weight = player_body[1]
                                        except IndexError:
                                            player_weight = ""

                            elif dt.text == "투타":

                                if dd.text == "":

                                    player_throw = ""
                                    player_stand = ""
                                
                                else:

                                    player_throw = dd.text[0]
                                    player_stand = dd.text[2]
                        
                        player_id = parts_dict['person_no'][0]
                        
                        year_player_df.loc[len(year_player_df)] = [team, distribution, player_name, player_number, player_position, player_grade, player_height, player_weight, player_throw, player_stand, player_id]
            
            year_player_df = year_player_df.drop_duplicates("선수ID")
            year_player_df.to_csv(os.path.join(year_team_csv_path, "{}_player_info_list.csv".format(kind)), index=False, encoding='euc-kr')
    
    except (Exception, KeyboardInterrupt, selfException) as E:

        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno

        print("Process Exception in line {}".format(line), E)

        year_player_df = year_player_df.drop_duplicates("선수ID")
        year_player_df.to_csv(os.path.join(year_team_csv_path, "{}_player_info_list.csv".format(kind)), index=False, encoding='euc-kr')


if __name__ == "__main__":
    
    year_player("2020")