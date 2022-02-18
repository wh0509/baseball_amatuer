import os
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from library.function import set_path, set_url_path, requests_url
from library.variable import class_dict

current_path = os.path.dirname(__file__)

def year_team(input_year):
       
    year = input_year

    for class_ in class_dict:

        kind_cd = class_dict[class_]

        year_team_df = pd.DataFrame(columns=["team_id", "year", "team_class"])
        year_work_path = set_path(current_path, workDir='data')
        year_class_path = set_path(year_work_path, path_list=[year, class_])
        url = set_url_path(category='team', sub_category='team_list')
        params_dict = {

            'season' : year,
            'sido_cd' : '00',
            'kind_cd' : kind_cd

        }

        for page in range(1,100,1):

            params_dict['page']=page

            contents = requests_url(url=url, parameter=params_dict)

            source_soup = bs(contents, "html.parser")
            team_info_list = source_soup.find("ul", class_="info_list").find_all("li")
            
            if len(team_info_list)==0:

                break

            else:

                for team in team_info_list:

                    team_url = team.find("a")['href']

                    parts = urlparse(team_url)
                    parts_dict = parse_qs(parts.query)

                    club_index = int(parts_dict['club_idx'][0])
                    
                    year_team_info = [club_index, year, kind_cd]

                    # "번호", "년도", "팀명", "팀구분", "지역", "선수수", "감독", "팀ID", "구분ID"
                    year_team_df.loc[len(year_team_df)] = year_team_info
                
        year_team_df.to_csv(os.path.join(year_class_path, "{}_info_list.csv".format(class_)), index=False, encoding='euc-kr')

if __name__ == "__main__":
    
    year_team("2020")