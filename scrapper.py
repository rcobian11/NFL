from bs4 import BeautifulSoup
import requests

def get_team(pos):
    ctr = 0
    for num, elem in enumerate(pos):
        if elem == ':':
            ctr += 1
        if ctr == 2:
            team = pos[num + 1:-1].strip('"')
            break
    return(team)

def get_points(pos):
    ctr = 0
    for num, elem in enumerate(pos):
        if elem == '"':
            ctr += 1
        if ctr == 3:
            num2 = num+1
            while(pos[num2] != '"'):
                num2 += 1
            points = pos[num + 1: num2]
            break
    if points[0] == '+':
        return(float(points[1:]))
    else:
        return(float(points[1:]) * -1)

def build_config(url,num_games):
    teams = []
    spreads = []
    target_html = requests.get(url)
    soup = BeautifulSoup(target_html.text, "html.parser")
    soup = soup.find(id="op-content-wrapper")
    for team in soup.find_all('div', "op-matchup-wrapper football"):
        top = team.find("div","op-matchup-team-wrapper").div['data-op-name']
        bot = team.find("div","op-matchup-team-wrapper").div.next_sibling['data-op-name']
        top_team = get_team(top)
        bot_team = get_team(bot)
        teams.append((top_team,bot_team))
        #print("{} vs {}".format(top_team, bot_team))
    for junk in soup.find_all('div', 'op-item-row-wrapper not-futures'):
        points = junk.find('div', 'op-first-row').div['data-op-info']
        spreads.append(get_points(points))
    config = open("config.csv", "w")
    num = 0
    for team,point in zip(teams,spreads):
        num += 1
        if num > num_games:
            break
        if point < 0:
            if point.is_integer():
                point -= 0.5
            config.write("{},{},{}\n".format(team[0].upper(),str(point),team[1].upper()))
        else:
            if point.is_integer():
                point += 0.5
            config.write("{},-{},{}\n".format(team[1].upper(),str(point),team[0].upper()))
