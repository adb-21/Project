simport socket
import pickle
import time
import hashlib

class blockchain:
    def __init__():
        self.head = None
        self.tail = None    


class block:
    def __init__(self, public, protected, private, block_id, hash_value, next_block):
        self.block_id = block_id
        self.private = private
        self.public = public
        self.protected = protected
        self.hash_value = hash_value
        self.next = next_block
        

def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9876
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

def socket_accept():
    global address
    global conn
    conn, address = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
    send_commands(conn)
    conn.close()

def send_commands(conn):
    pickle_in = open("chain.pickle","rb")
    var = pickle.load(pickle_in)
    pickle_in.close()

    last_id = var.tail.block_id
    
    job = conn.recv(1024)
    time.sleep(0.1)

    if job == b"aaaa":
        tail = conn.recv(1024)
        tail = int(tail.decode())
        
        if tail <= last_id:
            conn.send("sending".encode())
            time.sleep(0.1)
            current = var.head
            while True:
                if current.block_id == tail:
                  
                    final = pickle.dumps(current)

                    output = []
                    for i in range(0, len(final), 1000):
                        chunk = final[i:i+1000]
                        output.append(chunk)
            
                    length = str(len(output))
                    conn.send(length.encode())        
                    time.sleep(1)
                    
                    for i in range(int(length)):
                        message = output[i]
                        conn.send(message)
                        time.sleep(0.2)
                    break
                    
                else:
                    current = current.next
                

        else:
            conn.send("ok".encode())

    elif job == b"bbbb":


        global received
        global x
        global y
        global z
        x = {}
        y = {}
        z = {}

        received = b""
        counter = conn.recv(1024)
        print("counter received as " + counter.decode())
        time.sleep(0.8)
        for i in range(int(counter.decode())):
            chunk = conn.recv(4096)
            received += chunk
            print("received " + str(i))
        print("data collected")
        data = received.split(b"splitter")

        for i in data:
            a = i.split(b"****")
            typ = a[0]
            name = a[1]
            info = a[2]

            if typ == b"public":
                x[name] = info
            elif typ == b"protected":
                y[name] = info
            elif typ == b"private":
                z[name] = info
        
        pickle_in = open("chain.pickle","rb")
        var = pickle.load(pickle_in)
        pickle_in.close()

        previous = var.tail.block_id
        previous_hash = var.tail.hash_value
        hash_data = str(x) + str(y) + str(z) + previous_hash
        result = hashlib.sha256(str(hash_data).encode())
        hash_value = result.hexdigest()
        
        temp = block(x,y,z,previous+1,hash_value,None)
        
        pickle_in = open("chain.pickle","rb")
        var = pickle.load(pickle_in)
        pickle_in.close()
        
        var.tail.next = temp
        var.tail = temp

        pickle_out = open("chain.pickle","wb")
        pickle.dump(var, pickle_out)
        pickle_out.close()
        
        final = pickle.dumps(temp)

        output = []
        for i in range(0, len(final), 1000):
            chunk = final[i:i+1000]
            output.append(chunk)
        print("data cut")
        length = str(len(output))
        conn.send(length.encode())
        print("length sent")
        time.sleep(1)
        for i in range(int(length)):
            message = output[i]
            conn.send(message)
            time.sleep(0.2)
        print("block sent")

while True:
    create_socket()
    bind_socket()
    socket_accept()




