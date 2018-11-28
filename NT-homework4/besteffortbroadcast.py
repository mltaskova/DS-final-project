# from perfectpointtopointlinks import PerfectPointToPointLinks
#
#
# class BestEffortBroadcast:
#
#     def __init__(self, process_id, process_id_list, addr_str):
#         self.address = addr_str
#         self.links = PerfectPointToPointLinks(port=process_id, addr_str=addr_str)
#         self.process_id_list = process_id_list
#
#     def broadcast(self, message):
#         for process_id in self.process_id_list:
#             port = process_id[1]
#             addr = process_id[0]
#             self.links.send(port, addr, message)
#
#     def close(self):
#         self.links.close()
#
#     def deliver(self):
#         while True:
#             sender_id, message = self.links.deliver()
#             if message is not None:
#                 return (sender_id, message)
from perfectpointtopointlinks import PerfectPointToPointLinks


class BestEffortBroadcast:

    def __init__(self, process_id, process_id_list, addr_str):
        self.address = addr_str
        self.links = PerfectPointToPointLinks(port=process_id, addr_str=addr_str)
        self.process_id_list = process_id_list

    def broadcast(self, message):
        for process_id in self.process_id_list:
            self.links.send(process_id, self.address, message)

    def close(self):
        self.links.close()

    def deliver(self):
        while True:
            try:
                sender_id, message = self.links.deliver()
            except TypeError:
                return
            if message is not None:
                return (self.address+str(sender_id), message)