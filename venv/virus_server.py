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
