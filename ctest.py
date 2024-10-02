
import socket,os
import threading, pyaudio, pickle,struct
host_name = socket.gethostname()
host_ip = '85.23.95.56'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9611
def audio_stream():

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 22050
    OUTPUT_INDEX=3

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK, output_device_index=OUTPUT_INDEX)	
	
	
					
	# create socket
	
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_address = (host_ip,port-1)
    print('server listening at',socket_address)
    client_socket.connect(socket_address) 
    print("CLIENT CONNECTED TO",socket_address)
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024) # 4K
                if not packet: break
                data+=packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            stream.write(frame)

        except:
            
            break

    client_socket.close()
    print('Audio closed')
    os._exit(1)
	
t1 = threading.Thread(target=audio_stream, args=())
t1.start()




""" if __name__ == '__main__':
    client_program() """