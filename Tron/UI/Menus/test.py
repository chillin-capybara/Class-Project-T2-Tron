from collections import namedtuple		
        
Lobby = namedtuple('Lobby', ['host', 'port'])
lobby1 = Lobby("192.168.1.1", 20)
lobby2 = Lobby("10.0.0.1", 9984)
lobbieslist = [lobby1, lobby2]
print(lobby1.host)
print(lobby2.port)
print(lobbieslist[1].host)