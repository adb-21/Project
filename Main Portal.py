from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import base64
import os
import socket
import hashlib
import pickle
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
global stack
global data
global choice1
global choice2
data = b""


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

def check_stability():
    pickle_in = open("chain.pickle","rb")
    var = pickle.load(pickle_in)
    pickle_in.close()
    current = var.head
    
    while True:
        if current.block_id == var.tail.block_id:
            break
        hash_data = str(current.next.public) + str(current.next.protected) + str(current.next.private) + current.hash_value
        result = hashlib.sha256(str(hash_data).encode())
        temp_value = result.hexdigest()
        if current.next.hash_value != temp_value:
            messagebox.showinfo("Warning", "Blockchain unstable!")
            break
        current = current.next
        

        
    

def update_chain():
    pickle_in = open("chain.pickle","rb")
    var = pickle.load(pickle_in)
    pickle_in.close()

    tail = var.tail.block_id + 1

    job = "aaaa"
    
    s = socket.socket()
    host = "192.168.43.153"
    port = 9876

    s.connect((host, port))    

    s.send(job.encode())
    time.sleep(0.5)

    s.send(str(tail).encode())

    status = s.recv(1024)
    if status == b"sending":
        received = b""
        counter = int(s.recv(1024).decode())
        time.sleep(1)
        for i in range(int(counter)):
            chunk = s.recv(4096)
            received = received + chunk

        temp = pickle.loads(received)

        current = temp
        while True:
            if current.next == None:
                last_block = current
                break
            else:
                current = current.next

        var.tail.next = temp
        var.tail = last_block

        pickle_out = open("chain.pickle","wb")
        pickle.dump(var, pickle_out)
        pickle_out.close()


        
update_chain()          
check_stability()

root = Tk()
root.title("Blockchain Portal")



#FRAME ONE START#############################

frame1 = LabelFrame(root, text = "Upload to Blockchain", padx = 5, pady = 5)
frame1.grid(row = 0, column = 0)

def clicked(value):
    global choice1
    choice1 = value

def getpass():
    global password
    password = str(e1.get()).encode()

def sf():
    global f
    global data
    global salt
    global key
    
    password = b""
    frame1.filename = filedialog.askopenfilename(initialdir = "/C", title = "Select a file", filetypes = (("png files", "*.png"), ("all files", "*.*")))
    splitted = frame1.filename.split("/")
    fn = splitted[len(splitted)-1]

    if choice1 == 3: #for private
        password = str(e1.get()).encode()
        
        fo = open(frame1.filename, "rb")
        image = fo.read()
        fo.close()

        salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt = salt, iterations=1,backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        image = f.encrypt(image)
        print("data encrypted")
        file_out = open(frame1.filename +" " + "salt" + ".txt", "wb")
        file_out.write(salt)
        file_out.close()
 
        
        if len(data) == 0:
            data = b"private" + b"****" + fn.encode() + b"****" + image 
        else:
            data = data + b"splitter" + b"private" + b"****" + fn.encode() + b"****" + image 
        print("data updated")
        
    elif choice1 == 2: #for protected
        password = str(e1.get()).encode()

        fo = open(frame1.filename, "rb")
        image = fo.read()
        fo.close()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt = b"", iterations=1,backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        image = f.encrypt(image)

        file_out = open(frame1.filename +" " + "key" + ".txt", "w")
        file_out.write(key.decode())
        file_out.close()



        if len(data) == 0:
            data = b"protected" + b"****" + fn.encode() + b"****" + image 
        else:
            data = data + b"splitter" + b"protected" + b"****" + fn.encode() + b"****" + image 

    elif choice1 == 1:    #for public
        fo = open(frame1.filename, "rb")
        image = fo.read()
        fo.close()

        if len(data) == 0:
            data = b"public" + b"****" + fn.encode() + b"****" + image 
        else:
            data = data + b"splitter" + b"public" + b"****" + fn.encode() + b"****" + image 

def uf():
    job = "bbbb"
    s = socket.socket()
    host = "192.168.43.153"
    port = 9876

    s.connect((host, port))

    s.send(job.encode())
    time.sleep(1)


    output = []
    for i in range(0, len(data), 1000):
        chunk = data[i:i+1000]
        output.append(chunk)
    print("output done")
    
    length = str(len(output))
    s.send(length.encode())
    time.sleep(1)
    print("length sent as " + length)
    for i in range(int(length)):
        message = output[i]
        s.send(message)
        time.sleep(0.2)
        print("sent " + str(i))
    print("whole data sent")
    received = b""
    counter1 = s.recv(1024)
    counter1 = counter1.decode()
    counter = str(counter1)
    time.sleep(1)
    print("counter received")
    for i in range(int(counter)):
        chunk = s.recv(4096)
        received = received + chunk
    print("block received")
    temp = pickle.loads(received) 

    file_out = open("recent block id.txt", "w")
    file_out.write(str(temp.block_id))
    file_out.close()

    pickle_in = open("chain.pickle","rb")
    var = pickle.load(pickle_in)
    pickle_in.close()
    
    var.tail.next = temp
    var.tail = temp

    pickle_out = open("chain.pickle","wb")
    pickle.dump(var, pickle_out)
    pickle_out.close()





btn1 = Button(frame1, text="Select file", padx = 20, command = sf)
btn1.grid(row=4, column=0, padx=10, pady = 10)

label1 = Label(frame1, text="Select Accessibility")
label1.grid(row = 0, column = 0, pady = 10)

r = IntVar()

rb1 = Radiobutton(frame1, text = "Public", variable = r, value = 1, command = lambda: clicked(r.get()))
rb2 = Radiobutton(frame1, text = "Protected", variable = r, value = 2, command = lambda: clicked(r.get()))
rb3 = Radiobutton(frame1, text = "Private", variable = r, value = 3, command = lambda: clicked(r.get()))

rb1.grid(row = 1, column = 0)
rb2.grid(row = 1, column = 1)
rb3.grid(row = 1, column = 2, padx = 20)

label4 = Label(frame1, text="Enter Password")
label4.grid(row=2, column=0, pady=10, padx = 15)

e1 = Entry(frame1, width = 20, borderwidth = 5)
e1.grid(row = 3, column = 0, padx = 10, pady = 15)

btnuf = Button(frame1, text = "Upload files", padx = 20, command = uf)
btnuf.grid(row = 3, column = 2, padx = 10, pady = 10)



#FRAME TWO START  #######################################

frame2 = LabelFrame(root, text="Show Blockchain", padx = 5, pady = 5)
frame2.grid(row = 0, column = 1)

#######
label2 = Label(frame2, text="Enter Block Number")
label2.grid(row=0, column=0, pady = 7)

e2 = Entry(frame2, width = 20, borderwidth = 5)
e2.grid(row = 1, column = 0, padx = 10, pady = 0)

########
label5 = Label(frame2, text="Enter file name")
label5.grid(row=4, column=0, pady = 7)

e3 = Entry(frame2, width = 20, borderwidth = 5)
e3.grid(row = 5, column = 0, padx = 10, pady = 0)
#######
label6 = Label(frame2, text="Enter key")
label6.grid(row=4, column=1, pady = 7)

e4 = Entry(frame2, width = 20, borderwidth = 5)
e4.grid(row = 5, column = 1, padx = 10, pady = 0)

#######

label8 = Label(frame2, text="Enter Password")
label8.grid(row=6, column=0, pady = 7)

e5 = Entry(frame2, width = 20, borderwidth = 5)
e5.grid(row = 7, column = 0, padx = 10, pady = 0)

#######

label3 = Label(frame2, text="Choose accessibility")
label3.grid(row=0, column=1, padx = 10, pady = 7)

s = IntVar()

def clicked1(value):
    global choice2
    choice2 = value

rb4 = Radiobutton(frame2, text = "Public      ", variable = s, value = 1, command = lambda: clicked1(s.get()))
rb5 = Radiobutton(frame2, text = "Protected", variable = s, value = 2, command = lambda: clicked1(s.get()))
rb6 = Radiobutton(frame2, text = "Private     ", variable = s, value = 3, command = lambda: clicked1(s.get()))

rb4.grid(row = 1, column = 1)
rb5.grid(row = 2, column = 1)
rb6.grid(row = 3, column = 1)
########

def show(xx):
    choice2 = xx
    target = int(e2.get())
    if choice2 == 1:
        typ = "public"
    elif choice2 == 2:
        typ = "protected"
    elif choice2 == 3:
        typ = "private"

    
    pi = open("chain.pickle", "rb")
    chain_data = pickle.load(pi)
    pi.close()

    current = chain_data.head

    while True:
        if current.block_id == target:
            if typ == "public":
                msg = ""
                for key in current.public:
                    msg = msg + " " + key.decode()

            elif typ == "protected":
                msg = ""
                for key in current.protected:
                    msg = msg + " " + key.decode()

            elif typ == "private":
                msg = ""
                for key in current.private:
                    msg = msg + " " + key.decode()

            messagebox.showinfo("File names", msg)
            break

        else:
            current = current.next


def gf(xx):
    choice2 = xx
    target = int(e2.get())
    if choice2 == 1:
        typ = "public"
    elif choice2 == 2:
        typ = "protected"
    elif choice2 == 3:
        typ = "private"

    file = str(e3.get())

    pi = open("chain.pickle", "rb")
    chain_data = pickle.load(pi)
    pi.close()

    current = chain_data.head

    while True:
        if current.block_id == target:
            
            if typ == "public":
                ed = current.public[file.encode()]
                ba = bytearray(ed)
                
                fo = open("retrieved " + file ,"wb") 
                fo.write(ba)
                fo.close()
                    
            elif typ == "protected":
                key = str(e4.get())
                ed = current.protected[file.encode()]
                f = Fernet(key)
                ed = f.decrypt(ed)
                
                ba = bytearray(ed)
                
                fo = open("retrieved " + file ,"wb") 
                fo.write(ba)
                fo.close()

            elif typ == "private":
                password = str(e5.get()).encode()
                ed = current.private[file.encode()]
                kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt = salt_data, iterations=1,backend=default_backend())
                key = base64.urlsafe_b64encode(kdf.derive(password))
                f = Fernet(key)
                
                ed = f.decrypt(ed)
                
                ba = bytearray(ed)
                
                fo = open("retrieved " + file ,"wb") 
                fo.write(ba)
                fo.close()

            break

        else:
            current = current.next



def get_salt():
    global salt_data
    frame2.filename = filedialog.askopenfilename(initialdir = "C:/Users/Admin/Desktop", title = "Select a file", filetypes = (("text files", "*.txt"), ("all files", "*.*")))
    fo = open(frame2.filename, "rb")
    salt_data = fo.read()
    fo.close()


btnsf = Button(frame2, text="Show Files", padx = 20, command = lambda: show(choice2))
btnsf.grid(row = 2, column = 0, padx = 10, pady = 10)

btngf = Button(frame2, text="Get File", padx = 30, command = lambda: gf(choice2))
btngf.grid(row = 8, column = 1, padx = 10, pady = 10)

btngs = Button(frame2, text="Select salt file", padx = 20, command = get_salt)
btngs.grid(row = 7, column = 1, padx = 10, pady = 10)












root.mainloop()
