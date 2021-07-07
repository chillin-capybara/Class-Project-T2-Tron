# Server Admin Communication specifiations



## List

```bash
list
ls
```

- Call EList(self)

## cd

```bash
cd %s
cd lobby1
cd match1
```

- Call ECd(self, param=%s)

## end

```bash
end %s
end

end match1
end
```

- Call EEnd(self, param=%s)

## kick

```bash
kick %s

kick player1
```

- Call EKick(self, param=%s)

## ban

```bash
ban %s

ban player1
```

- Call EBan(self, param=%s)

## blacklist

```bash
blacklist %s

blacklist 192.168.1.121
```

- Call EBlacklist(self, param=%s)



## whiltelist

```bash
whitelist %s

whitelist 192.168.1.121
```

- Call EWhitelist(self, param=%s)

## help

```bash
help
```

- Call EHelp(self)

## create

```bash
create %s %s %s

create Tron match1 Players,1,lifes,3
```

- Call ECreate(self, game=%s, name=%s, features=%s)



## show

```bash
show %s
show

show lobby1
show match1
```



- Call EShow(self, params=%s)



# ALLES GENAU SO WIE BEI BASICCOMM

```python
def on_show(sender, params):
  print("Showing: %s " % params)

COMM = BasicComm()
COMM.EShow += on_show

packet = COMM.show('lobby') # show lobby -> UTF8 ENCODED MESSAGE \x00
COMM.process(packet) # Has to call the events
```

