"""
simple-beb-demonstration.py

COMSC 341DC HW4

Peter F. Klemperer
October 10, 2018
"""

import argparse
from time import time, sleep
from multiprocessing import Process
from besteffortbroadcast import BestEffortBroadcast

message_list = ["apple", "baby", "cat", "dog", "elephant", "figment", "george"]

def test_beb_process(process_id, process_list, addr):
    broadcast_done_flag = False
    send_time = time() + int(process_id%10000) + 1.0
    process_count = len(process_list)
    end_time = time() + process_count + 2.0
    print("process {}".format(process_id))

    beb = BestEffortBroadcast(process_id=process_id, process_id_list=process_list, addr_str=addr)

    while True:
        now_seconds = time()
        if now_seconds >= send_time and broadcast_done_flag is False:
            send_mesg = message_list[process_id%10000]
            beb.broadcast(message=send_mesg)
            broadcast_done_flag = True
        elif now_seconds >= end_time:
            beb.close()
            return

        sleep(0.1)
        mesg = beb.deliver()
        if mesg is not None:
            sender_id, message = mesg
            print("P{} : delivery from {} : {}".format(process_id, sender_id, message))

"""
Main:

Start count processes, each with a BestEffortBroadcast
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
    process_id_list = []
    for x in range(args.count):
        process_id_list.append(x+10000)

    # create list of test processes
    for process_num in process_id_list:
        p = Process(target=test_beb_process, args=(process_num, process_id_list, "127.0.0.1"))
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