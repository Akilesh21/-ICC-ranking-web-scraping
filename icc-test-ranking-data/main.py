import requests
from bs4 import BeautifulSoup
import pandas

URL = "https://www.icc-cricket.com/rankings/mens/team-rankings/test"
response =requests.get(url=URL)
forbes_html = response.text
soup = BeautifulSoup(forbes_html,"html.parser")
#--------------------------rank data-------------------#
Ranking = []
aus_rank = soup.find(name="td",class_="rankings-block__banner--pos")
Ranking.append(aus_rank.text)
others_rank = soup.find_all(name="td",class_="table-body__cell table-body__cell--position u-text-right")
for Rank in others_rank:
    Ranking.append(Rank.text)
print(Ranking)
Teams_ranking = [int(n) for n in Ranking]
#----------------------------teams data------------------------#
teams = soup.find_all(name="span",class_="u-hide-phablet")
Test_teams = []
for team in teams:
    Test_teams.append(team.text)
#---------------------------Matches & points data--------------#    
matches = []    
aus_match= soup.find(name="td",class_="rankings-block__banner--matches")
aus_points = soup.find(name="td",class_ = "rankings-block__banner--points")
matches.append(aus_match.text)
matches.append(aus_points.text)
team_matches = soup.find_all(name="td",class_="table-body__cell u-center-text")
for match in team_matches :
    matches.append(match.text) 

matches_per_team = []
points = []
for i in range(len(matches)):
    if i%2 :
        points.append((matches[i]))
    else:
        matches_per_team.append((matches[i])) 

Matches_per_team = [int(n) for n in matches_per_team]
#---------------------------------Teams rating data-------------------------#
aus_rating = soup.find(name="td",class_="rankings-block__banner--rating u-text-right")
rating = (aus_rating.text.split())
others_rating = soup.find_all(name="td",class_ = "table-body__cell u-text-right rating")
for _rating in others_rating:
    rating.append(_rating.text)
Teams_rating = [int(n) for n in rating]
#--------------------------------Test team changing data in dictionary------------#
Test_ranking = {}
for rank in range(len(Test_teams)):
    Test_ranking[rank] = {
        "Position":Teams_ranking[rank],
        "Team":Test_teams[rank],
        "Matches":Matches_per_team[rank],
        "Points":points[rank],
        "Rating":Teams_rating[rank]

    }
Test_ranking_dict = pandas.DataFrame(Test_ranking)
Test_ranking_csv  = Test_ranking_dict.to_csv("web-scraping-project/icc-test-ranking-data/Test_ranking_data.csv")
print(Test_ranking_dict)