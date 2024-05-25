import socket
import subprocess
import sys

# Configuration for the RSP-TCP-Server
RSP_HOST = '123.123.123.123'  # IP address or Hostname of RSP-TCP-Server
RSP_PORT = 1234         # Port of TCP-Server

# Using the configuration file from the command line arguments
if len(sys.argv) < 2:
    print("Please provide the path to the configuration file.")
    sys.exit(1)
CONFIG_FILE = sys.argv[1]

# Path to the spectrumserver from the command line arguments
if len(sys.argv) < 3:
    print("Please provide the path to the spectrumserver.")
    sys.exit(1)
SPECTRUMSERVER_PATH = sys.argv[2]

# Establish connection to the RSP-TCP-Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rsp_socket:
    rsp_socket.connect((RSP_HOST, RSP_PORT))
    print('Connected to RSP-TCP-Server')

    # Start the spectrumserver process with the specified configuration file
    spectrumserver_cmd = [SPECTRUMSERVER_PATH, '-c', CONFIG_FILE]
    with subprocess.Popen(spectrumserver_cmd, stdin=subprocess.PIPE) as spectrumserver_proc:
        print('spectrumserver started')

        # Receive data from the RSP-TCP-Server and send it to spectrumserver
        while True:
            data = rsp_socket.recv(1024)  # Receive data in 1024-byte chunks
            if not data:
                break
            spectrumserver_proc.stdin.write(data)
            spectrumserver_proc.stdin.flush()

print('Connection to RSP-TCP-Server closed')
