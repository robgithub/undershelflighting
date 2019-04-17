import sys, socket

def listen():
  try:
    s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
  except socket.error, err:
    print err
    print "run with sudo"
    sys.exit(2)
  s.settimeout(10)
  try:
    data, addr = s.recvfrom(1508)
    print "Packet from %r: %r" % (addr,data)
  except socket.timeout:
    print "timeout"


listen()
