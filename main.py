import telegram.ext
from bs4 import BeautifulSoup
import requests
import pytz
import prettytable as pt
import urllib.request
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from monotable import mono
import re
import prettytable as pt
from telegram import ParseMode
from prettytable import PLAIN_COLUMNS
from prettytable import MSWORD_FRIENDLY
from prettytable import MARKDOWN
from prettytable import ORGMODE



# / replace PL Teams name to Short formdef replacer(msg):
def replacer(msg):
    msg = re.sub("\n+", "", msg)
    res = ""
    if msg == "Arsenal":
        res = msg.replace("Arsenal", "ARS")
    elif msg == "AFC Bournemouth":
        res = msg.replace("AFC Bournemouth", "BOU")
    elif msg == "Bournemouth":
        res = msg.replace("Bournemouth", "BOU")
    elif msg == "Aston Villa":
        res = msg.replace("Aston Villa", "AVL")
    elif msg == "Brentford":
        res = msg.replace("Brentford", "BRE")
    elif msg == "Brighton and Hove Albion" or msg == "Brighton & Hove Albion":
        res = msg.replace(msg, "BHA")
    elif msg == "Chelsea":
        res = msg.replace("Chelsea", "CHE")
    elif msg == "Crystal Palace":
        res = msg.replace("Crystal Palace", "CRY")
    elif msg == "Everton":
        res = msg.replace("Everton", "EVE")
    elif msg == "Fulham":
        res = msg.replace("Fulham", "FUL")
    elif msg == "Leeds United":
        res = msg.replace("Leeds United", "LEE")
    elif msg == "Leicester City":
        res = msg.replace("Leicester City", "LEI")
    elif msg == "Liverpool":
        res = msg.replace("Liverpool", "LIV")
    elif msg == "Manchester City":
        res = msg.replace("Manchester City", "MCI")
    elif msg == "Manchester United":
        res = msg.replace("Manchester United", "MUN")
    elif msg == "Newcastle United":
        res = msg.replace("Newcastle United", "NEW")
    elif msg == "Nottingham Forest":
        res = msg.replace("Nottingham Forest", "NFO")
    elif msg == "Southampton":
        res = msg.replace("Southampton", "SOU")
    elif msg == "Tottenham Hotspur" or msg == " Tottenham":
        res = msg.replace(msg, "TOT")
    elif msg == "West Ham United":
        res = msg.replace("West Ham United", "WHU")
    elif msg == "Wolverhampton Wanderers" or msg == "Wolverhampton":
        res = msg.replace(msg, "WOL")
    else:
        pass
    return res


# /start - starts when bot runs
def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(
        f"Hello  {first_name}  🚀 \nWelcome To Match Notifier Bot!"
    )


def helps(update, context):
    update.message.reply_text(
        """
  The following commands are available:
  /start -> Welcome Message
  /fixtures -> This Week Matchs
  /table -> EPL Table
  /contact -> Contact Dev
  /help  ->  Help Commands
  /comments -> Comment about the Bot
  """
    )


def contact(update, context):
    update.message.reply_text(
        """
Phone No : +251966427203
Telegram : https://t.me/HuluWZ

  """
    )


def fixtures(update, context):
    url = "https://www.bbc.com/sport/football/premier-league/scores-fixtures"
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    div = soup.find("div", class_="qa-match-block")
    ui = div.find(
        "ul",
        class_="gs-o-list-ui gs-o-list-ui--top-no-border gs-o-list-ui--bottom-no-border",
    )
    title = soup.find("h3", class_="gel-minion sp-c-match-list-heading").text
    title = title.split()
    tabless = pt.PrettyTable([" PL Fixtures"])
    # tabless.align['Time'] = 'r'
    tabless.set_style(ORGMODE)

    title = f" {title[0]},  {title[2]} {title[1][:2]} "
    lop = []
    # # Collecting Ddata
    for row in ui:
        homeTeam = row.find(
            "span",
            class_="gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc",
        ).text
        homegoal = row.find("span", class_="sp-c-fixture__block").span.text
        awayTeam = row.find(
            "span",
            class_="sp-c-fixture__team sp-c-fixture__team--time sp-c-fixture__team--time-away",
        ).span.span.text
        homeTeam = replacer(homeTeam)
        awayTeam = replacer(awayTeam)
        displayAll = f"{homeTeam}  {homegoal}  {awayTeam}"
        lop.append((displayAll))
        # update.message.reply_text(f"{homeTeam}  \t{homegoal}\t {awayTeam}")
    for a in lop:
        tabless.add_row([a])
    tabless = tabless.get_string(title=title)
    update.message.reply_text(f'```{tabless}```', parse_mode=ParseMode.MARKDOWN_V2)


def liveScore(update,context):
    url = "https://api.sofascore.com/api/v1/sport/football/events/live"
    payload = ""
    headers ={
    "authority": "api.sofascore.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.7",
    "cache-control": "max-age=0",
    "if-none-match": "W/'d4c91ff73f",
    "origin": "https://www.sofascore.com",
    "referer": "https://www.sofascore.com/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    data = response.json()
    topLeague = ["LaLiga","Serie A","Ligue 1","Bundesliga","Premier League",
     "UEFA Champions League, Group A","UEFA Champions League, Group B","UEFA Champions League, Group C","UEFA Champions League, Group D","UEFA Champions League, Group E","UEFA Champions League, Group F","UEFA Champions League, Group G","UEFA Champions League, Group H",
     "UEFA Europa League, Group A","UEFA Europa League, Group B","UEFA Europa League, Group C","UEFA Europa League, Group D","UEFA Europa League, Group E","UEFA Europa League, Group F","UEFA Europa League, Group H"]
    topCountry = ["Spain","Germany","Italy","England","France","Europe"]
    msg = " No Live Matches !"
    tabless = pt.PrettyTable(["League","Status"])
    tabless.set_style(MSWORD_FRIENDLY)
    # tabless.align = 'c'
    lop = []
    for game in data['events']:
       league = game['tournament']['name']
       country = game['tournament']['category']['name']
       if league not in topLeague:
         continue
       if country not  in topCountry:
         continue
       if "UEFA Champions League" in league:
            leagueName = league.split(",")[1]
            leagueName = str(leagueName).strip()
            leagueName = leagueName.split(" ")[1]
            league = f"UCL-Grp {leagueName}"
       if "UEFA Europa League" in league:
            leagueName = league.split(",")[1]
            leagueName = str(leagueName).strip()
            leagueName = leagueName.split(" ")[1]
            league = f"UEL-Grp {leagueName}"
       league = "PL" if league == "Premier League" else league
       league = "LL" if league == "LaLiga" else league
       league = "SA" if league == "Serie A" else league
       league = "L1" if league == "Ligue 1" else league
       league = "BL" if league == "Bundesliga" else league
    #    homeTeam = game['homeTeam']['name']
       homeCode = game['homeTeam']['nameCode']
    #    awayTeam = game['awayTeam']['name']
       awayCode = game['awayTeam']['nameCode']
       homeScore = game['homeScore']['current']
       awayScore = game['awayScore']['current']
    #    displayAll = f"{homeCode} {homeScore} - {awayScore} {awayCode}"
       status = game['status']['description']
       start = game['startTimestamp']
       now = datetime.datetime.now()
       now = int(round(now.timestamp()))
       td = now - start
       td_mins = int(round(td/60))

       if status == "Halftime":
          status = "HT " 
       elif status == "Fulltime":
          status ="FT "
       elif td_mins < 10 and status == "1st half" and td_mins > 0:
          status =f"0{td_mins}'"
       elif td_mins > 45 and status != "2nd half":
          status = f"45+"
       elif td_mins > 45 and status == "2nd half":
          halfStart = game['time']['currentPeriodStartTimestamp']
          status = int(round((now - halfStart)/60)) + 46
          status = "90+" if status > 90 else status
          status = f"{status}'"
       else:
         status = f"{td_mins}'"   
        
       displayAll = f"{homeCode} {homeScore} - {awayScore} {awayCode} {status}"
       lop.append((league,displayAll))

    for a, b in lop:
        tabless.add_row([a,b])
    
    tabless = tabless.get_string(title="Live Match Score")
    if len(lop) > 0:
        update.message.reply_text(f'```{tabless}```', parse_mode=ParseMode.MARKDOWN_V2)
    else:
        update.message.reply_text(f"{msg}")

def get_epl_table(update, context):

    url = "https://api.sofascore.com/api/v1/unique-tournament/17/season/41886/standings/total"
    payload = ""
    headers = {
        "authority": "api.sofascore.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.8",
        "cache-control": "max-age=0",
        "if-none-match": "W/^\^0da734c3d4^^",
        "origin": "https://www.sofascore.com",
        "referer": "https://www.sofascore.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36",
    }
    all = []
    response = requests.request("GET", url, data=payload, headers=headers)
    data = response.json()
    # update.message.reply_text(f"PL Table 2022/23")
    tabless = pt.PrettyTable(['#','T',"P" ,"GD","Pt"])
    tabless.set_style(MARKDOWN)
    # tabless.align = 'l'
    lop = []
    # update.message.reply_text(f"# \t T  \tP \tW \tD \tL \tGD \tPt")
    for game in data["standings"]:
        for games in game["rows"]:
            position = games["position"]
            nameCode = games["team"]["nameCode"]
            matches = games["matches"]
            wins = games["wins"]
            draws = games["draws"]
            # losses = games["losses"]
            points = games["points"]
            goalD = games["scoresFor"] - games["scoresAgainst"]
            windraw = f"{wins}|{draws}"
            lop.append((position,nameCode,matches,goalD,points))
    for a, b, c, d,g in lop:
       tabless.add_row([a,b,c,d,g])
    tabless = tabless.get_string(title="EPL Table 2022/23")
    update.message.reply_text(f'```{tabless}```', parse_mode=ParseMode.MARKDOWN_V2)

   
def topScorer(update, context):
    url = "https://www.bbc.com/sport/football/premier-league/top-scorers"
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    tables = soup.find("table", class_="gs-o-table")
    lop = []
    tabless = pt.PrettyTable(['#','N','P',"G"])
    tabless.set_style(MSWORD_FRIENDLY)
    # tabless.set_style(ORGMODE)
    # tabless.align = 'l'

    for row in tables.tbody.find_all("tr")[0:5]:
        # Find all data for each column
        columns = row.find_all("td")
        if columns != []:
          r = columns[0].text.strip()
          n = columns[1].find("span", class_="gs-u-vh gs-u-display-inherit@l").text
          if len(n)>14:
            n = f"{n[:14]}."
          g = columns[2].text.strip()
          a = columns[3].text.strip()
          p = columns[4].text.strip()
        #   ga = f"{g}+{a}"
        #   gp = columns[5].text.strip()
          lop.append((r,n, p, g))

    for a, b, c, d  in lop:
        tabless.add_row([a,b,c,d])
    tabless = tabless.get_string(title="EPL Top Scorers")
    update.message.reply_text(f'```{tabless}```', parse_mode=ParseMode.MARKDOWN_V2)



updater = telegram.ext.Updater(
    "5714068437:AAFwAi-6HwfVEbSVsbAhwEffeHJ8atACEAc", use_context=True
)
disp = updater.dispatcher
#
disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("table", get_epl_table))
disp.add_handler(telegram.ext.CommandHandler("contact", contact))
disp.add_handler(telegram.ext.CommandHandler("scorer", topScorer))
disp.add_handler(telegram.ext.CommandHandler("fixtures", fixtures))
disp.add_handler(telegram.ext.CommandHandler("live", liveScore))

updater.start_polling()
updater.idle()
