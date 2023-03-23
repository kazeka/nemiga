#!/usr/bin/env python3

import json
import networkx
import pandas as pd
import sqlalchemy


def main():
    with open('data.json', 'r') as fp:
        data = json.load(fp)

    team_sums = {}
    def sum_teams(d, team_sums):
        if not d['refs']:
            team_sums[d['id']] = [d['refs'], 1]
            return 1
        else:
            team_sums[d['id']] = [[i['id'] for i in d['refs']], sum([sum_teams(i, team_sums) for i in d['refs']])]
            return sum([sum_teams(i, team_sums) for i in d['refs']])

    sum_teams(data, team_sums)


    df = pd.DataFrame.from_dict({
        'id': team_sums.keys(), 
        'refs': [i[0] for i in team_sums.values()], 
        'team_size':  [i[1] for i in team_sums.values()]})

    # check
    df[df['id'].str.match('01GTXNX97R9RRQ4JYVECEVA081')]
    df[df['id'].str.match('01GTXNX97R9RRQ4JYVECEVA081')]['refs'].str.len()
    df[df['id'].str.match('01GTXNX97R9RRQ4JYVECEVA081')]['refs'].str.get(1)

    # assign levels
    df['level'] = ['V1'] * len(df)
    df.loc[(df['team_size'] > 20) & (df['refs'].str.len() >= 3), 'level'] = 'V2'

    V2 = set(df[df['level'] == 'V2']['id'].tolist())
    for index, row in df[(df['team_size'] > 100) & (df['refs'].str.len() >= 5)].iterrows():
        refs = set(row['refs'])
        if len(V2 & refs) >= 3:
            df.at[index, 'level'] = 'V3'

    V3 = set(df[df['level'] == 'V3']['id'].tolist())
    for index, row in df[(df['team_size'] > 300) & (df['refs'].str.len() >= 8)].iterrows():
        refs = set(row['refs'])
        if len(V3 & refs) >= 3:
            df.at[index, 'level'] = 'V4'

    V4 = set(df[df['level'] == 'V4']['id'].tolist())
    for index, row in df[(df['team_size'] > 800) & (df['refs'].str.len() >= 12)].iterrows():
        refs = set(row['refs'])
        if len(V4 & refs) >= 3:
            df.at[index, 'level'] = 'V5'

    V5 = set(df[df['level'] == 'V5']['id'].tolist())
    for index, row in df[(df['team_size'] > 1500) & (df['refs'].str.len() >= 20)].iterrows():
        refs = set(row['refs'])
        if len(V5 & refs) >= 3:
            df.at[index, 'level'] = 'V6'

    # export to sqlite
    engine = sqlalchemy.create_engine('sqlite:///./mmm.db')
    db_df = df.drop(columns=['refs'])
    db_df.to_sql('users', con=engine, if_exists='replace', dtype={
        'id': sqlalchemy.Text,
        'team_size': sqlalchemy.Integer,
        'level': sqlalchemy.Text,
    })

    return 0


if __name__ == "__main__":
    raise SystemExit(main())