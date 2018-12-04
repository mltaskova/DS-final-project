from perfectpointtopointlinks import PerfectPointToPointLinks


class BestEffortBroadcast:

    def __init__(self, process_id, process_id_list, addr_str, arg_callback):
        self.address = addr_str
        self.deliver_call_back = arg_callback
        self.links = PerfectPointToPointLinks(port=process_id, addr_str=addr_str, arg_callback = self.deliver)
        self.process_id_list = process_id_list

    def broadcast(self, message):
        for process_id in self.process_id_list:
            self.links.send(process_id, self.address, message)

    def close(self):
        self.links.close()

    def deliver(self, sender_id, message):
        if message is not None:
            self.deliver_call_back((self.address+str(sender_id), message))
