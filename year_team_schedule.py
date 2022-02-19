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
        url = set_url_path(category='team', sub_category='team_schedule')
        params_dict = {

            'kind_cd' : kind_cd,
            'season' : year

        }

        year_team_df = pd.read_csv(os.path.join(year_class_path, "{}_info_list.csv".format(class_)))
        year_player_df =  pd.DataFrame(columns=["team_class", "game_pk", "game_date", "time", "place", "team_1_name", "team_1_score", "team_2_name", "team_2_score"])
        year_team_id_list = list(year_team_df["team_id"].dropna().unique())

        for team_id in year_team_id_list:

            params_dict["club_idx"] = team_id
            contents = requests_url(url=url, parameter=params_dict)

            source_soup = bs(contents, "html.parser")
            
            game_soup = source_soup.find("ul", class_="date")
            game_list = game_soup.findAll('li', class_="past")
            
            if game_list == None:
            
                continue
            
            else:

                for game_soup in game_list:

                    game_date = game_soup.find('h4').text.split("(")[0].replace(".",'-')
                    game_list = game_soup.find('ul', class_="game_list").find_all('li')

                    for game in game_list:



                        game_info = game.find("dd", class_="btn")

                        try:
                            game_url = game_info.find("a")['href']
                        
                        except:
                            game_url = None
                        
                        if game_url!=None:

                            parts = urlparse(game_url)
                            parts_dict = parse_qs(parts.query)

                            game_pk = parts_dict['game_idx'][0]

                            game_info = game.find("dd", class_="inform")
                            time = game_info.find("span", class_="time").text
                            place = game_info.find("span", class_="place").text
                            
                            ## 
                            team_1_info = game.find("p", class_="team1")
                            team_1_name = team_1_info.find("span", class_="team").text 
                            team_1_score = team_1_info.find("span", class_="score").text if team_1_info.find("span", class_="score")!=None else None
                            
                            team_2_info = game.find("p", class_="team2")
                            team_2_name = team_2_info.find("span", class_="team").text
                            team_2_score = team_2_info.find("span", class_="score").text if team_2_info.find("span", class_="score")!=None else None
                            
                            year_player_df.loc[len(year_player_df)] = [kind_cd, game_pk, game_date, time, place, team_1_name, team_1_score, team_2_name, team_2_score]

                        else:

                            continue

        year_player_df = year_player_df.drop_duplicates("game_pk")
        year_player_df.to_csv(os.path.join(year_class_path, "{}_game_list.csv".format(class_)), index=False, encoding='euc-kr')

if __name__ == "__main__":
    
    year_player("2020")