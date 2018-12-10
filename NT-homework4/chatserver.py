from perfectpointtopointlinks import PerfectPointToPointLinks
import json
import socket

# This is the chat server which keeps track of the people in the chat application


class ChatServer:
    def __init__(self):
        self.ADDRESS = "127.0.0.1"
        self.PORT = 11000
        # a dictionary which acts like a hash map
        self.clients = {}
        self.just_delivered = False
        # This server link is to deliver
        self.server_link = PerfectPointToPointLinks(port=self.PORT, addr_str=self.ADDRESS, arg_callback=self.delivery)

    # Send message to every one in the client list
    # Create a new client and send without using the p2p send method so that one can fake port
    # to mark if it is a client list update or notification
    def send(self, message):
        for port in self.clients.keys():
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect((self.ADDRESS, int(port)))
            except ConnectionRefusedError:
                print("Cannot connect to {}.".format(self.clients.get(port)))
                continue
            client_socket.send(message.encode())
            client_socket.close()

    # Send the current client list to everyone
    def send_address_list(self):
        message = json.dumps(self.clients)
        mesg = "-1" + "+" + message
        self.send(mesg)

    def delivery(self, sender_port, message):
        # Update client list when someone joins/quits
        # First send is to update the client list
        # Second send is to notify who just joins/quits
        if message.startswith("New client:"):
            name = message.split(':')[-1]
            self.clients.update({int(sender_port): name})
            self.send_address_list()
            message = "-2" + "+" + "{} just joined the conversation.".format(name)
            self.send(message)
        elif message == "{quit}":
            name = self.clients.get(int(sender_port))
            message = "-2" + "+" + "{} just left the conversation.".format(name)
            self.clients.pop(int(sender_port), None)
            self.send_address_list()
            self.send(message)
        else:
            return
        print(self.clients)


def main():
    chat_server = ChatServer()


if __name__ == "__main__":
    main()
