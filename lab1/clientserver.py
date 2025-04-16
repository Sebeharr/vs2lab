"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long
telephoneBook = {
    "Lili":"0123 456789",
    "Lara":"1234 567890",
    "Kyra":"2345 678901",
    "Sebbe":"3456 789012"
}

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped
                    # connection.send(data + "*".encode('ascii'))  # return sent data plus an "*"
                    connection.send((Server.requestHandler(self, data)).encode('ascii')) # !!NEU!! ruft die methode auf die aus der data die entsprechenden aufrufe auf das telefonbich macht
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")
    

    #neue methode die auf das telefonbuch zugreift, jenachdem wie die decoded data aussieht

    def requestHandler(self, data):
        decodedData = data.decode('ascii')
        if decodedData.startswith("GET "):
            name = decodedData[4:]
            if name in telephoneBook:
                return name + ": " + telephoneBook[name]
            else:
                return "Name not in telephonebook"
        elif decodedData.startswith("GETALL"):
            allEntries = ""
            for names, number in telephoneBook.items():
                allEntries = allEntries + names + ": " + number + "\n"
            return allEntries
        else:
            return "Command not found"
            


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in):
        """ Call server """
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def close(self):
        """ Close socket """
        self.sock.close()