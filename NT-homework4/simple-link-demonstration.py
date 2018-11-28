"""
simple-link-demonstration.py

COMSC 341DC HW4

Create count test processes

Each test process instantiates a link and then sends a message.

Peter F. Klemperer
Sept. 19, 2018
"""

import argparse
from time import time, sleep
from multiprocessing import Process
from perfectpointtopointlinks import PerfectPointToPointLinks

message_list = ["apple", "baby", "cat", "dog", "elephant", "figment", "george"]

def test_link_process(process_id, process_count, addr):
    broadcast_done_flag = False
    send_time = time() + int(process_id) + 1.0
    end_time  = time() + process_count + 2.0
    print("process {}".format(process_id))

    links = PerfectPointToPointLinks(port=process_id+10000, addr_str=addr)
    while True:
        now_seconds = time()
        if now_seconds >= send_time and broadcast_done_flag is False:
            send_mesg = message_list[process_id]
            links.send(recipient_process_port=((process_id+1)%process_count)+10000,
                                               addr_str=addr, message=send_mesg)
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