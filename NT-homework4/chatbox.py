from besteffortbroadcast import BestEffortBroadcast
from time import sleep



def main():
    address = ''
    addr = ''
    port = ''
    while True:
        try:
            address = input("enter this ip:port (ex:127.0.0.1:10000) -> ")
            addr = address.split(":")[0]
            port = address.split(":")[1]
            port = int(port)
            break
        except IndexError or ValueError:
            print("Wrong input")
            continue


    address_list = []
    address_list.append(int(port))

    friend_addr = ''
    while True:
        try:
            friend_addr = input("enter friend's ports e.g. 10000, 10001, 10002 -> ")
            for address in friend_addr.split(","):
                if int(address) not in address_list:
                    address_list.append(int(address))
            break
        except IndexError:
            print("Wrong input")
            continue



    print(address_list)

    beb = BestEffortBroadcast(process_id=int(port), process_id_list=address_list, addr_str=addr)

    while True:
        while True:
            mesg = beb.deliver()
            if mesg is not None:
                sender_id, message = mesg
                if message:
                    print("Delivery from {} : {}".format(sender_id, message))
            else:
                break

        message = input("type a message, q(quit) or enter (continue) -> ")
        if message is 'q':
            break
        if not message:
            continue
        sleep(0.1)
        beb.broadcast(message)


if __name__ == "__main__":
    main()
