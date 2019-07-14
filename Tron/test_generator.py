packet = bytes("asdasd\x00jsdkasdlj\x00","UTF-8")
parts = packet.split(b'\x00')
print(parts)