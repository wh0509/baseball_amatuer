import sys
import os
import re

import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from library.function import set_path, set_url_path, requests_url
from library.variable import class_dict

current_path = os.path.dirname(__file__)

def year_player(input_year):

    year = input_year

    for class_ in class_dict:

        kind_cd = class_dict[class_]

        year_team_df = pd.DataFrame(columns=["team_id", "year", "team_class"])
        year_work_path = set_path(current_path, workDir='data')
        year_class_path = set_path(year_work_path, path_list=[year, class_])
        url = set_url_path(category='team', sub_category='team_player')
        params_dict = {

            'kind_cd' : kind_cd,
            'season' : year

        }

        year_team_df = pd.read_csv(os.path.join(year_class_path, "{}_info_list.csv".format(class_)))
        year_player_df =  pd.DataFrame(columns=["team_class", "player_id", "player_name", "back", "position", "grade", "height", "weight", "throws", "stand"])
        year_team_id_list = list(year_team_df["team_id"].dropna().unique())

        for team_id in year_team_id_list:

            params_dict["club_idx"] = team_id
            contents = requests_url(url=url, parameter=params_dict)

            source_soup = bs(contents, "html.parser")
            
            player_list_soup = source_soup.find("ul", class_="team_list").find_all("li")
            
            if player_list_soup == None:
            
                continue
            
            else:

                for player in player_list_soup:

                    player_url = player.find("a")['href']
                    parts = urlparse(player_url)
                    parts_dict = parse_qs(parts.query)

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

                                player_number = re.findall('\d+',dd_list[0].find("span", class_="number").text)[0] if dd_list[0].find("span", class_="number") else None
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
                    
                    year_player_df.loc[len(year_player_df)] = [kind_cd, player_id, player_name, player_number, player_position, player_grade, player_height, player_weight, player_throw, player_stand]
            
        year_player_df = year_player_df.drop_duplicates("player_id")
        year_player_df.to_csv(os.path.join(year_class_path, "{}_player_info_list.csv".format(class_)), index=False, encoding='euc-kr')

if __name__ == "__main__":
    
    year_player("2020")