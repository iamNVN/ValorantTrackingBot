import mysql.connector as mysql

db = mysql.connect(
  host="localhost",
  user="root",
  password="",
  database='discord'
)

cursor = db.cursor()

def player_exists_in_db(player):
    sql = "SELECT * FROM players WHERE player='{}'".format(player)
    cursor.execute(sql)
    exist = cursor.fetchone()
    if exist is None:
        return False
    else:
        return True
    

def add_to_watchlist(player,channel,region,last_match_id):
    if not player_exists_in_db(player):
        sql1 = "INSERT INTO players (player,region,last_match_id) VALUES ('{}','{}','{}')".format(player,region,last_match_id)
        cursor.execute(sql1)
        
    sql = "INSERT INTO channels (channel_id, player) VALUES ('{}','{}')".format(channel,player)
    cursor.execute(sql)
    db.commit()

def remove_from_watchlist(player,channel):
    sql = "DELETE FROM channels WHERE channel_id = '{}' AND player='{}'".format(channel,player)
    cursor.execute(sql)
    
    sql1 = "SELECT count(*) FROM channels WHERE player = '{}' ".format(player)
    cursor.execute(sql1)
    count = cursor.fetchone()[0]
    if count < 1:
        sql2 = "DELETE FROM players WHERE player='{}'".format(player)
        cursor.execute(sql2)
        
    db.commit()

def is_user_already_watched(player,channel):
    if not player_exists_in_db(player):
        return False
    sql = "SELECT * FROM channels WHERE channel_id = '{}' AND player='{}'".format(channel,player)
    cursor.execute(sql)
    exist = cursor.fetchone()
    if exist is None:
        return False
    else:
        return True

def get_watchlist(channel):
    sql = "SELECT player FROM channels WHERE channel_id = '{}' ".format(channel)
    cursor.execute(sql)
    results = cursor.fetchall()
    row_count = cursor.rowcount
    if row_count == 0:
        return None
    else:
        return results

def get_last_matchid(player):
    sql = "SELECT last_match_id FROM players WHERE player = '{}' ".format(player)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]

def update_last_match(player,matchid):
    sql = "UPDATE players SET last_match_id = '{}' WHERE player = '{}' ".format(matchid,player)
    cursor.execute(sql)
    db.commit()

def get_watched_players():
    sql = 'SELECT t1.player from players t1, channels t2 WHERE t2.player = t1.player GROUP BY t1.player HAVING count(t2.channel_id) > 0'
    cursor.execute(sql)
    results = cursor.fetchall()
    row_count = cursor.rowcount
    if row_count == 0:
        return None
    else:
        return [item[0] for item in results]
    
def get_player_channels(player):
    sql = "SELECT channel_id FROM channels WHERE player = '{}' ".format(player)
    cursor.execute(sql)
    results = cursor.fetchall()
    row_count = cursor.rowcount
    if row_count == 0:
        return None
    else:
        return [item[0] for item in results]