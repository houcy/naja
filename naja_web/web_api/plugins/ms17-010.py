from ctypes import *
import sys
import socket
import re
import struct

# ^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$
# re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

'''
https://support.microsoft.com/zh-cn/help/204279/direct-hosting-of-smb-over-tcp-ip
http://blog.csdn.net/w83761456/article/details/21171085
http://blog.csdn.net/crylearner/article/details/38521685
'''

class ScanModule:

    informaiton = {
        'name': 'ms17-010',
        'result': '',
        'description': None,
    }

    check_arguments = {
        'host': ['alive'],
        'port': [445, 139],
        'proto': ['TCP'],
        'Service': ['microsoft-ds'],
        'SBanner': '',
        'URL': '',
        'UBanner': '',
        'exp_argv': ['host', 'port'],
    }

    def exp(self, host):

        pass

class SMB_Header(Structure):

    _pack_ = 1  # Alignment
    _fields_ = [
        ("server_component", c_uint32),
        ("smb_command", c_uint8),
        ("nt_status", c_uint32),
        ("flags", c_uint8),
        ("flags2", c_uint16),
        ("process_id_high", c_uint16),
        ("signature", c_uint64),
        ("reserved", c_uint16),
        ("tree_id", c_uint16),
        ("process_id", c_uint16),
        ("user_id", c_uint16),
        ("multiplex_id", c_uint16)
    ]
    def __new__(self, buffer=None):
        return self.from_buffer_copy(buffer)
    def __init__(self, buffer):
        pass


def generate_smb_proto_payload(*protos):
    """Generate SMB Protocol. Pakcet protos in order.
    """
    hexdata = []
    for proto in protos:
        hexdata.extend(proto)
    return b''.join(hexdata)

def negotiate_protocol_request():

    smb_header = [
        b'\xFF\x53\x4D\x42',  # 'server_component': .SMB
        b'\x72',              # 'smb_command': Negotiate Protocol
        b'\x00\x00\x00\x00',  # 'nt_status'
        b'\x18',              # 'flags'
        b'\x01\x28',          # 'flags2'
        b'\x00\x00',          # 'process_id_high'
        b'\x00\x00\x00\x00\x00\x00\x00\x00',  # 'signature'
        b'\x00\x00',          # 'reserved'
        b'\x00\x00',          # 'tree_id'
        b'\xff\xfe',          # 'process_id'
        b'\x00\x00',          # 'user_id'
        b'\x40\x00'           # 'multiplex_id'
    ]

    smb_parameters = [
        b'\x00',              # WordCount
    ]

    smb_data_dialets = [
        # TODO:
        '\x02{}\x00'.format("PC NETWORK PROGRAM 1.0").encode("utf-8"),
        b'\x02\x4c\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00',
        b'\x02\x57\x69\x6e\x64\x6f\x77\x73\x20\x66\x6f\x72\x20\x57\x6f\x72\x6b\x67\x72\x6f\x75\x70\x73\x20\x33\x2e\x31\x61\x00',
        b'\x02\x4c\x4d\x31\x2e\x32\x58\x30\x30\x32\x00',
        b'\x02\x4c\x41\x4e\x4d\x41\x4e\x32\x2e\x31\x00',
        b'\x02\x4e\x54\x20\x4c\x4d\x20\x30\x2e\x31\x32\x00',
    ]

    smb_data = [
        struct.pack('<H', get_bytes_length(smb_data_dialets)),  # ByteCount
    ]
    smb_data.extend(smb_data_dialets)

    netbios = [
        b'\x00',              # 'Message Type:'
        b'\x00',
        struct.pack('>H', get_bytes_length(smb_header, smb_parameters, smb_data)),      # 'Length'
    ]

    return generate_smb_proto_payload(netbios, smb_header, smb_parameters, smb_data)

def session_setup_andx_request():

    smb_header = [
        b'\xFF\x53\x4D\x42',  # 'server_component': .SMB
        b'\x73',              # 'smb_command': Session Setup AndX
        b'\x00\x00\x00\x00',  # 'nt_status'
        b'\x18',  # 'flags'
        b'\x01\x28',  # 'flags2'
        b'\x00\x00',  # 'process_id_high'
        b'\x00\x00\x00\x00\x00\x00\x00\x00',  # 'signature'
        b'\x00\x00',  # 'reserved'
        b'\x00\x00',  # 'tree_id'
        b'\xff\xfe',  # 'process_id'
        b'\x00\x00',  # 'user_id'
        b'\x40\x00'  # 'multiplex_id'
    ]

    smb_parameters_words = [
        b'\xFF',  # AndXCommand: No further command
        b'\x00',  # Reserved
        b'\x88\x00',  # AndXOffset
        b'\x04\x11',  # Max Buffer
        b'\x0a\x00',  # Max Mpx Count
        b'\x00\x00',  # VC Number
        b'\x00\x00\x00\x00',  # Session Key
        b'\x01\x00',  # ANSI Password Length
        b'\x00\x00',  # Unicode Password Length
        b'\x00\x00\x00\x00',  # Reserved
        b'\xd4\x00\x00\x00',  # Capabilities
    ]
    smb_parameters = [
        struct.pack('B', int(get_bytes_length(smb_parameters_words) / 2))
    ]
    smb_parameters.extend(smb_parameters_words)

    smb_data_bytes = [
        b'\x00',        # ANSI Password
        b'\x00\x00',    # Account
        b'\x00\x00',    # Primary Domain
        b'\x57\x00\x69\x00\x6e\x00\x64\x00\x6f\x00\x77\x00\x73\x00\x20\x00\x32\x00\x30\x00\x30\x00\x30\x00\x20\x00\x32\x00\x31\x00\x39\x00\x35\x00\x00\x00',  # Native OS: Windows 2000 2195
        b'\x57\x00\x69\x00\x6e\x00\x64\x00\x6f\x00\x77\x00\x73\x00\x20\x00\x32\x00\x30\x00\x30\x00\x30\x00\x20\x00\x35\x00\x2e\x00\x30\x00\x00\x00',  # Native OS: Windows 2000 5.0
    ]

    smb_data = [
        struct.pack('<H', get_bytes_length(smb_data_bytes)),  # ByteCount
    ]
    smb_data.extend(smb_data_bytes)


    netbios = [
        b'\x00',  # 'Message Type:'
        b'\x00',
        struct.pack('>H', get_bytes_length(smb_header, smb_parameters, smb_data)),  # 'Length'
    ]

    return generate_smb_proto_payload(netbios, smb_header, smb_parameters, smb_data)

# TODO: Flags2控制字符串的格式


def tree_connect_andx_request(ip, user_id):
    smb_header = [
        b'\xFF\x53\x4D\x42',  # 'server_component': .SMB
        b'\x75',              # 'smb_command': Tree Connect AndX
        b'\x00\x00\x00\x00',  # 'nt_status'
        b'\x18',  # 'flags'
        b'\x01\x28',  # 'flags2'
        b'\x00\x00',  # 'process_id_high'
        b'\x00\x00\x00\x00\x00\x00\x00\x00',  # 'signature'
        b'\x00\x00',  # 'reserved'
        b'\x00\x00',  # 'tree_id'
        b'\xff\xfe',  # 'process_id'
        user_id,  # 'user_id'
        b'\x40\x00'  # 'multiplex_id'
    ]

    ipc = "\\\\{}\IPC$\x00".format(ip)

    smb_parameters_words = [
        b'\xFF',  # AndXCommand: No further command
        b'\x00',  # Reserved
        b'\x60\x00',  # AndXOffset
        b'\x08\x00',  # Flags
        b'\x01\x00',  # Password Length
    ]
    smb_parameters = [
        struct.pack('B', int(get_bytes_length(smb_parameters_words) / 2))
    ]
    smb_parameters.extend(smb_parameters_words)

    ipc = "\\\\{}\IPC$\x00".format(ip)

    x = ipc.encode("utf-8")

    print(x)

    smb_data_bytes = [
        b'\x00',                     # Password
        ipc.encode(),                # Path
        b'\x3f\x3f\x3f\x3f\x3f\x00', # Service: Matches any type of device or resource
    ]

    smb_data = [
        struct.pack('<H', get_bytes_length(smb_data_bytes)),  # ByteCount
    ]
    smb_data.extend(smb_data_bytes)

    netbios = [
        b'\x00',  # 'Message Type:'
        b'\x00',
        struct.pack('>H', get_bytes_length(smb_header, smb_parameters, smb_data)),  # 'Length'
    ]

    return generate_smb_proto_payload(netbios, smb_header, smb_parameters, smb_data)

def peek_named_pipe_request(tree_id, process_id, user_id, multiplex_id):

    smb_header = [
        b'\xFF\x53\x4D\x42',  # 'server_component': .SMB
        b'\x25',              # 'smb_command': Transaction
        b'\x00\x00\x00\x00',  # 'nt_status'
        b'\x18',              # 'flags'
        b'\x01\x28',          # 'flags2'
        b'\x00\x00',          # 'process_id_high'
        b'\x00\x00\x00\x00\x00\x00\x00\x00',  # 'signature'
        b'\x00\x00',          # 'reserved'
        tree_id,
        process_id,
        user_id,
        multiplex_id
    ]

    smb_parameters_words = [
        b'\x00\x00',  # Total Parameter Count
        b'\x00\x00',  # Total Data Count
        b'\xff\xff',  # Max Parameter Count
        b'\xff\xff',  # Max Data Count
        b'\x00',      # Max Setup Count
        b'\x00',      # Reserved
        b'\x00\x00',  # Flags
        b'\x00\x00\x00\x00',  # Timeout: Return immediately
        b'\x00\x00',  # Reversed
        b'\x00\x00',  # Parameter Count
        b'\x4a\x00',  # Parameter Offset
        b'\x00\x00',  # Data Count
        b'\x4a\x00',  # Data Offset
        b'\x02',      # Setup Count
        b'\x00',      # Reversed
        b'\x23\x00',  # SMB Pipe Protocol: Function: PeekNamedPipe (0x0023)
        b'\x00\x00',  # SMB Pipe Protocol: FID
    ]
    smb_parameters = [
        struct.pack('B', int(get_bytes_length(smb_parameters_words) / 2))
    ]
    smb_parameters.extend(smb_parameters_words)

    # If the field is not specified in the section for the subcommands,the field should be set to \PIPE\
    smb_data_bytes = [
        '{}\x00'.format('\\PIPE\\').encode("utf-8")  # \PIPE\
    ]

    smb_data = [
        struct.pack('<H', get_bytes_length(smb_data_bytes)),  # ByteCount
    ]
    smb_data.extend(smb_data_bytes)

    netbios = [
        b'\x00',  # 'Message Type:'
        b'\x00',
        struct.pack('>H', get_bytes_length(smb_header, smb_parameters, smb_data)),  # 'Length'
    ]

    return generate_smb_proto_payload(netbios, smb_header, smb_parameters, smb_data)

def check(ip, port=445):

    buffersize = 1024
    timeout = 5.0

    dict = {
        'module': 'ms17-010',
        'host': '{}:{}'.format(ip, port),
        'process': None,
        'result': None,
        'info': None,
    }

    try:
        # connect
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        client.connect((ip, port))

        # SMB - Negotiate protocol  request
        raw_proto = negotiate_protocol_request()
        client.send(raw_proto)
        tcp_response = client.recv(buffersize)

        # SMB - Session Setup Andx Request
        raw_proto = session_setup_andx_request()
        client.send(raw_proto)
        tcp_response = client.recv(buffersize)

        # TODO:SMB通用解析包
        # get uid from response
        smb_header = SMB_Header(tcp_response[4:36])
        user_id = struct.pack('<H', smb_header.user_id)
        # get server banner
        smb_parameters_and_data = tcp_response[36:]
        native_os = smb_parameters_and_data[9:].decode("utf-8")

        # SMB - Tree Connect AndX Request
        raw_proto = tree_connect_andx_request(ip, user_id)
        client.send(raw_proto)
        tcp_response = client.recv(buffersize)

        smb_header = SMB_Header(tcp_response[4:36])
        tree_id = struct.pack('<H', smb_header.tree_id)
        process_id = struct.pack('<H', smb_header.process_id)
        user_id = struct.pack('<H', smb_header.user_id)
        multiplex_id = struct.pack('<H', smb_header.multiplex_id)

        raw_proto = peek_named_pipe_request(tree_id, process_id, user_id, multiplex_id)
        client.send(raw_proto)
        tcp_response = client.recv(buffersize)

        smb_header = SMB_Header(tcp_response[4:36])
        nt_status = struct.pack('>L', smb_header.nt_status)

        if nt_status == b'\xc0\x00\x02\x05':
            dict['result'] = 'yes'
        else:
            dict['result'] = 'no'

        dict['process'] = 'success'
        dict['info'] += 'NT_STATUS:{}.\nServer banner:{}.'.format(nt_status, native_os)

        return dict

    except Exception as e:
        dict['process'] = 'error'
        dict['error'] = e
        return dict

def get_bytes_length(*bytes_arr):
    length = 0
    for bytes_list in bytes_arr:
        for bytes in bytes_list:
            length += len(bytes)
    return length

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Error: {} {IP or Host}".format(sys.argv[0]))
        sys.exit(1)
    x = check(sys.argv[1])
    print(x)
