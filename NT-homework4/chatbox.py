from besteffortbroadcast import BestEffortBroadcast
import multiprocessing
import random
import socket
import json


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
    name = raw_input("Your name: ")
    addr = '127.0.0.1'
    try:
        # Choose a random port for each client
        port = random.randint(1024, 49151)
        chat_box = ChatBox(name, addr, port)
        print("Chat box initiated")
    except OSError:
        if chat_box.beb:
            chat_box.beb.close()

    # Initiate a client socket to send to chat server as the beb is to send messages to friends
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connecting to chat server
        client_socket.connect(("127.0.0.1", 11000))
    except socket.error:
        print("Cannot connect to chat server.")
        return
    mesg = str(port) + "+" + "New client:" + name
    client_socket.send(mesg.encode())
    client_socket.close()

    # Sending messages
    print("## Type a message or {quit} to quit ##")
    while True:
        message = raw_input("")
        # If quit, send quit message to chat server
        if message == '{quit}':
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # Connecting to chat server
                client_socket.connect(("", 11000))
            except socket.error:
                print("Cannot connect to chat server.")
                continue
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
