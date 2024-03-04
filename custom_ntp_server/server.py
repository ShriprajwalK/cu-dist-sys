import socket
import struct
import time

NTPDELTA = 2208988800.0

def to_ntp_time(t):
        t += NTPDELTA
        return (int(t) << 32) + int(abs(t - int(t)) * (1<<32))

def get_ntp_response(org_ts,rcv_ts):
    leap_indicator = 0
    version_number = 4
    mode = 4
    stratum = 1
    precision = -6
    root_delay = 0
    root_dispersion = 0
    reference_identifier = 0
    reference_timestamp = to_ntp_time(time.time())
    originate_timestamp = org_ts
    receive_timestamp = rcv_ts
    poll = 0
    transmit_timestamp = to_ntp_time(time.time())
    ntp_packet = struct.pack('!1B1B1b1b3I4Q',
                             (leap_indicator << 6) | (version_number << 3) | mode,
                             stratum,
                             poll,
                             precision,
                             root_delay,
                             root_dispersion,
                             reference_identifier,
                             reference_timestamp,
                             originate_timestamp,
                             receive_timestamp,
                             transmit_timestamp
                             )

    return ntp_packet

def handle_ntp_request(data, rcv_ts):
    unpacked_request = struct.unpack("!1B1B1b1b3I4Q", data)
    client_org_ts = unpacked_request[8]
    client_rcv_ts = unpacked_request[9]
    client_xmt_ts = unpacked_request[10]

    ntp_response = get_ntp_response(client_xmt_ts, rcv_ts)

    return ntp_response


def run_ntp_server():
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(("", 82))
    print("NTP Server is listening on port 1024...")
    while True:
        try:
            print(1)
            data, client_address = UDPServerSocket.recvfrom(1024)
            rcv_ts = to_ntp_time(time.time())
            ntp_response = handle_ntp_request(data, rcv_ts)
            # ntp_response = get_ntp_response()
            print(3)
            UDPServerSocket.sendto(ntp_response, client_address)
            print("Sent NTP response to", client_address)

        except KeyboardInterrupt:
            print("NTP Server shutting down...")
            break

if __name__ == "__main__":
    run_ntp_server()