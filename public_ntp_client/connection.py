from socket import AF_INET, SOCK_DGRAM
import socket
import struct, time

NTPDELTA = 2208988800.0
buf = 1024


def to_ntp_time(t):
    t += NTPDELTA
    return (int(t) << 32) + int(abs(t - int(t)) * (1 << 32))


def create_request_packet(org_ts, rcv_ts, xmt_ts):
    packet = struct.pack('!B', 0x1b) + 23 * b'\0' + struct.pack('!Q', int(org_ts)) + struct.pack('!Q',
                                                                                                 int(rcv_ts)) + struct.pack(
        '!Q', int(xmt_ts))
    return packet


def calc_delay(t1, t2, t3, t4):
    delay = (t4 - t1) - (t3 - t2)
    return delay


def calc_offset(t1, t2, t3, t4):
    offset = ((t2 - t1) + (t3 - t4)) / 2
    return offset


def ge_min_delay(delays):
    return delays.index(min(delays))


class Connection:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def sendRequest(self, org_ts, rcv_ts):
        xmt_ts = to_ntp_time(time.time())
        a = self.send(org_ts, rcv_ts, xmt_ts)
        ## timeout / message loss
        while a[2] == -1:
            print('Retrying:::')
            xmt_ts = to_ntp_time(time.time())
            a = self.send(org_ts, rcv_ts, xmt_ts) # to_ntp_time(time.time())
        return a

    def send(self, org_ts, rcv_ts, xmt_ts):

        ntp_packet = create_request_packet(org_ts, rcv_ts, xmt_ts)

        address = (self.host, self.port)

        client = socket.socket(AF_INET, SOCK_DGRAM)
        client.settimeout(1)
        client.sendto(ntp_packet, address)
        try:
            msg, address = client.recvfrom(buf)
        except Exception as e:
            print(e)
            return (-1, -1, -1, -1)

        t4 = to_ntp_time(time.time())

        unpacked_response = struct.unpack("!1B1B1b1b3I4Q", msg)

        # leap_indicator = (unpacked_response[0] & 0xC0) >> 0x06
        # version = (unpacked_response[0] & 0x38) >> 0x03
        # mode = unpacked_response[0] & 0x07
        # stratum = unpacked_response[1]
        # poll = unpacked_response[2]
        # precision = unpacked_response[3]
        # root_delay = unpacked_response[4]
        # root_dispersion = unpacked_response[5]
        # root_identifier = unpacked_response[6]
        # reference_timestamp = unpacked_response[7]
        originate_timestamp = unpacked_response[8]
        receive_timestamp = unpacked_response[9]
        transmit_timestamp = unpacked_response[10]
        # print(unpacked_response)

        ## delayesd duplicate
        if(originate_timestamp < xmt_ts):
            return (-1,-1,-1,-1)

        # print(struct.unpack("!12I", msg))
        # t1 = time.ctime(struct.unpack( "!12I", msg )[6] - NTPDELTA).replace("  "," ") ### origniate
        # t2 = time.ctime(struct.unpack( "!12I", msg )[8] - NTPDELTA).replace("  "," ") ### receive
        # t3 = time.ctime(struct.unpack( "!12I", msg )[10] - NTPDELTA).replace("  "," ") ### transmit
        # t4 = time.ctime(t4).replace("  "," ")

        # t1 = struct.unpack( "!12I", msg )[6] - NTPDELTA
        # t2 = struct.unpack( "!12I", msg )[8] - NTPDELTA
        # t3 = struct.unpack( "!12I", msg )[10] - NTPDELTA
        # t4 = t4

        t1 = originate_timestamp
        t2 = receive_timestamp
        t3 = transmit_timestamp
        t4 = t4

        delay = calc_delay(t1, t2, t3, t4)
        offset = calc_offset(t1, t2, t3, t4)
        return delay, offset, originate_timestamp, receive_timestamp


if __name__ == "__main__":

    packet_bursts = 8
    originate_timestamp = 0
    receive_timestamp = 0
    connection = Connection("127.0.0.1", 82)
    # connection = Connection("pool.ntp.org", 123)
    # connection = Connection("35.192.154.114", 1234)

    delay_list = []
    offset_list = []
    for burst in range(packet_bursts):
        delay, offset, new_originate_timestamp, new_receive_timestamp = connection.sendRequest(
            originate_timestamp, receive_timestamp
        )
        delay_list.append(delay)
        offset_list.append(offset)
        originate_timestamp = new_originate_timestamp
        receive_timestamp = new_receive_timestamp

    print(delay_list)
    print(offset_list)