import pygame

# Stores all the important constants
# For the game:
FPS = 60
WIDTH,HEIGHT = 800,800
ROWS,COLS = 8,8
SQUARE_SIZE = WIDTH//COLS

#RGB colors
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREY = (128,128,128)
# load the crown image
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))


BG_COLOR = "#50ACC5"
TEXT_BG_COLOR = "#6CA8D5"
SALT = '$2a$12$22m1hiKtFqLNEFH5TjnvuO'
SERVER_IP = "0.0.0.0" # 0.0.0.0
CLIENT_IP = "127.0.0.1" #0.tcp.ngrok.io 127.0.0.1
PORT_SERVER = 15201
PORT_CLIENT = 15201  #14156
# Types of messages that can be send by the client to the server
QUIT = 'Quit'
QUITFROMGAME = 'Quitfromgame'
CHECKSIGN = 'checksign'
CHECKLOGIN = 'checklogin'
NEWGUEST = 'newguest'
RECORDS_GAMES = "recordsgames"
RECORDS_TOURNAMENTS = 'recordstour'
WAIT_FOR_GAME = 'gamewait'
WAIT_FOR_TOURNAMENTS = 'tournamentwait'
CREATE_TOURNAMENT = 'createtournament'
STOPWAITING = "stopwaiting"
CHECK_IF_STARTED = 'checkifstarted'
ENDGAME = 'endgame'
TRY_CREATE_TOURNAMENT = 'trycreatetournament'
JOIN_TOURNAMENT = 'jointournament'
CHECK_TOUR_NAME = 'checktourname'
CREATE_GAME = 'creategame'
JOIN_GAME_WITH_PIN = 'joinagamewithpin'
DELETE_ROOM = 'deleteroom'
GET_STATS = 'getstats'