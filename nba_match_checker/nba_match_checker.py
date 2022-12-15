import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

MATCH_DAY = (datetime.date.today() - relativedelta(days=1)).strftime('%Y-%m-%d')

# MATCH_DAY = '2022-12-07'

r = requests.get(f'https://www.nba.com/games?date={MATCH_DAY}')
soup = BeautifulSoup(r.text, 'html.parser')
matches = []
for game in soup.findAll('div', {'class': "GameCard_gc__UCI46 GameCardsMapper_gamecard__pz1rg"}):
    teams = []
    for team in game.findAll('span', {'class': 'MatchupCardTeamName_teamName__9YaBA'}):
        teams.append(team.text)
    records = []
    for record in game.findAll('p', {'class': 'MatchupCardTeamRecord_record__20YHe'}):
        records.append(record.text)
    scores = []
    for score in game.findAll('p', {'class': 'MatchupCardScore_p__dfNvc GameCardMatchup_matchupScoreCard__owb6w'}):
        scores.append(score.text)
    final_result = 'NA'
    for result in game.findAll('p', {'class': 'GameCardMatchupStatusText_gcsText__PcQUX'}):
        final_result = result.text
    leaders = []
    for pra in game.findAll('td'):
        if pra.text.isdigit():
            leaders.append(int(pra.text))

    matches.append([teams[0], records[0], scores[0], teams[1], records[1], scores[1], final_result,
                    leaders[0], leaders[1], leaders[2], leaders[3], leaders[4], leaders[5]])

matches_df = pd.DataFrame(matches, columns=['AWAY', 'AWAY_RECORD', 'AWAY_SCORE',
                                            'HOME', 'HOME_RECORD', 'HOME_SCORE', 'RESULT',
                                            'AL_PTS', 'AL_REB', 'AL_AST', 'HL_PTS',
                                            'HL_REB', 'HL_AST'])

matches_df['RECORD_DIFF%'] = matches_df.apply(lambda x: abs(int(x['AWAY_RECORD'].split('-')[0]) -
                                                            int(x['HOME_RECORD'].split('-')[0]))/(int(x['AWAY_RECORD'].split('-')[0]) + int(x['AWAY_RECORD'].split('-')[1])), axis=1)


# Result increase for teams with similar record
matches_df['MATCH_RESULT'] = matches_df['RECORD_DIFF%'].apply(lambda x: 1 if x < 0.25 else 0)
# result increase for close match and for big leaders scores
for i in range(len(matches_df)):
    points_diff = abs(int(matches_df.loc[i, 'AWAY_SCORE']) - int(matches_df.loc[i, 'HOME_SCORE']))
    if points_diff < 10 and points_diff > 3:
        matches_df.loc[i, 'MATCH_RESULT'] += 1
    elif points_diff <= 3:
        matches_df.loc[i, 'MATCH_RESULT'] += 2

for i in range(len(matches_df)):
    if matches_df.loc[i, 'AL_PTS'] > 30 or matches_df.loc[i, 'HL_PTS'] > 30:
        matches_df.loc[i, 'MATCH_RESULT'] += 1
    elif matches_df.loc[i, 'AL_PTS'] > 40 or matches_df.loc[i, 'HL_PTS'] > 40:
        matches_df.loc[i, 'MATCH_RESULT'] += 2
    elif matches_df.loc[i, 'AL_PTS'] > 50 or matches_df.loc[i, 'HL_PTS'] > 50:
        matches_df.loc[i, 'MATCH_RESULT'] += 3

for i in range(len(matches_df)):
    if matches_df.loc[i, 'AL_REB'] > 20 or matches_df.loc[i, 'HL_REB'] > 20:
        matches_df.loc[i, 'MATCH_RESULT'] += 1
    if matches_df.loc[i, 'AL_AST'] > 15 or matches_df.loc[i, 'HL_AST'] > 15:
        matches_df.loc[i, 'MATCH_RESULT'] += 1

# Points for OT
matches_df['MATCH_RESULT'] = matches_df.apply(lambda x: x['MATCH_RESULT'] + 1 if 'OT' in x['RESULT'] else x['MATCH_RESULT'], axis=1)

score_df = matches_df[['AWAY', 'HOME', 'MATCH_RESULT']]
score_df.to_excel('today_matches_to_watch.xlsx', index=False)