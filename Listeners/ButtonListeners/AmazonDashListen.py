#!/usr/bin/python
import socket, struct
import sys, os, subprocess
from re import search
from binascii import hexlify,unhexlify
from time import time,strftime,gmtime
import signal

class AmazonDashButtonListener():
    def __init__(self,mac_address,func,min_time_between_presses,allowed_ifs=None):
        BaseEventListener.__init__(self,func,min_time_between_presses)
        self.mac_address = mac_address
        self.rawSocket = None
        
    def _create_socket(self): 
        #Doesn't support windows
        return  socket.socket(socket.AF_PACKET, socket.SOCK_RAW,\
                              socket.htons(0x0003))

    def _recieve_packet(self):
        #Doesn't support windows
        return self.rawSocket.recvfrom(2048)
        
    def _parse_eth(self,packet):
            ethernet_header = packet[0][0:14]
            ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
            return ethernet_detailed
        
    def _is_arp(self,etherdst, ethertype):
        return ((ethertype == '\x08\x06') \
                and (etherdst == '\xff\xff\xff\xff\xff\xff'))

    def _is_valid_src(self,ethersrc):   
        idnet=hexlify(ethersrc)
        return idnet == mac_address
        
    def _is_valid_interface(self,packet):
        if (self.allowed_ifs is not None):
            recieved_interface = packet[1][0]
            if (recieved_interface not in self.allowed_ifs):
                return False
        return True
    
    def _get_click(self,packet):
        if not self._is_valid_interface(packet):
            return None
        etherdst, ethersrc, ethertype = self._parse_eth(packet)
        if self._is_arp(etherdst, ethertype):
            if self._is_valid_src(ethersrc):
                return True
        return False
    
    def _pre_listen(self):
        self.rawSocket = self._create_socket()
    
    def _event_detect(self):
        packet = self._recieve_packet()
        mac_address = self._get_click(packet)
        return (mac_address is not None)
    
    def _post_listen(self):
        self.rawSocket.shutdown()
        self.rawSocket.close()
    