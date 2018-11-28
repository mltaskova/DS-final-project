import socket

class PerfectPointToPointLinks:
    def __init__(self, port, addr_str):
        self.port = port
        self.address = addr_str
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.address, int(self.port)))
        self.server_socket.listen(4)
        self.deliver_list = []

    def send(self, recipient_process_port, addr_str, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((addr_str, recipient_process_port))
        except ConnectionRefusedError:
            print("Friend {} has not joined.".format(recipient_process_port))
            return
        mesg = str(self.port) + "+" + message
        client_socket.send(mesg.encode())
        client_socket.close()

    def deliver(self):
        while True:
            try:
                self.server_socket.setblocking(0)
            except BlockingIOError:
                self.server_socket.close()
                return
            try:
                (connection, address) = self.server_socket.accept()
            except BlockingIOError:
                return
            connection.setblocking(0)
            buf = connection.recv(2048)
            message = None
            if buf:
                message = buf.decode()
                recipient_port = message.split("+")[0]
                message = message.split("+")[1]
            connection.close()
            return (recipient_port, message)


    def close(self):
        self.server_socket.close()