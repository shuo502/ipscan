__author__ = 'yo'
from winpcapy import WinPcap
device=b'\\Device\\NPF_{8634FFB9-ABE0-4501-B966-A60A66D55B93}'
device='\\Device\\NPF_{8634FFB9-ABE0-4501-B966-A60A66D55B93}'
s=0
ipfilters=""
def packet_callbackr(win_pcap, param, header, pkt_data):
    ip_frame = pkt_data[14:]
    src_ip = ".".join([str(b) for b in ip_frame[0xc:0x10]])
    dst_ip = ".".join([str(b) for b in ip_frame[0x10:0x14]])




    if s!=0:
        win_pcap.stop()
with WinPcap(device) as capture:
    capture.run(callback=packet_callbackr)
t_i=1