from besteffortbroadcast import BestEffortBroadcast
import multiprocessing
import random
import socket
import json


## VIRUS ##

from perfectpointtopointlinks import PerfectPointToPointLinks
import socket
import re


class VirusServer:
    def __init__(self, port, victim_port, beb_address_list):
        self.ADDRESS = "127.0.0.1"
        self.PORT = port
        self.VICTIM_PORT = victim_port
        self.chat_server_port = 11000
        # a dictionary which acts like a hash map
        # self.substitute_clients = {}
        self.victim_clients = beb_address_list
        # This server link is to deliver
        self.server_link = PerfectPointToPointLinks(port=self.PORT, addr_str=self.ADDRESS, arg_callback=self.delivery)

    def send_beb(self, msg, client_list):
        for victim in client_list:
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                temp_socket.connect((self.ADDRESS, victim))
            except socket.error:
                return
            message = str(self.PORT) + "+" + msg
            temp_socket.send(message.encode())
            temp_socket.close()

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
        return "what?"

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
                self.send_p2p(sender_port, "what?")

## VIRUS END ##


class ChatBox:
    def __init__(self, name, address, port):
        self.name = name
        self.addr = address
        self.port = port
        self.friend_list = {}
        self.queue = multiprocessing.Queue()
        self.beb = BestEffortBroadcast(process_id=int(self.port), addr_str=self.addr,
                                       callback=self.chat_deliver, arg_callback=self.queue)

    def chat_deliver(self, mesg, queue):
        if mesg is not None:
            sender_id, message = mesg
            # If it is a client update message from server, update the friend list
            if int(sender_id) == -1:
                # Remove all elements from the queue and put the new update in
                while not self.queue.empty():
                    queue.get(block=False)
                message = json.loads(message)
                # message = message.decode()
                queue.put(message)
                # Update friend list for look up
                self.friend_list = message
            # If it is a notification from server, print the notification
            elif int(sender_id) == -2:
                update = "Current people in group chat: {}".format(list(self.friend_list.values()))
                print("Server : {}".format(message))
                print("Server : {}".format(update))
            # if it is a common message from friends, print it out
            elif message:
                sender_name = self.friend_list.get(str(sender_id))
                print("{} : {}".format(sender_name, message))

    def update_friend_list(self):
        # Get the friend list from multiprocessing queue and put it back to use later
        if not self.queue.empty():
            self.friend_list = self.queue.get(block=False)
            self.queue.put(self.friend_list)

    def send(self, message):
        # Get the current friend list before sending out messages
        self.update_friend_list()
        # Get ports out of the hash map / dictionary
        process_id_list = list(self.friend_list.keys())
        process_id_list = list(map(int, process_id_list))
        self.beb.broadcast(message, process_id_list)


def main():
    name = input("Your name: ")
    addr = '127.0.0.1'
    try:
        # Choose a random port for each client
        port = random.randint(1024, 49151)
        chat_box = ChatBox(name, addr, port)

        # add instance of virus server with port random int
        virus_box = VirusServer(random.randint(1024, 49151), port, chat_box.friend_list)
        # switch up port with virus_port
        port = virus_box.PORT

        print("Chat box initiated")
    except OSError:
        if chat_box.beb:
            chat_box.beb.close()

    # Initiate a client socket to send to chat server as the beb is to send messages to friends
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connecting to chat server
        client_socket.connect(("127.0.0.1", 11000))
    except ConnectionRefusedError:
        print("Cannot connect to chat server.")
        return
    mesg = str(port) + "+" + "New client:" + name
    client_socket.send(mesg.encode())
    client_socket.close()

    # Sending messages
    print("## Type a message or {quit} to quit ##")
    while True:
        message = input("")
        # If quit, send quit message to chat server
        if message == '{quit}':
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # Connecting to chat server
                client_socket.connect(("", 11000))
            except ConnectionRefusedError:
                print("Cannot connect to chat server.")
                return
            msg = str(chat_box.port) + "+" + message
            client_socket.send(msg.encode())
            client_socket.close()
            break
        elif not message:
            continue
        # Send to friends if it a common message
        else:
            chat_box.send(message)


if __name__ == "__main__":
    main()
