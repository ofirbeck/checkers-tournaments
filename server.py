# -*- coding: utf-8 -*-
from checkers.constants import *
import socket
import select
import sqlite3
import random
import threading
import time
import bcrypt
import os.path
"""
The DB:
username (text)
password (text)
games_wins integer
tournaments_wins integer
is_guest text
"""
# Checking if the DB exists,
# if not it creates it along with 10 users in order to show the Top 10 in games and tournaments
if os.path.isfile('users.db'):
    USERS = sqlite3.connect('users.db')
    U = USERS.cursor()
else:
    USERS = sqlite3.connect('users.db')
    U = USERS.cursor()
    U.execute("""CREATE TABLE users(
              username text,
              password text,
              games_wins integer,
              tournaments_wins integer,
              is_guest text
              )""")
    hashed = bcrypt.hashpw(b'Pler', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("George", hashed, 10, 11, "No"))
    USERS.commit()
    hashed = bcrypt.hashpw(b'Volt3', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("Sival", hashed, 4, 5, "No"))
    USERS.commit()
    hashed = bcrypt.hashpw(b'Keller', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("Jo", hashed, 10, 11, "No"))
    USERS.commit()
    hashed = bcrypt.hashpw(b'Kim4', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("Kim", hashed, 6, 3, "No"))
    USERS.commit()
    hashed = bcrypt.hashpw(b'Jeo4f', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("Jeff", hashed, 10, 11, "No"))
    USERS.commit()
    hashed = bcrypt.hashpw(b'Kremar2', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("Alon", hashed, 10, 11, "No"))
    USERS.commit()
    hashed = bcrypt.hashpw(b'Dana22', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("Danny", hashed, 1, 5, "No"))
    USERS.commit()
    hashed = bcrypt.hashpw(b'Daniel5', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("Gabriel6", hashed, 1, 4, "No"))
    USERS.commit()
    hashed = bcrypt.hashpw(b'dona244', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("Dona23456", hashed, 1, 0, "No"))
    USERS.commit()
    hashed = bcrypt.hashpw(b'MarkMM2', SALT.encode('utf-8'))
    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", ("Markus222", hashed, 1, 0, "No"))
    USERS.commit()
save_winners = [[]]
open_sockets = []

for i in range(0, 1000):
    save_winners.append([])


def managing_a_game(players, pin):
    # This function manges a single game
    # The server is responsible for sending each player move to the other
    # when one player wins, the username of the winner is saved
    # The counter of wins of the winner in the DB gets increased by one
    users2 = sqlite3.connect('users.db')
    u2 = users2.cursor()
    global save_winners, open_sockets
    red_player = random.choice(players)
    if players[0] == red_player:
        white_player = players[1]
    else:
        white_player = players[0]
    time.sleep(1)
    red_player.sendall("Your color is red-")
    white_player.sendall("Your color is white-")
    time.sleep(random.randint(1, 2))
    turn = white_player
    waiting = red_player
    game_runs = True
    while game_runs:
        time.sleep(0.2)
        waiting.sendall("It's the other player's turn")
        turn.sendall("Your turn is now")
        time.sleep(1)
        msg = turn.recv(1024)
        if msg.isdigit() == False:
            game_runs = False
            reply1 = msg
            reply2 = waiting.recv(1024)
            if reply1 == "Not me":
                open_sockets.append(turn)
                winner_username = reply2
                if pin is not None:
                    save_winners[pin].append(waiting)
                else:
                    open_sockets.append(waiting)
            else:
                winner_username = reply1
                open_sockets.append(waiting)
                if pin is not None:
                    save_winners[pin].append(turn)
                else:
                    open_sockets.append(turn)
            u2.execute("SELECT games_wins FROM users WHERE username = :username", {'username': winner_username})
            wins_total = u2.fetchone()
            if wins_total is not None:
                wins_total = wins_total[0]
                wins_total += 1
                update = str(wins_total)
                u2.execute("UPDATE users SET games_wins = :games_wins WHERE username = :username", {'games_wins': update, 'username': winner_username})
                users2.commit()
        else:
            waiting.sendall(msg)
            save = turn
            turn = waiting
            waiting = save
    turn.sendall(ENDGAME)
    waiting.sendall(ENDGAME)
    print "A game ended"


def managing_a_tournament(sockets, tour_name, pin):
    # sockets - contains the sockets of the players in the current round
    # each round, each player gets a random one to play with
    # the socket of the winners in each round will be saved in the global array save_winners,in an index equal to the PIN
    # the tournament will continue to the next round the number of games that took place equal to the number of winners
    # in the array, it will go on and on until one remains
    global save_winners, open_sockets
    save_winners[pin] = []
    index_jumps_one = 0
    threads = []
    while len(sockets) > 1:
        print sockets
        save_winners[pin] = []
        for b in range(0, len(sockets), 2):
            wait_games = [sockets[b], sockets[b+1]]
            sockets[b].sendall("The game starts")
            sockets[b+1].sendall("The game starts")
            time.sleep(random.randint(1, 2))
            threads.append(threading.Thread(target=managing_a_game, args =(wait_games, pin)))
            threads[index_jumps_one].start()
            index_jumps_one += 1
        for thread in threads:
            thread.join()
        sockets = save_winners[pin]
    time.sleep(2)
    sockets[0].sendall("You are the grand winner of the tournament!")
    winner_username = sockets[0].recv(1024)
    open_sockets.append(sockets[0])
    users3 = sqlite3.connect('users.db')
    u3 = users3.cursor()
    u3.execute("SELECT tournaments_wins FROM users WHERE username = :username", {'username': winner_username})
    wins_total = u3.fetchone()
    if wins_total is not None:
        wins_total = wins_total[0]
        wins_total += 1
        update = str(wins_total)
        u3.execute("UPDATE users SET tournaments_wins = :tournament_wins WHERE username = :username", {'tournament_wins': update, 'username': winner_username})
        users3.commit()


def main():
    global open_sockets
    socket_name = {}
    open_sockets = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, PORT_SERVER))
    server.listen(5)
    wait_games = []
    tournaments_players = [[]]
    games_players_with_pin = [[]]
    tournaments_names = []
    tournaments_num_of_players = []
    for i in range(0, 1000):
        # setting up 4 arrays:
        # tournaments_names - contains the name of the tournament according to his pin(index = pin)
        # tournaments_players - contains the sockets of the players in that tournament(in the same way above)
        # tournaments_num_of_players - contains the number of players defined to the tournament
        # games_players_with_pin - this array works as the tournaments_players,
        # but for 2 players,manging the single games with a pin.
        tournaments_names.append("")
        tournaments_players.append([])
        games_players_with_pin.append([])
        tournaments_num_of_players.append(0)
    while True:
        # This loop constantly searches for new connections and messages.
        # Messages to the server are in the following structure:
        # THE TYPE OF THE MESSAGE + '-' + the message
        # (sometimes there are more than one '-' to divide the parts of the message)
        # Than the message is getting splited by '-'
        # Than the type of the message is getting checked and the suitable actions will take place according to it
        rlist, wlist, xlist = select.select([server] + open_sockets, open_sockets, [], 1)
        for current_socket in rlist:
            if current_socket is server:
                (new_sock, address) = server.accept()
                open_sockets.append(new_sock)
            else:
                # splits the data the server got, and then checks it's type
                data = current_socket.recv(1024)
                mail = data.split('-')
                if mail[0] == QUIT:
                    open_sockets.remove(current_socket)
                    if mail[1] != "":
                        U.execute("DELETE FROM users WHERE username = :username", {'username': mail[1]})
                        USERS.commit()
                elif mail[0] == CHECKSIGN:
                    # structure: CHECKSIGN-USERNAME-PASSWORD
                    # if a client wants to sign up, checks if the username or password aren't already in the DB
                    # if not, add them to the DB and send a suitable msg to the client
                    U.execute("SELECT * FROM users WHERE username = :username", {'username': mail[1]})
                    check_username = U.fetchone()
                    hashed_password = bcrypt.hashpw(bytes(mail[2]), SALT.encode('utf-8'))
                    print hashed_password
                    U.execute("SELECT * FROM users WHERE password = :password", {'password': hashed_password})
                    check_password = U.fetchone()
                    print check_password
                    if check_password is None and check_username is None:
                        current_socket.sendall('You can use it')
                        U.execute("INSERT INTO users VALUES(?,?,?,?,?)", (mail[1], hashed_password, 0, 0, "No"))
                        USERS.commit()
                        socket_name[current_socket] = mail[1]
                    elif check_username is not None and check_password is not None:
                        current_socket.sendall("This username and password have been already taken")
                    elif check_username is not None:
                        current_socket.sendall("This username has been already taken")
                    elif check_password is not None:
                        current_socket.sendall("This password has been already taken")
                elif mail[0] == CHECKLOGIN:
                    # structure: CHECKLOGIN-USERNAME-PASSWORD
                    # if a client wants to log in, checks if it's username and password is in the DB
                    U.execute("SELECT * FROM users WHERE username = :username", {'username': mail[1]})
                    user = U.fetchone()
                    if user is not None:
                        if bcrypt.hashpw(mail[2], SALT.encode('utf-8')) == user[1]:
                            current_socket.sendall('You can continue')
                            socket_name[current_socket] = mail[1]
                        else:
                            current_socket.sendall('You can not continue')
                    else:
                        current_socket.sendall('You can not continue')
                elif mail[0] == NEWGUEST:
                    # structure: NEWGUEST-
                    # if a client want to be a guest, than give him a random number(like guest34579)
                    # and give him a place in the DB, until he quits(now until the server goes down)
                    U.execute("SELECT * FROM users WHERE username = :username" , {'username' : mail[1]})
                    guest_num = random.randint(10000, 99999)
                    guest_name = 'guest' + str(guest_num)
                    U.execute("INSERT INTO users VALUES(?,?,?,?,?)", (guest_name, None, 0, 0, "Yes"))
                    USERS.commit()
                    socket_name[current_socket] = guest_name
                    current_socket.sendall(guest_name)
                elif mail[0] == RECORDS_GAMES:
                    # structure: RECORDS_GAMES-
                    # returns the top 10 players in the DB ordered by their game wins
                    U.execute('SELECT * FROM users WHERE is_guest = "No" ORDER BY games_wins')
                    lst = U.fetchall()
                    lst.reverse()
                    for people in range(0,10):
                        current_socket.sendall(lst[people][0] + "    "+str(lst[people][2]))
                        time.sleep(0.1)
                elif mail[0] == RECORDS_TOURNAMENTS:
                    # structure: RECORDS_TOURNAMENTS-
                    # returns the top 10 players in the DB ordered by their tournaments wins
                    U.execute('SELECT * FROM users WHERE is_guest = "No" ORDER BY tournaments_wins')
                    lst = U.fetchall()
                    lst.reverse()
                    for people in range(0, 10):
                        current_socket.sendall(lst[people][0] + "    "+str(lst[people][3]))
                        time.sleep(0.1)
                elif mail[0] == GET_STATS:
                    # structure: GET_STATS-username
                    # return the number of wins of that player in single games and in tournaments
                    U.execute("SELECT games_wins FROM users WHERE username = :username", {'username': mail[1]})
                    game_wins = U.fetchone()
                    U.execute("SELECT tournaments_wins FROM users WHERE username = :username", {'username': mail[1]})
                    tournament_wins = U.fetchone()
                    current_socket.sendall(str(game_wins[0]))
                    current_socket.sendall(str(tournament_wins[0]))
                elif mail[0] == WAIT_FOR_GAME:
                    #structure: WAIT_FOR_GAME-
                    # Adds the socket to the wait_games arr - contains the sockets of players
                    # that are waiting to play a game with a random player
                    # if another player is waiting, the two get a message that the game starts
                    # and a new thread which is manging the game between the two starts
                    wait_games.append(current_socket)
                    if len(wait_games) == 2:
                        for player in wait_games:
                            open_sockets.remove(player)
                            player.sendall("The game starts")
                        t = threading.Thread(target=managing_a_game, args =(wait_games, None))
                        t.start()
                        wait_games = []
                    else:
                        current_socket.sendall("Not yet")
                elif mail[0] == CREATE_GAME:
                    game_pin = random.randint(100, 999)
                    while games_players_with_pin[game_pin] is []: #### not sure about that
                        game_pin = random.randint(100, 999)
                    games_players_with_pin[game_pin] = []
                    games_players_with_pin[game_pin].append(current_socket)
                    current_socket.sendall(str(game_pin))
                elif mail[0] == JOIN_GAME_WITH_PIN:
                    pin = int(mail[1])
                    if len(games_players_with_pin[pin]) == 1:
                        current_socket.sendall("Joined to the game")
                        games_players_with_pin[pin].append(current_socket)
                        players_for_game = games_players_with_pin[pin]
                        for client in players_for_game:
                            client.sendall("The game starts")
                            open_sockets.remove(client)
                        t = threading.Thread(target=managing_a_game, args=(players_for_game, None))
                        t.start()
                        games_players_with_pin[pin] = []
                    else:
                        current_socket.sendall("No such game exists right now")
                elif mail[0] == DELETE_ROOM:
                    pin = current_socket.recv(1024)
                    games_players_with_pin[int(pin)].remove(current_socket)
                    current_socket.sendall(STOPWAITING)
                elif mail[0] == STOPWAITING:
                    if current_socket in wait_games:
                        wait_games.remove(current_socket)
                    current_socket.sendall(STOPWAITING)
                elif mail[0] == CHECK_TOUR_NAME:
                    if mail[1] in tournaments_names:
                        current_socket.sendall("The request is denied")
                    else:
                        current_socket.sendall("The request is confirmed")
                elif mail[0] == TRY_CREATE_TOURNAMENT:
                    # Gives a random pin number for the new tournament
                    # It's name will be what the creator of it wrote
                    # If he didn't write anything, the name will be tournament following his PIN
                    tournament_pin = random.randint(100, 999)
                    while tournaments_names[tournament_pin] is not "":
                        tournament_pin = random.randint(100, 999)
                    if mail[2] is not "":
                        tournaments_names[tournament_pin] = mail[2]
                    else:
                        tournaments_names[tournament_pin] = "tournament " + str(tournament_pin)
                    tournaments_num_of_players[tournament_pin] = int(mail[1])
                    tournaments_players[tournament_pin] = []
                    tournaments_players[tournament_pin].append(current_socket)
                    current_socket.sendall(tournaments_names[tournament_pin])
                    time.sleep(1)
                    current_socket.sendall(str(tournament_pin))
                elif mail[0] == JOIN_TOURNAMENT:
                    # checking if a tournament with the same name is live
                    # if so, checking it's state - if there is a place in it for other player
                    # if so, the new player joins, and if the max of players has reached, start it
                    pin = int(mail[1])
                    if tournaments_names[pin] is "":
                        current_socket.sendall("Incorrect PIN")
                    else:
                        if int(len(tournaments_players[pin])) == tournaments_num_of_players[pin]:
                            current_socket.sendall("This tournament is already full")
                        else:
                            tournaments_players[pin].append(current_socket)
                            current_socket.sendall("Joined to the tournament")
                            time.sleep(1)
                            current_socket.sendall(tournaments_names[pin])
                            if int(len(tournaments_players[pin])) == tournaments_num_of_players[pin]:
                                # start the tournament
                                time.sleep(0.1)
                                for player in tournaments_players[pin]:
                                    open_sockets.remove(player)
                                t = threading.Thread(target=managing_a_tournament, args=(tournaments_players[pin], tournaments_names[pin], pin))
                                t.start()
    USERS.close()
if __name__ == '__main__':
    main()