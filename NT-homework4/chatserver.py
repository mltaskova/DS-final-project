## VIRUS ##

from perfectpointtopointlinks import PerfectPointToPointLinks
import socket
import re
import json


class VirusServer:
    def __init__(self, port, victim_port, beb_address_list):
        self.ADDRESS = "127.0.0.1"
        self.PORT = port
        self.VICTIM_PORT = victim_port
        self.chat_server_port = 11000
        # a dictionary which acts like a hash map
        self.victim_clients = beb_address_list
        self.question_words_list = ["where", "how", "why"]
        # This server link is to deliver
        self.server_link = PerfectPointToPointLinks(port=self.PORT, addr_str=self.ADDRESS, arg_callback=self.delivery)

    def send_p2p(self, sender_port,  msg):
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            temp_socket.connect((self.ADDRESS, self.VICTIM_PORT))
        except socket.error:
            return
        message = str(sender_port) + "+" + msg
        temp_socket.send(message.encode())
        temp_socket.close()

    def manipulate_msg(self, msg):
        for qw in self.question_words_list:
            if msg.__contains__(qw):
                return qw + " is it still a fact that children get killed in schools due to openly available automated rifles"
        if msg.__contains__("hey"):
            return "hey when was the last time you researched immigration policies in America"
        elif msg.__contains__("do"):
            return "do you want to join me in the fight against sexism"
        else:
            return msg + ", and btw black lives matter"

    def delivery(self, sender_port,  message):
        if message is not None:
            if sender_port == self.VICTIM_PORT or sender_port == self.PORT:
                self.send_p2p(self.PORT , message)
            elif sender_port == -1:
                msg = json.loads(message)
                self.victim_clients = msg
                self.send_p2p(sender_port, message)
            elif sender_port == -2 or sender_port == self.chat_server_port:
                self.send_p2p(sender_port, message)
            else:
                msg = self.manipulate_msg(message)
                self.send_p2p(sender_port, msg)

## VIRUS END ##
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
            except socket.error:
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
