#!/usr/bin/python
"""Listen for Amazon Dash Button press."""

import socket
import struct
import binascii
from Listeners.BaseListener import BaseEventListener

def _parse_eth(packet):
    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
    return ethernet_detailed

def _is_arp(etherdst, ethertype):
    return (ethertype == '\x08\x06') and (etherdst == '\xff\xff\xff\xff\xff\xff')

class AmazonDashButtonListener(BaseEventListener):
    """Listen for Amazon Dash Buttons."""
    def __init__(self, mac_address, func, min_time_between_presses, allowed_ifs=None):
        self.allowed_ifs = allowed_ifs
        BaseEventListener.__init__(self, func, min_time_between_presses)
        self.mac_address = mac_address
        self.raw_socket = None

    def _recieve_packet(self):
        #Doesn't support windows
        return self.raw_socket.recvfrom(2048)

    def _is_valid_interface(self, packet):
        if self.allowed_ifs is not None:
            recieved_interface = packet[1][0]
            if recieved_interface not in self.allowed_ifs:
                return False
        return True

    def _is_valid_src(self, ethersrc):
        idnet = binascii.hexlify(ethersrc)
        return idnet == self.mac_address

    def _get_click(self, packet):
        if not self._is_valid_interface(packet):
            return None
        etherdst, ethersrc, ethertype = _parse_eth(packet)
        if _is_arp(etherdst, ethertype):
            if self._is_valid_src(ethersrc):
                return True
        return False

    def _pre_listen(self):
        #Doesn't support windows
        self.raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

    def _event_detect(self):
        packet = self._recieve_packet()
        mac_address = self._get_click(packet)
        return mac_address is not None

    def _post_listen(self):
        self.raw_socket.shutdown()
        self.raw_socket.close()
