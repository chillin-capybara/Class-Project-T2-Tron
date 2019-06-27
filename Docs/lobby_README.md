# Protocol Description

The lobby protocol described in the following consists of a TCP protocol, implementing a client/server communication model. The server provides several different games from which users can choose one. The lobby protocol handles listing of different games and created matches for one game, the creation of a match for a particular game and joining to an existing match.

## General

  - Each message is terminated by *null Byte* (\x00)
  - There is a limit of 1024*1024 Bytes (1 MB) per TCP message.
  - All text has to be encoded in ASCII, if not otherwise stated. Mixed encodings are allowed for custom features.
  - All text is only allowed to contain the characters A-Za-z0-9_.!
  - Lists (denoted as list<> in the protocol description) are always comma-separated and are not allowed to contain spaces.
  - Colors are always denoted as a list representing a decimal RGB code.
  
## Server Specification
 
  - The server shall support one lobby and multiple active matches.
  - One client can only be part of one match.
  - If a match in the lobby has no active players anymore, it is deleted. 

## Protocol Extensions / Modifications (*Features*)

  - The protocol can be extended or modified through *features*.
  - The available features are negotiated during the handshake between server and client.
  - All protocol details, except the handshake, can be modified by a feature.

Some (important) extra features which can be implemented are described in separate files:

  - [CHAT](features/CHAT.md)

------

## Broadcast

  * In order to get the IP and Port of the Server the Client can send a broadcast.
  * The broadcast works with UDP
  * The server listens on port 54000
  * The client sends the message to the address 255.255.255.255

| Command            | Direction        | Example        | Parameters                                           | Description                                                 |
| ------------------ | ---------------- | -------------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| **DISCOVER_LOBBY**  | Client -> Subnet | DISCOVER_LOBBY  | -                                                    | Broadcast message sent to IP 255.255.255.255 and port 54000 |
| **LOBBY** [Port]    | Server -> Client | LOBBY 54001     | Port: The port the server waits for a TCP connection | Response to the Client                                      |
 
## Control Protocol (TCP)

  * The default control protocol port is on server side 54001.

### Connection Initiation / Handshake

![Connection Initiation](diagrams/01_handshake.png "Handshake")

| Command                                                      | Direction         | Example                               | Parameters                                                                                                                                                | Description                         |
| ------------------------------------------------------------ | ----------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------ |
| **HELLO** [NAME] [list\<CLIENT_FEATURES\>]                   | Client -> Server  | HELLO IKPLAYER BASIC                  | NAME: The name of the player to register. <br> CLIENT_FEATURES: Comma-separated list of lobby features supported by the client.                           | Client handshake                    |
| **WELCOME** [list\<SERVER_FEATURES\>]                        | Server -> Client  | WELCOME BASIC oder WELCOME BASIC,DIMS,10,10,50,50                         | SERVER_FEATURES: Lobby features supported by the server.                                                                                                  | Server response to client handshake |

The width and height of one cell on the game board and the number of cells in x and y direction are transmitted during handshake in the following format: 

  * *DIMS*: list<[CELL_WIDTH],[CELL_HEIGHT],[NUM_FIELDS_X],[NUM_FIELDS_Y]>

*DIMS* is a server feature and thus send as part of the *WELCOME* message.
Where all dimensions are in pixel and the origin is the upper left corner with all positive coordinates

### Create / Join a match (Lobby)

![Create and join a match](diagrams/02_lobby.png "Create and join a match")

| Command                                        | Direction        | Example                                   | Parameters                                                                                                                                              | Description                                                                                                                                                                               |
| ---------------------------------------------- | ---------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LIST_GAMES**                                 | Client -> Server | LIST_GAMES                                | -                                                                                                                                                       | Request a list of available games.
| **AVAILABLE_GAMES** [list\<GAME_NAMES\>        | Server -> Client | AVAILABLE_GAMES Tron,Pong                 | GAME_NAMES: List of game names.                                                                                                                         | Returns a list of available games.
| **CREATE_MATCH** [GAME] [NAME] [list\<GAME_FEATURES\>] | Client -> Server | CREATE_MATCH Tron Testmatch Players,4,lifes,3   | GAME: The name of the game for which a match should be created <br> NAME: The name of the match to create.<br>GAME_FEATURES: A list of the features of a GAME.     | Create a new match for a specific game in the lobby for others to join. The player who created the match is not automatically participating. The client has to send a separate JOIN_MATCH message.                                                                                                                                       |
| **MATCH_CREATED**                  | Server- > Client | MATCH_CREATED                             |                                                                                                                        | Confirm that the game was created. If not, a **ERR_FAILED_TO_CREATE** is thrown. The client who created the match is **not** automatically joined to the match.                                   |
| **LIST_MATCHES** [GAME]                        | Client -> Server | LIST_MATCHES Pong                         | GAME: Name of a specific game available on the server.                                                                                                  | Request a list of all (open) matches of a specific game in the lobby. This does not include already started matches. The server answers with the **GAMES** message.                                             |
| **GAMES** [GAME] [list\<MATCHES\>]             | Server -> Client | GAMES Pong game1,game2,game3              | GAME: Name of a specific game <br> MATCHES: A list of active matches.                                                                                   | List of all join-able matches in the lobby.                                                                                                                                               |
| **MATCH_FEATURES** [NAME]                       | Client -> Server | MATCH_FEATURES game1                       | NAME: The name of a specific match                                                                                                                    | Request to get a list of features of a specific match. The server answers with the **MATCH** command. If the game does not exist the server answers with the **ERR_MATCH_NOT_EXIST** message |
| **MATCH** [GAME] [NAME] [list\<MATCH_FEATURES\>]        | Server -> Client | GAME Tron game1 Players,4,lifes,3| GAME: Name of a specific game. <br>NAME: The name of the match<br>MATCH_FEATURES: A list of the features of a MATCH.                                    | List of the features of a game.                                                                                                                                                           |
| **JOIN_MATCH** [NAME] [COLOR]                   | Client -> Server | JOIN_MATCH game1 117,112,179               | NAME: Name of the match to join.<br> COLOR: Color of the player as decimal RGB triple (color of Tron avatar, color of paddle in pong)                 | Join a specific match. If this fails, a **ERR_FAILED_TO_JOIN** is thrown.                                                                                                                 |
| **MATCH_JOINED** [PLAYER_ID]                    | Server -> Client | MATCH_JOINED 2                             | PLAYER_ID: Numeric ID of player, only valide for the duration of this match                                                                             | Server confirmed that the client joined the match.                                                                                                                                        |
| **MATCH_STARTED** [PORT] list<[PLAYER] [COLOR]> | Server -> Client | MATCH_STARTED 45000 1 117,112,179,2 27,158,119 | PORT: The UDP port of the match.<br>PLAYER: The (numeric) id of the player starting at 1. <br>COLOR: The color triple of a player.<br> PLAYER and COLOR are given for each player in the game                                                             | The match is now started at UDP port PORT.                                                                                                                       |
| **GAME_ENDED** [REASON]                        | Server -> Client | GAME_ENDED You won!                       | REASON: A reason for match ending.                                                                                                                      | Server signals client that his match ended.                                                                                                                                               |

### Error Messages

All errors, except CMD_NOT_UNDERSTOOD, *have to* be followed by a reason.
The message (reason) is allowed to contain whitespaces.

| Command                           | Direction        | Example                                     | Parameters                                  | Description                                                                               |
| --------------------------------- | ---------------- | ------------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **ERR_CMD_NOT_UNDERSTOOD**        | Server -> Client | ERR_CMD_NOT_UNDERSTOOD                      | -                                           | The server signals the client that it did not understand the command and ignored it.      |
| **ERR_FAILED_TO_CREATE** [REASON] | Server -> Client | ERR_FAILED_TO_CREATE Name already taken <br> ERR_FAILED_TO_CREATE Color already taken     | -                          | The server signals the client that it failed to create the match in the lobby.            |
| **ERR_FAILED_TO_JOIN** [REASON]   | Server -> Client | ERR_FAILED_TO_JOIN Match does not exist     | -                                           | The server signals the client that it was not able to join the client to the match.       |
| **ERR_GAME_NOT_EXIST** [NAME]     | Server -> Client | ERR_GAME_NOT_EXIST Testmatch                | Name: The name of the game                  | The server signals the client that the game does not exist.                               |
| **DISCONNECTING_YOU** [REASON]    | Server -> Client | DISCONNECTING_YOU You are banned            | -                                           | The server can always choose to disconnect a client forcefully.                           |
| **LEAVING_MATCH** [REASON]        | Client -> Server | LEAVING_MATCH I do not want to play anymore | -                                           | The client can always choose to leave a match in the lobby or an active match.            |
 

