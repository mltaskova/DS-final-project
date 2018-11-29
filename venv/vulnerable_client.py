##Taskova

import socket
import pickle
import argparse
import select
from time import time, sleep
from multiprocessing import Process


class PerfectPointToPointLinks:
    def __init__(self, port, addr_str):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((addr_str, port))
        self.set_timeout(5)
        # self.server.setblocking(0)
        self.server.listen(5)

    def set_timeout(self, limit):
        self.server.settimeout(limit)

    def send(self, recipient_process_port, addr_str, message):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((addr_str, recipient_process_port))
        client.send(pickle.dumps(message))
        client.close()

    def close(self):
        self.server.close()

    def deliver(self):
        try:
            (c, address) = self.server.accept()
            data = c.recv(4096)
            message = pickle.loads(data)
            return address, message
        except socket.timeout:
            return None

"""
simple-link-demonstration.py

COMSC 341DC HW4

Create count test processes
t
Each test process instantiates a link and then sends a message.

Peter F. Klemperer
Sept. 19, 2018
"""

message_list = ["apple", "baby", "cat", "dog", "elephant", "figment", "george"]


def test_link_process(process_id, process_count, addr):
    broadcast_done_flag = False
    send_time = time() + int(process_id) + 1.0
    end_time = time() + process_count + 2.0
    print("process {}".format(process_id))

    links = PerfectPointToPointLinks(port=process_id+10000, addr_str=addr)

    links.send(0, '', (process_id+10000, addr))
    ### virus line ends here here ###
    while True:
        now_seconds = time()
        if now_seconds >= send_time and broadcast_done_flag is False:
            send_mesg = message_list[process_id]
            links.send(recipient_process_port=((process_id + 1) % process_count) + 10000,
                       addr_str=addr,
                       message=send_mesg)
            broadcast_done_flag = True
        elif now_seconds >= end_time:
            links.close()
            return

        sleep(0.1)
        mesg = links.deliver()
        if mesg is not None:
            sender_id, message = mesg
            print("P{} : delivery from {} : {}".format(process_id, sender_id, message))

"""
Main:

Start count processes, each with a PerfectPointToPointLinks
"""

def main():
    """ parse the ip and port to connect to """
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=4,
                        help='number of processes to spawn')
    args = parser.parse_args()

    # set up the test
    # generate a list of length process_count
    process_list = []

    # create list of test processes
    for process_num in range(args.count):
        p = Process(target=test_link_process, args=(process_num, args.count, "127.0.0.1"))
        process_list.append(p)

    # start all processes in the list
    for process in process_list:
        process.start()

    # collect them after they finish
    for process in process_list:
        process.join()

    # all done
    print("Goodbye.")

if __name__ == "__main__":
    main()


