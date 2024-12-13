from bs4 import BeautifulSoup
import pandas as pd 
import requests

bet_types = ["Over/Under", "Moneyline", "Player Props"]
def player_name(first_name, last_name):
  first_name = first_name.replace(" ", "").lower()
  last_name = last_name.replace(" ", "").lower()
  return last_name[:5] + first_name[:2]

def team_name(name):
    team_abbreviations = {
            "Golden State Warriors": "GSW",
            "Los Angeles Lakers": "LAL",
            "Chicago Bulls": "CHI",
            "Miami Heat": "MIA",
            "Boston Celtics": "BOS",
            "Toronto Raptors": "TOR",
            "New York Knicks": "NYK",
            "Houston Rockets": "HOU",
            "Philadelphia 76ers": "PHI",
            "Dallas Mavericks": "DAL",
            "San Antonio Spurs": "SAS",
            "Phoenix Suns": "PHX",
            "Milwaukee Bucks": "MIL",
            "Denver Nuggets": "DEN",
            "Utah Jazz": "UTA",
            "Cleveland Cavaliers": "CLE",
            "Atlanta Hawks": "ATL",
            "Brooklyn Nets": "BKN",
            "Portland Trail Blazers": "POR",
            "Washington Wizards": "WAS",
            "Minnesota Timberwolves": "MIN",
            "Orlando Magic": "ORL",
            "Charlotte Hornets": "CHA",
            "Sacramento Kings": "SAC",
            "New Orleans Pelicans": "NOP",
            "Oklahoma City Thunder": "OKC",
            "Detroit Pistons": "DET",
            "Indiana Pacers": "IND",
            "Memphis Grizzlies": "MEM",
        }
    return team_abbreviations[name]

def create_url_player(name):
  initial = name[0]
  url = f"https://www.basketball-reference.com/players/{initial}/{name}01.html"
  return url

def create_url_team(team_name):
  url = f"https://www.basketball-reference.com/teams/{team_name}/2025_games.html"
  return url

def scrape_team_stats(url):
  response = requests.get(url)
  response.raise_for_status()  

  soup = BeautifulSoup(response.text, 'html.parser')
  table = soup.find('table', id='games')
  if not table:
      raise ValueError("Table with ID 'games' not found!")

  data = []
  rows = table.find_all('tr') 
  for row in rows[1:]:
      cols = row.find_all('td') 
      cols_text = [col.text.strip() for col in cols] 
      if cols_text: 
          data.append(cols_text)

  df = pd.DataFrame(data, columns=["G", "", "Date", "Start", "", "Opp", "W/L", "OT", "TP", "OP", "W", "L", "Streak", "Attend.", "LOG", "Notes"])
  df = df.tail(5)

def scrape_player_stats(url):
  response = requests.get(url)
  response.raise_for_status()  

  soup = BeautifulSoup(response.text, 'html.parser')

  table = soup.find('table', id='last5')
  if not table:
      raise ValueError("Table with ID 'last5' not found!")

  data = []
  rows = table.find_all('tr') 
  for row in rows[1:]:
      cols = row.find_all('td') 
      cols_text = [col.text.strip() for col in cols] 
      if cols_text: 
          data.append(cols_text)

  df = pd.DataFrame(data, columns=["Date", "Team", "Opp", "Result", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT",
                                    "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS", "GmSc", "+/-"])
  return df 

def get_odds():
    odds = input()
    if odds > 0:
        odds = abs(odds)
    else: 
        pass

def calculate_ev(odds, amt_wagered, profit_on_win, profit_on_loss):
    if odds > 0:
        implied_prob = odds / (odds + 100)
    else:
        implied_prob = 100 / (abs(odds) + 100)
    if profit_on_win is None:
        profit_on_win = amt_wagered * (odds / 100 if odds > 0 else 100 / abs(odds))
    if profit_on_loss is None:
        profit_on_loss = -amt_wagered
    expected_profit = (implied_prob * profit_on_win) + ((1 - implied_prob) * profit_on_loss)
    expected_value = expected_profit

    return {
        "implied_probability": implied_prob,
        "expected_profit": expected_profit,
        "expected_value": expected_value
    }

def take_leg(bet_type, df):
    if bet_type == bet_types[1]:
        over_under = input("Was your stat an over or under? (over/under): ").lower() #in dropdown menu
        if over_under == "over":
            comparison_operator = ">"
        elif over_under == "under":
            comparison_operator = "<"
        else:
            print("Invalid input for over/under. Please try again.")
            return

        stat = input("What stat was your bet? ").strip() #in dropdown menu
        stat_number = float(input("What is the bet over/under number? ")) #in dropdown menu

        times_true = 0

        if stat not in df.columns:
            print(f"Stat '{stat}' not found in the player stats dataframe.")
            return

        for index, row in df.iterrows():
            player_stat = float(row[stat])
            if comparison_operator == ">" and player_stat > stat_number:
                times_true += 1
            elif comparison_operator == "<" and player_stat < stat_number:
                times_true += 1

        print(f"The condition was met {times_true} times.")

        return times_true
    else:
        print("Bet type not recognized or not supported.")
        return


def rate_leg(bet_type):
    if take_leg() >= 3:
        return "Good"
    else: 
        return "Bad"

## do in a dropdown menu 
name = player_name("Cade", "Cunningham")
url = create_url_player(name)
df = scrape_player_stats(url)
take = take_leg(bet_types[1], df)
print(take)
