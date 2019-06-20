from Backend.Classes.TCPCLient import TCPCLient

client = TCPCLient()
client.Connect("127.0.0.1", 9877)
client.Start()


