# -*- coding: utf-8 -*-
import socket
from Tkinter import *
import tkMessageBox
from checkers.constants import *
from checkers.game import Game
import threading
import random
import time
runningnow = True
turn = ""
game_run = True
is_tournament = False
firstgame = True
is_there_a_tournament_winner = False
sock = None
is_guest = False
guest_name = ""


def get_row_col_from_mouse(pos):
    # gets a tuple of the position of the mouse
    # returns the middle of the square which has been typed
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def connect():
    # Tries to connect to the server, and if it can , it return his socket, if not return an error message
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((CLIENT_IP,PORT_CLIENT))
        print "Connected to the server"
        return sock
    except:
        print "Can't connect to the server"
        return None


def welcome_screen():
    # The open screen
    # asks for the client to choose his login way - log in with an exciting user, sign up as a new one
    # or continue as a guest, and get a random username(guest + a random 5 digits number)
    start = Tk()
    start.title("Welcome to Checkers!")
    start.geometry("800x400+400+200")
    start['background'] = BG_COLOR
    welcome_msg = Label(start, font="Helvetica 24 bold italic",bg= TEXT_BG_COLOR, text="Welcome to the checkers game!", height=2)
    welcome_msg.pack()
    log_button = Button(start, text="log in", fg="white", bg="blue", width=10,
                        command=lambda: log_in(start))
    log_button.pack(side="left", padx=80, pady=20)
    sign_button = Button(start, text="sign up", fg="white", bg="blue", width=10,
                        command=lambda: sign_up(start))
    sign_button.pack(side="right", padx=80, pady=20)
    guest_button = Button(start, text="play as a guest", fg="white", bg="blue", width=10,
                        command=lambda: guest_login(start))
    guest_button.pack(side="right", padx=80, pady=20)
    start.mainloop()


def sign_up(start):
    # The sign up screen
    # The user can try to sign up by entering a username and a password
    socket = connect()
    if socket is None:
        tkMessageBox.showerror("Error", "Cannot connect to the server , please try again")
    else:
        start.destroy()
        sign_screen = Tk()
        sign_screen.title("Sign up")
        sign_screen.geometry("800x500+400+200")
        sign_screen['background'] = BG_COLOR
        sign_msg = Label(sign_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text="Please enter the username and password you want", height=2)
        sign_msg.pack()
        username_msg = Label(sign_screen, bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="Username (needs to be 4 to 8 characters)", height=3)
        username_msg.pack()
        username = StringVar()
        username.trace("w", lambda user, index, mode, name=username: None)
        enter_name = Entry(sign_screen, textvariable=username)
        enter_name.pack()
        password_msg = Label(sign_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text="Password (needs to be 6 to 12 characters)", height=3)
        password_msg.pack()
        password = StringVar()
        password.trace("w", lambda user, index, mode, name=password: None)
        enter_password = Entry(sign_screen, textvariable=password)
        enter_password.pack()
        log_button = Button(sign_screen, text="sign up", fg="white", bg="blue", width=10,
                            command=lambda: try_sign(enter_name.get(), enter_password.get(), socket, sign_screen))
        log_button.pack(side="left", padx=80, pady=20)
        sign_screen.mainloop()


def try_sign(username , password , socket, sign_screen):
    # The server checks if the username and password typed are on the DB
    # If not, the client continues to the main menu, else an error message pops up
    if username and password is not "":
        if username == password:
            tkMessageBox.showerror("Error", "The username and password can not be the same")
        elif len(username) > 3 and len(username) < 9 and len(password) > 5 and len(password) < 13:
            info = CHECKSIGN + "-" + username + "-" + password
            socket.sendall(info)
            reply = socket.recv(1024)
            if reply == "You can use it":
                main_menu(sign_screen, socket, username)
            else:
                tkMessageBox.showerror("Error", reply)
        else:
            tkMessageBox.showerror("Error", "Please check the amount of characters entered")
    else:
        tkMessageBox.showerror("Error", "Please enter a username and a password")


def log_in(start):
    # The log in screen
    # The user tries can try to log in with a username and a password
    socket = connect()
    if socket is None:
        tkMessageBox.showerror("Error", "Cannot connect to the server , please try again")
    else:
        start.destroy()
        login_screen = Tk()
        login_screen.title("Log in")
        login_screen.geometry("800x500+400+200")
        login_screen['background'] = BG_COLOR
        log_msg = Label(login_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text= "Please enter your username and password below", height=2)
        log_msg.pack()
        username_msg = Label(login_screen,bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="Username", height=3)
        username_msg.pack()
        username = StringVar()
        username.trace("w", lambda user, index, mode, name=username: None)
        enter_name = Entry(login_screen, textvariable=username)
        enter_name.pack()
        password_msg = Label(login_screen, bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="Password", height=3)
        password_msg.pack()
        password = StringVar()
        password.trace("w", lambda user, index, mode, name=password: None)
        enter_password = Entry(login_screen, textvariable=password)
        enter_password.pack()
        log_button = Button(login_screen, text="log in", fg="white", bg="blue", width=10,
                            command=lambda: try_log(enter_name.get(), enter_password.get(), socket, login_screen))
        log_button.pack(side="left", padx=80, pady=20)
        login_screen.mainloop()


def try_log(username, password, socket, login_screen):
    # The server checks if the username and password typed are on the DB
    # If so, the client continues to the main menu, else an error message pops up
    if username and password is not "":
        info = CHECKLOGIN + "-" + username + "-" + password
        socket.sendall(info)
        reply = socket.recv(1024)
        if reply == "You can continue":
            main_menu(login_screen, socket, username)
        elif reply == "You can not continue":
            tkMessageBox.showinfo("Error", "Your username or password are not correct")
    else:
        tkMessageBox.showinfo("Error", "Please enter your info")


def guest_login(start):
    # log in the system as a guest - it's data is deleted from the DB as he quits from the server
    # Gets a 5 digits number for it's username from the server
    global guest_name
    socket = connect()
    if socket is None:
        tkMessageBox.showinfo("Error", "Cannot connect to the server , please try again")
    else:
        socket.sendall(NEWGUEST + "-")
        username = socket.recv(1024)
        guest_name = username
        main_menu(start, socket, username)


def main_menu(start, socket, username):
    # The main screen of the game
    # Here the user can choose to go to 5 different screens:
    # The Instructions screen - in order to view the game's instructions
    # The records screen - view the top 10 players according to their wins in both tournaments and single games
    # The (single) game screen - there the user can choose how and with who he wants to play a game with
    # The tournament screen - there you can choose o create or join a tournament
    # The stats screen - shows the number of wins in single games and in tournaments of the player
    if start is not None:
        start.destroy()
    main_m = Tk()
    main_m.title("Checkers - Main Menu")
    main_m.geometry("850x425+400+200")
    main_m['background'] = BG_COLOR
    name = Label(main_m, font="Helvetica 24 bold italic", text="Checkers - Welcome " + username, bg=TEXT_BG_COLOR, height=2)
    name.pack()
    play_button = Button(main_m, text="Play a game", fg="white", bg="blue", width=15,
                        command=lambda: single_games_main_screen(main_m, socket, username))  # wait for a game
    play_button.pack(side="top", padx=80, pady=20)
    tournament_button = Button(main_m, text="Play a tournament", fg="white", bg="blue", width=15,
                        command=lambda: tournaments_main_screen(main_m, socket, username))  # join a tournament
    tournament_button.pack(side="top", padx=80, pady=20)
    records_button = Button(main_m, text="Records", fg="white", bg="blue", width=15,
                        command=lambda: records_screen(main_m, socket, username))  # go to the records screen
    stats_button = Button(main_m, text="View Stats", fg="white", bg="blue", width=15,
                        command=lambda: stats_screen(main_m, socket, username))  # go to the stats screen
    stats_button.pack(side="bottom", padx=80, pady=20)
    records_button.pack(side="bottom", padx=80, pady=20)
    instructions_button = Button(main_m, text="Instructions", fg="white", bg="blue", width=15,
                        command=lambda: instructions_screen(main_m, socket, username))  # go to the Instructions screen
    instructions_button.pack(side="bottom", padx=80, pady=20)
    main_m.mainloop()


def stats_screen(root, socket, username):
    # The personal stats screen
    # Shows the number of wins of the player in single games and tournaments
    if root is not None:
        root.destroy()
    stat_screen = Tk()
    stat_screen.title("Checkers - " + username + "'s stats")
    stat_screen.geometry("750x450+400+200")
    stat_screen['background'] = BG_COLOR
    your_stats = Label(stat_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text= username + "'s stats:", height=2)
    your_stats.pack(side = "top")
    socket.sendall(GET_STATS + "-" + username + '-')
    game_wins = socket.recv(1024)
    tournaments_wins = socket.recv(1024)
    in_games = Label(stat_screen, font="Helvetica 24 bold italic",bg=TEXT_BG_COLOR, text= "Single game wins: " + game_wins, height=2)
    in_games.pack()
    in_tournaments = Label(stat_screen, font="Helvetica 24 bold italic",bg=TEXT_BG_COLOR, text= "Tournaments wins: " + tournaments_wins, height=2)
    in_tournaments.pack()
    back_button = Button(stat_screen, text="back to the main menu", fg="white", bg="blue", width=20,
                        command=lambda: main_menu(stat_screen, socket, username))
    back_button.pack(side="left", padx=80, pady=20)
    stat_screen.mainloop()


def single_games_main_screen(root, socket, username):
    # Here the player can choose how and with who he wants to play with
    if root is not None:
        root.destroy()
    single_screen = Tk()
    single_screen.title("Checkers - single games main screen")
    single_screen.attributes("-fullscreen", True)
    single_screen['background'] = BG_COLOR
    different_ways = Label(single_screen, font="Helvetica 24 bold italic",bg=TEXT_BG_COLOR, text= "Here you can choose with who you want to play with", height=2)
    different_ways.pack(side="top")
    side_note = Label(single_screen, font="Helvetica 24 bold italic",bg=TEXT_BG_COLOR, text= "You can also create or join a room, in order to play with a friend", height=2)
    side_note.pack(side="top")
    random_player_button = Button(single_screen, text="with a random player", fg="white", bg="blue", width=20,
                        command=lambda: join_single_game_screen(single_screen, socket, username, False))
    random_player_button.pack(side="right", padx=80, pady=20)
    same_computer = Button(single_screen, text="2 players from the same computer", fg="white", bg="blue", width=25,
                        command=lambda: play_on_one_computer(single_screen, socket, username))
    same_computer.pack(side="right", padx=80, pady=20)
    create_room = Button(single_screen, text="Create a room", fg="white", bg="blue", width=25,
                        command=lambda: join_single_game_screen(single_screen, socket, username, True))
    create_room.pack(side="right", padx=80, pady=20)
    join_room = Button(single_screen, text="Join a room", fg="white", bg="blue", width=25,
                        command=lambda: join_game_with_pin(single_screen, socket, username))
    join_room.pack(side="right", padx=80, pady=20)
    back_button = Button(single_screen, text="back to the main menu", fg="white", bg="blue", width=20,
                        command=lambda: main_menu(single_screen, socket, username))
    back_button.pack(side="left", padx=80, pady=20)
    single_screen.mainloop()


def play_on_one_computer(root, socket, username):
    root.destroy()
    global firstgame
    if firstgame:
        pygame.init()
    firstgame = False
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.init()
    pygame.display.set_caption('Checkers')
    run = True
    clock = pygame.time.Clock()
    game = Game(window, WHITE)
    while run:
        clock.tick(FPS)
        if game.winner() is not None:
            print game.winner()
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        game.update()
    pygame.display.quit()
    single_games_main_screen(None, socket, username)


def join_game_with_pin(root, socket, username):
    # Join a room with a PIN number
    root.destroy()
    join_screen = Tk()
    join_screen.title("Checkers - Join a game with a pin")
    join_screen.geometry("750x450+400+200")
    join_screen['background'] = BG_COLOR
    join_msg = Label(join_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text= "Please enter the 3 digits PIN number of the game", height=2)
    join_msg.pack()
    pin_number = StringVar()
    pin_number.trace("w", lambda user, index, mode, name=pin_number: None)
    enter_number = Entry(join_screen, textvariable=pin_number)
    enter_number.pack()
    join_button = Button(join_screen, text="Join", fg="white", bg="blue", width=10,
                        command=lambda: try_join_game(join_screen, socket, username, pin_number))
    join_button.pack(side="left", padx=80, pady=20)
    back_button = Button(join_screen, text="back to the selection screen", fg="white", bg="blue", width=20,
                        command=lambda: single_games_main_screen(join_screen, socket, username))
    back_button.pack(side="right", padx=80, pady=20)
    join_screen.mainloop()
    join_screen.destroy()
    play_game(socket, username)


def try_join_game(join_screen, socket, username, pin):
    # Try to join a room with a PIN number, if a game with that PIN doesn't exists, an error message pops up.
    pin = pin.get()
    if pin is not "":
        info = JOIN_GAME_WITH_PIN + "-" + str(pin)
        socket.sendall(info)
        reply = socket.recv(1024)
        if reply == "Joined to the game":
            reply = socket.recv(1024)
            if reply == "The game starts":
                join_screen.quit()
        else:
            tkMessageBox.showinfo("Error", reply)
    else:
        tkMessageBox.showinfo("Error", "Please enter a 3 digits pin number")


def waiting_for_two_players(root, socket, username):
    # If there aren't enough players for the game, wait for other one.
    # The server will send a message if so
    global is_there_a_tournament_winner
    run = True
    while run:
        msg = socket.recv(1024)
        time.sleep(1)
        if msg == "The game starts":
            run = False
            root.quit()
        if msg == "You are the grand winner of the tournament!":
            print "you are the grand winner"
            is_there_a_tournament_winner = True
            root.quit()
            run = False
        if msg == STOPWAITING:
            run = False


def join_single_game_screen(root, socket, username, is_room):
    # At first, checks if there is already another player waiting
    # If so, automatically starts the game for both players
    # Else, wait for other player in the waiting screen
    global is_tournament
    is_tournament = False
    root.destroy()
    pin_single_game = ""
    if is_room:
        socket.sendall(CREATE_GAME + "-")
        pin_single_game = socket.recv(1024)
    if pin_single_game == "":
        msg = WAIT_FOR_GAME + '-'
        socket.sendall(msg)
        msg = socket.recv(1024)
        if msg == "The game starts":
            play_game(socket, username)
            return
    joining = Tk()
    joining.title("Checkers - Join a Game")
    joining.geometry("800x400+400+200")
    joining['background'] = BG_COLOR
    waiting = Label(joining, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text="Waiting for other player to join", height=2)
    waiting.pack()
    back_button = Button(joining, text="back to the selection screen", fg="white", bg="blue", width=20,
                         command=lambda: stop_waiting(joining, socket, username, pin_single_game))
    if pin_single_game != "":
        waiting = Label(joining, bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="Ask other players to join with this PIN " + pin_single_game, height=2)
        waiting.pack()
    back_button.pack(side="bottom", padx=80, pady=20)
    t = threading.Thread(target=waiting_for_two_players, args=(joining,socket, username))
    t.start()
    joining.mainloop()
    joining.destroy()
    play_game(socket, username)


def stop_waiting(root, socket, username, pin):
    # Sends a message to the server in order to be removed from the waiting list of a single game,
    # If the player quits a room, it means he is his creator thus, send to the server to delete the room
    if pin == "":
        msg = STOPWAITING + '-'
        socket.sendall(msg)
        single_games_main_screen(root, socket, username)
    else:
        socket.sendall(DELETE_ROOM)
        socket.sendall(pin)
        single_games_main_screen(root, socket, username)


def play_game(socket, username):
    # Starts the game
    # Each player gets its color, and if their turn is now or not
    global turn, game_run, firstgame
    game_run = True
    turn = ""
    if firstgame:
        pygame.init()
    firstgame = False
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.init()
    pygame.display.set_caption('Checkers')
    clock = pygame.time.Clock()
    msg = socket.recv(1024)
    msg = msg.split("-")
    color = msg[0]
    turn = msg[1]
    if color == "Your color is red":
        color = RED
    else:
        color = WHITE
    game = Game(window, WHITE)
    manage_a_game(socket, clock, game, color, username)


def other_player_turn(socket, game, msg):
    # Changes the board according to what the other player did in his turn
    global game_run
    if game_run:
        game.selected = game.board.get_piece(int(msg[0]), int(msg[1]))
        game.valid_moves = game.board.get_valid_moves(game.selected)
        game.move(int(msg[2]), int(msg[3]))
        game.update()


def recv_from_server(socket, game, username):
    # Keeps receiving from server during the game
    # Gets what the other player did, turns, and if a game ended and it should stop receiving
    global turn
    global game_run
    while game_run:
        time.sleep(0.1)
        if game_run:
            msg = socket.recv(1024)
        print msg
        if msg == ENDGAME:
            game_run = False
        if msg == "It's the other player's turn" or msg == "Your turn is now":
            turn = msg
        elif msg.isdigit():
            other_player_turn(socket, game, msg)


def manage_a_game(socket, clock, game, color, username):
    # Manages a single game, when it's this client turn he can move his pieces
    # If a move has been made, it is sent to the server
    # Runs until a winner detected
    global turn, game_run, is_tournament
    t = threading.Thread(target=recv_from_server, args=(socket, game, username))
    t.start()
    while game_run:
        #time.sleep(2)
        if game.winner() is not None:
            time.sleep(1)
            game_run = False
            pygame.display.quit()
            if game.winner() == RED:
                print "The winner is red!"
            else:
                print "The winner is white!"
            if game.winner() == color:
                print "I am the winner! " + username
                time.sleep(1)
                socket.sendall(username)
                if is_tournament:
                    winners_wait_for_next_game(socket, username)
                else:
                    winner_or_loser_of_game(socket, username, True)
            else:
                print "I am the loser"
                socket.sendall("Not me")
                winner_or_loser_of_game(socket, username, False)
            break
        if game_run:
            for event in pygame.event.get():
                """
                if event.type == pygame.QUIT:
                    socket.sendall(QUITFROMGAME)
                    game_run = False
                """
                if turn == "Your turn is now" and event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    has_moved = game.select(row, col)
                    if isinstance(has_moved, str):
                        socket.sendall(has_moved)
        clock.tick(FPS)
        if game_run:
            game.update()
    pygame.display.quit()


def tournaments_main_screen(main_m, socket, username):
    # decide to create or join a tournament
    main_m.destroy()
    tour_screen = Tk()
    tour_screen.title("Checkers - tournaments main screen")
    tour_screen.geometry("1000x500+400+200")
    tour_screen['background'] = BG_COLOR
    inst = Label(tour_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text= "Choose if you want to create a new tournament or to join one", height=2)
    inst.pack(side = "top")
    join_button = Button(tour_screen, text="join a tournament", fg="white", bg="blue", width=20,
                        command=lambda: join_tournament(tour_screen, socket, username))
    join_button.pack(side="right", padx=80, pady=20)
    create_button = Button(tour_screen, text="Create a tournament", fg="white", bg="blue", width=20,
                        command=lambda: create_tournament(tour_screen, socket, username))
    create_button.pack(side="right", padx=80, pady=20)
    back_button = Button(tour_screen, text="back to the main menu", fg="white", bg="blue", width=20,
                        command=lambda: main_menu(tour_screen, socket, username))
    back_button.pack(side="left", padx=80, pady=20)
    tour_screen.mainloop()


def join_tournament(tour_screen, socket, username):
    # join a tournament with a PIN number
    tour_screen.destroy()
    join_screen = Tk()
    join_screen.title("Join a tournament")
    join_screen.geometry("1000x450+400+200")
    join_screen['background'] = BG_COLOR
    join_msg = Label(join_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text= "Please enter the 3 digits PIN number of the tournament", height=2)
    join_msg.pack()
    pin_number = StringVar()
    pin_number.trace("w", lambda user, index, mode, name=pin_number: None)
    enter_number = Entry(join_screen, textvariable=pin_number)
    enter_number.pack()
    join_button = Button(join_screen, text="Join", fg="white", bg="blue", width=10,
                        command=lambda: try_join_tournament(join_screen, socket, username, pin_number))
    join_button.pack(side="left", padx=80, pady=20)
    back_button = Button(join_screen, text="back to the selection screen", fg="white", bg="blue", width=20,
                        command=lambda: tournaments_main_screen(join_screen, socket, username))
    back_button.pack(side="right", padx=80, pady=20)
    join_screen.mainloop()


def try_join_tournament(join_screen, socket, username, pin):
    # Try to join with a PIN number, if not possible, an error message pops up
    pin = pin.get()
    if pin is not "":
        info = JOIN_TOURNAMENT + "-" + str(pin)
        socket.sendall(info)
        reply = socket.recv(1024)
        print reply
        if reply == "Joined to the tournament":
            tour_name = socket.recv(1024)
            wait_for_tournament(join_screen, socket, username, tour_name, pin)
        else:
            tkMessageBox.showinfo("Error", reply)
    else:
        tkMessageBox.showinfo("Error", "Please enter a 3 digits pin number")


def create_tournament(tour_screen, socket, username):
    # Choose the number of players(4 or 8) and the name of the tournament(optional)
    tour_screen.destroy()
    create_screen = Tk()
    create_screen.title("Checkers - Create a tournament")
    create_screen.geometry("900x550+400+200")
    create_screen['background'] = BG_COLOR
    create_msg1 = Label(create_screen, bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text= "Please choose if you want to play with 4 or 8 players", height=2)
    create_msg1.pack()
    create_msg2 = Label(create_screen, bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text= "and give a name for the tournament(optional)", height=2)
    create_msg2.pack()
    number_msg = Label(create_screen, bg = TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="(4 or 8)Number of players:", height=3)
    number_msg.pack()
    players_number = StringVar()
    players_number.trace("w", lambda user, index, mode, name=players_number: None)
    enter_number = Entry(create_screen, textvariable=players_number)
    enter_number.pack()
    name_msg = Label(create_screen, bg = TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="The tournament's name(optional)", height=3)
    name_msg.pack()
    tournaments_name = StringVar()
    tournaments_name.trace("w", lambda user, index, mode, name=tournaments_name: None)
    enter_name = Entry(create_screen, textvariable=tournaments_name)
    enter_name.pack()
    create_button = Button(create_screen, text="Create", fg="white", bg="blue", width=10,
                        command=lambda: try_to_create_tournament(create_screen, socket, username, players_number, tournaments_name))
    create_button.pack(side="left", padx=80, pady=20)
    back_button = Button(create_screen, text="back to the selection screen", fg="white", bg="blue", width=20,
                        command=lambda: tournaments_main_screen(create_screen, socket, username))
    back_button.pack(side="right", padx=80, pady=20)
    create_screen.mainloop()


def try_to_create_tournament(root, socket, username, players_num, tour_name):
    # tries to create a tournament if the name of it is not one of other tournament
    num = players_num.get()
    name = tour_name.get()
    print num
    print name
    check = True
    if name is not "":
        msg = CHECK_TOUR_NAME + "-" + name
        socket.sendall(msg)
        reply = socket.recv(1024)
        if reply == "The request is denied":
            tkMessageBox.showinfo("Error", "This name is already occupied")
            check = False
    if num is not "":
        if (int(num) == 4 or int(num) == 8) and check:
            info = TRY_CREATE_TOURNAMENT + "-" + str(num) + "-" + name
            socket.sendall(info)
            name = socket.recv(1024)
            pin = socket.recv(1024)
            wait_for_tournament(root, socket, username, name, pin)
        else:
            tkMessageBox.showinfo("Error", "Please enter 4 or 8 as the number of the players")
    else:
        tkMessageBox.showinfo("Error", "Please enter 4 or 8 as the number of the players")


def wait_for_tournament(root, socket, username, name, pin):
    # Waites for the tournament to begin
    global is_tournament
    root.destroy()
    is_tournament = True
    wait_screen = Tk()
    wait_screen.title("Checkers - waiting for the tournament: " + name)
    wait_screen.geometry("800x400+400+200")
    wait_screen['background'] = BG_COLOR
    waiting = Label(wait_screen, bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="Waiting for other players to join", height=2)
    waiting.pack()
    ask_friends = Label(wait_screen, bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="Ask other players to join with this PIN " + str(pin), height=2)
    ask_friends.pack()
    back_button = Button(wait_screen, text="back to the main menu", fg="white", bg="blue", width=20,
                        command=lambda: main_menu(wait_screen, socket, username))
    back_button.pack(side="bottom", padx=80, pady=20)
    thread = threading.Thread(target=waiting_for_two_players, args=(wait_screen,socket, username))
    thread.start()
    wait_screen.mainloop()
    wait_screen.destroy()
    play_game(socket, username)


def winners_wait_for_next_game(socket, username):
    # A winner of the round of a tournament waits for other players to finish their games
    # Before starting a new match
    global is_tournament, is_there_a_tournament_winner
    is_tournament = True
    wait_screen = Tk()
    wait_screen.title("Checkers - waiting for the other players")
    wait_screen.geometry("1000x400+400+200")
    wait_screen['background'] = BG_COLOR
    congratulations = Label(wait_screen, bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="Congratulations for making it to the next round!", height=2)
    congratulations.pack()
    waiting = Label(wait_screen, bg=TEXT_BG_COLOR, font="Helvetica 24 bold italic", text="You will have to wait for all other players to finish their games ", height=2)
    waiting.pack()
    t = threading.Thread(target=waiting_for_two_players, args=(wait_screen, socket, username))
    t.start()
    wait_screen.mainloop()
    wait_screen.destroy()
    if is_there_a_tournament_winner:
        tournament_winner(socket, username)
    else:
        print "another round is starting"
        play_game(socket, username)


def tournament_winner(socket, username):
    # The winner of the tournament is announced
    global is_there_a_tournament_winner
    is_there_a_tournament_winner = False
    socket.sendall(username)
    winner_screen = Tk()
    winner_screen.title("Checkers - tournament winner")
    winner_screen.geometry("1000x400+400+200")
    winner_screen['background'] = BG_COLOR

    winner = Label(winner_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text="Congratulation! you are the winner of the tournament", height=2)
    winner.pack()
    back_button = Button(winner_screen, text="back to the main menu", fg="white", bg="blue", width=20,
                        command=lambda: main_menu(winner_screen, socket, username))
    back_button.pack(side="bottom", padx=80, pady=20)
    winner_screen.mainloop()


def winner_or_loser_of_game(socket, username, iswinner):
    # a suitable message for a single game winner or loser
    endgame_screen = Tk()
    if iswinner:
        endgame_screen.title("Checkers - the game's winner")
        endgame_screen.geometry("1000x400+400+200")
        winner = Label(endgame_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text="Congratulation " + username + "! you are the winner of the match", height=2)
        winner.pack()
    else:
        endgame_screen.title("Checkers - the game's loser")
        endgame_screen.geometry("1000x400+400+200")
        loser = Label(endgame_screen, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text="Don't worry " + username + " you will surely win the next game!", height=2)
        loser.pack()
    endgame_screen['background'] = BG_COLOR
    back_button = Button(endgame_screen, text="back to the main menu", fg="white", bg="blue", width=20,
                            command=lambda: main_menu(endgame_screen, socket, username))
    back_button.pack(side="bottom", padx=80, pady=20)
    endgame_screen.mainloop()


def instructions_screen(root, socket, username):
    # View the game's instructions
    root.destroy()
    instructions = Tk()
    instructions.title("Checkers - Instructions")
    instructions.attributes("-fullscreen", True)
    instructions['background'] = BG_COLOR

    instr = Label(instructions, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text="Instructions", height=1)
    instr.pack()
    inst = Label(instructions, font="Helvetica 18 bold italic", bg=TEXT_BG_COLOR, text="""Moves are allowed only on the dark squares, so pieces always move diagonally.
    Single pieces are always limited to forward moves (toward the opponent).
	A piece making a non-capturing move (not involving a jump) may move only one square.
	A piece making a capturing move (a jump) leaps over one of the opponent's pieces,
	landing in a straight diagonal line on the other side. Only one piece may be captured in a single jump;
	however, multiple jumps are allowed during a single turn. When a piece is captured, it is removed from the board.
	If a player is able to make a capture, there is no option; the jump must be made. If more than one capture is available,
    the player is free to choose whichever he or she prefers. When a piece reaches the furthest row from the player who controls that piece,
    it is crowned and becomes a king. One of the pieces which had been captured is placed on top of the king
    so that it is twice as high as a single piece. Kings are limited to moving diagonally but may move both forward and backward.
    (Remember that single pieces, i.e. non-kings, are always limited to forward moves.)
	Kings may combine jumps in several directions, forward and backward, on the same turn.
    Single pieces may shift direction diagonally during a multiple capture turn, but must always jump forward (toward the opponent).
""", height=20)
    inst.pack(side='left')
    back_button = Button(instructions, text="back to the main menu", fg="white", bg="blue", width=20,
                        command=lambda: main_menu(instructions, socket, username))
    back_button.pack(side="bottom", padx=80, pady=20)
    instructions.mainloop()


def records_screen(main_m, socket, username):
    # From here the player can choose to view the top 10 in single games, as well as tournaments
    main_m.destroy()
    records = Tk()
    records.title("Checkers - Records")
    records.geometry("1000x500+400+200")
    records['background'] = BG_COLOR
    in_games = Label(records, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text= "Records", height=2)
    in_games.pack(side = "top")
    games_button = Button(records, text="in single games", fg="white", bg="blue", width=20,
                        command=lambda: records_games(records, socket, username))
    games_button.pack(side="right", padx=80, pady=20)
    tournaments_button = Button(records, text="in tournaments", fg="white", bg="blue", width=20,
                        command=lambda: records_tournaments(records, socket, username))
    tournaments_button.pack(side="right", padx=80, pady=20)
    back_button = Button(records, text="back to the main menu", fg="white", bg="blue", width=20,
                        command=lambda: main_menu(records, socket, username))
    back_button.pack(side="left", padx=80, pady=20)
    records.mainloop()


def records_games(root, socket, username):
    # Top 10 players in single games, ordered by most wins
    root.destroy()
    socket.sendall(RECORDS_GAMES + "-")
    records = []
    for i in range(0,10):
        name = socket.recv(1024)
        records.append(name)
    record = Tk()
    record.title("Checkers - Single Games Records")
    record.geometry("800x700+400+200")
    record['background'] = BG_COLOR
    in_games = Label(record, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text= "Top 10 in single games", height=2)
    in_games.pack(side="top")
    for i in range(0, 10):
        recor_games = Label(record, bg=TEXT_BG_COLOR, font="Helvetica 20 bold italic", text=records[i], height=1)
        recor_games.pack()
    back_button = Button(record, text="back to the records screen", fg="white", bg="blue", width=20,
                        command=lambda: records_screen(record, socket, username))
    back_button.pack(side="bottom", padx=80, pady=20)
    record.mainloop()


def records_tournaments(root, socket, username):
    # Top 10 players in tournaments, ordered by most wins
    root.destroy()
    socket.sendall(RECORDS_TOURNAMENTS + "-")
    records = []
    for i in range(0,10):
        name = socket.recv(1024)
        records.append(name)
    record = Tk()
    record.title("Checkers - Tournaments Records")
    record.geometry("800x700+400+200")
    record['background'] = BG_COLOR
    in_games = Label(record, font="Helvetica 24 bold italic", bg=TEXT_BG_COLOR, text= "Top 10 in tournaments", height=2)
    in_games.pack(side="top")
    for i in range(0, 10):
        recor_games = Label(record, bg=TEXT_BG_COLOR, font="Helvetica 20 bold italic", text=records[i], height=1)
        recor_games.pack()
    back_button = Button(record, text="back to the records screen", fg="white", bg="blue", width=20,
                        command=lambda: records_screen(record, socket, username))
    back_button.pack(side="bottom", padx=80, pady=20)
    record.mainloop()


def main():
    # Opens up the starting screen, when the client stop running, sending
    # a message to the server, if it's a guest it will be removed from the DB
    global sock, guest_name
    welcome_screen()
    if guest_name != "":
        sock.sendall(QUIT + "-" + guest_name)
    else:
        sock.sendall(QUIT + "-")


if __name__ == '__main__':
    main()