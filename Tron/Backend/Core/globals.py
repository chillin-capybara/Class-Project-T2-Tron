# Global configuration of BACKEND classes

LOBBY_DISCOVERY_PORT = 54000
LOBBY_DISCOVERY_ADDR = "255.255.255.255"
#LOBBY_PORT_RANGE = range(54010, 54100 + 1)
LOBBY_PORT_RANGE = range(54010, 54200 + 1)
#LOBBY_PORT_RANGE = range(0, 65000)
LOBBY_DISCOVERY_RECV_SIZE = 1024
LOBBY_DISCOVER_TIMEOUT = 1 # Wait for broadcast responses only 2 seconds
DEFAULT_CONTROL_PROTOCOL_PORT = 54001

CONTROL_PROTOCOL_RECV_SIZE = 1024
CLIENT_FEATURES = ['BASIC', 'JSONCOMM'] # LIST of the client features
# Feature DIMS,10,10,50,50 is obligatory
SERVER_FEATURES = ['BASIC', 'DIMS', 10,10,50,50, 'JSONCOMM'] # List of server features

SERVER_GAMES = ['Tron']

UDP_RECV_BUFFER_SIZE = 1024

MAX_MATRIX_SIZE = (20,20)

MATCH_IDLE_TIMEOUT = 10 # How many seconds to wait, until a match is closed

# Default feature string to initialize match objects at the client side
MATCH_DEFAULT_FEATURES = ['BASIC', 'Players', 1, 'lifes', 1]

CLIENT = None
