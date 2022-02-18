import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import requests
import library.variable as V

def set_url_path(category='team', sub_category='team_list'):

    '''
    설명 : url을 설정하는 함수

    인자
    - category : 팀/선수
    - sub_category : team_list, team_player, team_schedule
    
    '''

    ## 팀
    if category == 'team':

        team_url = os.path.join(V.base_url, 'team')

        if sub_category != None:

            if sub_category == 'team_list':

                team_url = "{}/{}".format(team_url, 'team_list')
            
            elif sub_category == 'team_player':

                team_url = "{}/{}".format(team_url, 'team_player')
            
            elif sub_category == 'team_schedule':

                team_url = "{}/{}".format(team_url, 'team_schedule')
            
        return team_url

    ## 선수
    # elif category == 'player':

def requests_url(url, parameter, format='html'):

    """
    설명 : url을 요청하여 데이터를 가져오는 함수
    
    
    """

    relay_response = requests.get(url,params=parameter)

    if relay_response.status_code == 200:

        if format == "json":

            result_format = relay_response.json()
        
        elif format == "html":

            result_format = relay_response.content

    else:
        
        result_format = None
    
    return result_format

def set_path(root, workDir=None, path_list=None):

    if workDir==None:

        pass
    
    else:

        root = os.path.join(root, workDir)

    if path_list!=None:

        for path in path_list:

            root = os.path.join(root, path)

    if os.path.isdir(root):

        pass

    else:

        os.makedirs(root)
    
    return root