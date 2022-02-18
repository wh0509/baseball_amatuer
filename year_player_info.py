import sys
import os
import re

import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from urllib.request import urlretrieve

from baseball_library import crawling, path
from exception import selfException

def year_player(input_year):

    # team_df = pd.read_csv(os.path.join(os.getcwd(), "team_info.csv"), encoding="euc-kr")
    # team_index_list = list(team_df["팀ID"].dropna().unique())
    try:

        exist_player_df = pd.read_csv("exist_player.csv",encoding='euc-kr')
        exist_player_id_list = list(exist_player_df["선수ID"].dropna().unique())

    except:

        exist_player_df = pd.DataFrame(columns=["선수명", "선수ID"])
        exist_player_id_list = []

    year = input_year
    try:

        for kind_cd in ["31", "41"]:
        
            if kind_cd == "31":

                kind = "19세_이하부"
                
            elif kind_cd == "41":

                kind = "대학부"

            year_path = path(workDir="data")
            year_path.setWorkDir(path_list=[year, kind])
            year_csv_path = year_path.getWorkDir()

            year_player_df = pd.read_csv(os.path.join(year_csv_path, "{}_player_info_list.csv".format(kind)), encoding='euc-kr')

            year_team_list = list(year_player_df["팀명"].dropna().unique())

            for team in year_team_list:

                year_team_player_df = year_player_df[(year_player_df["팀명"]==team)]
                player_id_list = list(year_team_player_df["선수ID"].dropna().unique())

                for player in player_id_list:

                    if player in exist_player_id_list:

                        continue
                    
                    player_name = year_team_player_df.loc[(year_team_player_df["선수ID"]==player), "선수명"].values[0]
                    
                    exist_player_df.loc[len(exist_player_df)] = [player_name, player]

                    player_path = path(workDir="data")
                    player_path.setWorkDir(path_list=[year, kind, team, player_name])
                    player_csv_path = player_path.getWorkDir()

                    url = "http://www.korea-baseball.com/info/player/player_view?person_no={}&gubun=P".format(player)

                    crawler = crawling(url, 0)
                    driver = crawler.set_driver()

                    source_soup = bs(driver.page_source, "html.parser")
                    driver.quit()

                    img_source = source_soup.find("div", class_="img player").find("img")['src']
                    urlretrieve("http:{}".format(img_source), os.path.join(player_csv_path, "{}.jpg".format(player_name)))

                    for category in ["hitter", "pitcher"]:

                        if category == "hitter":

                            category_hangeul = "타자"

                        elif category == "pitcher":

                            category_hangeul = "투수"

                        section_list = source_soup.find("div", id=category).findAll("div", class_="section_info")

                        for section in section_list:
                            
                            section_name = section.find("h4").text.replace(" ","")
                            section_name = section_name.strip()

                            if "타구방향" in section_name or "5경기" in section_name or "(-)" in section_name:

                                continue
                            
                            else:

                                section_df = None                                
                                data_list = section.find("ul").findAll("li")

                                if len(data_list)==0:

                                    continue

                                for data in data_list:
                                    
                                    if data == data_list[0]:

                                        columns = data.text.split("\n")
                                        columns = [elem for elem in columns if elem != ""]
                                        columns.append("년도")

                                        section_df = pd.DataFrame(columns = columns)
                                    
                                    else:

                                        row = data.text.split("\n")
                                        row = [elem for elem in row if elem != ""]
                                        row.append(year)
                                        section_df.loc[len(section_df)] = row
                        
                                section_df.to_csv(os.path.join(player_csv_path, "{}_{}.csv".format(category_hangeul, section_name)), index=False, encoding='euc_kr')
                    
                    info_list = source_soup.findAll("div", class_="info_list")
                    info = info_list[-1]

                    info_section_list = info.findAll("div", class_="section_info")
                    for info in info_section_list:

                        info_name = info.find("h4").text.replace(" ","")
                        info_name = info_name.strip()

                        info_df = None
                        data_list = info.find("ul").findAll("li")

                        if len(data_list)==0:

                            continue

                        for data in data_list:
                            
                            if data == data_list[0]:
                                
                                columns = []
                                span_list = data.findAll("span")

                                for span in span_list:

                                    columns.append(span.text.strip())

                                info_df = pd.DataFrame(columns = columns)
                            
                            else:

                                row = []
                                span_list = data.findAll("span")

                                for span in span_list:

                                    row.append(span.text.strip())

                                info_df.loc[len(info_df)] = row
                    
                            info_df.to_csv(os.path.join(player_csv_path, "{}.csv".format(info_name)), index=False, encoding='euc_kr')

                    del player_path

        exist_player_df.to_csv("exist_player.csv",encoding='euc-kr', index=False)

    except (Exception, KeyboardInterrupt, selfException) as E:

        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno

        print("Process Exception in line {}".format(line), E)

        exist_player_df.to_csv("exist_player.csv",encoding='euc-kr', index=False)
        # year_player_df = year_player_df.drop_duplicates("선수ID")
        # year_player_df.to_csv(os.path.join(year_team_csv_path, "{}_player_info_list.csv".format(kind)), index=False, encoding='euc-kr')


if __name__ == "__main__":
    
    year_player("2020")