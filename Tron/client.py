from Backend.Classes.TCPCLient import TCPCLient

client = TCPCLient()
client.Connect("192.168.178.63", 9876)
client.Start()

