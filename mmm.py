'''
Made with ChatGPT
'''

from fastapi import FastAPI
from starlette.responses import RedirectResponse

import sqlite3
import networkx as nx


class TeamManager():
    def __init__(self):
        # connect to the database
        conn = sqlite3.connect('mmm.db')

        # create a networkx graph
        self.G = nx.DiGraph()

        # fetch nodes from users table and add them to the graph
        cursor = conn.execute('SELECT id, level FROM users')
        for row in cursor:
            node_id, level = row
            self.G.add_node(node_id, level=level)

        # fetch edges from refs table and add them to the graph
        cursor = conn.execute('SELECT origin, dst FROM refs')
        for row in cursor:
            origin, dst = row
            self.G.add_edge(origin, dst)

        # close the database connection
        conn.close()

        # DEBUG: save G
        nx.write_gpickle(self.G, 'G.pickle')
    

    def get_payout(self, level, depth):
        if depth == 1:
            if level == 'V1':
                return 30
            if level == 'V2':
                return 40
            if level == 'V3':
                return 50
            if level == 'V4':
                return 60
            if level == 'V5':
                return 65
            if level == 'V6':
                return 70
        
        if depth == 2:
            if level == 'V2':
                return 10
            if level == 'V3':
                return 20
            if level == 'V4':
                return 30
            if level == 'V5':
                return 35
            if level == 'V6':
                return 40
        
        if depth == 3:
            if level == 'V3':
                return 10
            if level == 'V4':
                return 20
            if level == 'V5':
                return 25
            if level == 'V6':
                return 30
        
        if depth == 4:
            if level == 'V4':
                return 10
            if level == 'V5':
                return 15
            if level == 'V6':
                return 20
        
        if depth == 5:
            if level == 'V5':
                return 5
            if level == 'V6':
                return 10
        
        if depth == 5 and level == 'V6':
            return 5



    def get_level_for(self, member_id):
        if member_id not in self.G:
            return {'user_id': member_id, 'level': 'No such member'}
        
        level = nx.get_node_attributes(self.G, 'level')
        return {'user_id': member_id, 'level': level[member_id]}


    # NOTE: only valid for leaf nodes as there is no way to verify levels in the past
    def get_payouts_for(self, member_id):
        if member_id not in self.G:
            return {'user_id': member_id, 'level': 'No such member'}
        
        level = nx.get_node_attributes(self.G, 'level')
        resp = [{'user_id': member_id, 'level': level[member_id], 'amount': -120}]
        payout_depth = 1
        for p in self.G.predecessors(member_id):
            payout = self.get_payout(level[p], payout_depth)
            payout_depth += 1
            resp.append({'user_id': p, 'level': level[p], 'amount': payout})

        return resp
        


mngr = TeamManager()
app = FastAPI()

@app.get('/')
def root():
    # TODO: fix sorting
    global mngr
    level = nx.get_node_attributes(mngr.G, 'level')
    return RedirectResponse(f'/get_level_for/{max(level)}')

@app.get('/get_level_for/{user_id}')
def get_level_for(user_id: str):
    global mngr
    return mngr.get_level_for(user_id)


@app.get('/get_payouts_for/{user_id}')
def get_payouts_for(user_id: str):
    global mngr
    return mngr.get_payouts_for(user_id)
