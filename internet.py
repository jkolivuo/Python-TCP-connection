

import socket, sys



def main():
  
  if len(sys.argv) < 2:
    print "Not enough arguments"
    sys.exit(1)
  else:
    print "Arguments received"
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    TCP_PORT = 10000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT)) 

    s.send("HELO 10000\r\n")
    data = s.recv(1024)
    UDP_PORT = UDP(data)
    
    
    s.close()

    print 'Received', data
    
        #answer(question)
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 10000))
    
    while(1):
      msg = "Hello"
      try:
        sock.sendto(msg, (IP, TCP_PORT))
        received = sock.recvfrom(1024)
        
        print "Server reply: " + received

      except socket.error, msg:
        print "Error Code: " + str(msg[0]) + " Message " + msg[1]
        sys.exit(1)



questions = {
  "What is your name?":
  "It is Arthur, King of the Britons.",
  "What is your quest?":
  "To seek the Holy Grail.",
  "What is your favourite colour?":
  "Blue.",
  "What is the capital of Assyria?":
  "I don't know that.",
  "What is the air-speed velocity of an unladen swallow?":
  "What do you mean? An African or European swallow?",
}
 
 
def answer(question):
  a = list()
  while True:
    part, separator, question = question.partition('?')
    part = part.lstrip() + separator
    if part in questions:
      a.append(questions[part])
    if not question:
      break
    return ' '.join(a) 

def UDP(data):
  d = data.split(' ')
  UDP_PORT = d[1]
  UDP_PORT.strip()
  UDP_PORT = int(UDP_PORT)
  return UDP_PORT

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    sys.exit(1)