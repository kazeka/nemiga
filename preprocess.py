#!/usr/bin/env python3

import json
import pandas as pd
import sqlalchemy
import sys


def main(fname='data.json'):
    with open(fname, 'r') as fp:
        data = json.load(fp)

    def _sumup_teams(d, team_sums):
        # base case: size of team is 1
        if not d['refs']:
            team_sums[d['id']] = [d['refs'], 1]
            return 1
        # recursive case: size of team is 1 + size of teams recommended by recommended users
        else:
            team_sums[d['id']] = [[i['id'] for i in d['refs']], sum([_sumup_teams(i, team_sums) for i in d['refs']])]
            return 1 + sum([_sumup_teams(i, team_sums) for i in d['refs']])

    team_sums = dict()
    _sumup_teams(data, team_sums)


    df = pd.DataFrame.from_dict({
        'id': team_sums.keys(), 
        'refs': [i[0] for i in team_sums.values()], 
        'team_size':  [i[1] for i in team_sums.values()]})

    # DEBUG: check
    # df[df['id'].str.match('01GTXNX97R9RRQ4JYVECEVA081')]
    # df[df['id'].str.match('01GTXNX97R9RRQ4JYVECEVA081')]['refs'].str.len()
    # df[df['id'].str.match('01GTXNX97R9RRQ4JYVECEVA081')]['refs'].str.get(1)

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

    # prepare refs table
    db_refs = []
    for i in df.itertuples():
        if i.refs:
            for j in i.refs:
                db_refs.append([i.id, j])


    # export to sqlite
    engine = sqlalchemy.create_engine('sqlite:///./mmm.db')
    db_users = df.drop(columns=['refs'])
    db_users.to_sql('users', con=engine, if_exists='replace', dtype={
        'id': sqlalchemy.Text,
        'team_size': sqlalchemy.Integer,
        'level': sqlalchemy.Text,
    })
    
    pd.DataFrame(db_refs, columns=['origin', 'dst']).to_sql('refs', con=engine, if_exists='replace')

    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit(main(sys.argv[1]))
    else:
        raise SystemExit(main())