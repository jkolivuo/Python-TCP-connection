import sys, socket, struct
from questions import answer

#Funktio, jossa saadusta tcp-viestista otetaan udp-portti talteen
#ja tallennetaan se muuttujaan.
def get_udp(tcp_data):
	data = tcp_data.split(' ')
	udp_p = data[1]
	udp_p.strip()
	udp_p = int(udp_p)
	return udp_p


def main():
#Komentoriviargumenttien syotto, seka mahdollinen HELP-tulostus, jos argumentteja ei ole oikea maara
	if len(sys.argv) < 2:
		print "HELP: Please give server address and port as command-line arguments."
		print "Server address should be ii.virtues.oulu.fi"
		print "Please give port number in range of 10000-10100"
		print "Proper command should be in form: python program.py server port"
		sys.exit(1)
	else:
		print "Arguments received!"
		addr = str(sys.argv[1])
		tcp_port = int(sys.argv[2])
		

	host_ip = socket.gethostbyname(addr)
	

	#Luodaan TCP- ja UDP-socket

	tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	#Etsitaan oikea portti valilta 10000-10100
	for bind_port in range(10000,10100):
		try:
			udp_socket.bind(("",bind_port))
			break;
		except udp_socket.error:
			#Annetaan virhe, mikali porttia ei ole kaytettavissa.
			print "Couldn't bind port"
			

	tcp_socket.connect((host_ip, tcp_port))

	#Lahetetaan TCP:lla HELO viesti + portti, johon bindataan.
	tcp_socket.send("HELO %i\r\n" % bind_port)
	tcp_data = tcp_socket.recv(1024)
	udp_port = get_udp(tcp_data)

	#Luodaan UDP:n headeri osio ja lahetetaan avaava viesti serverille.
	msg = "The eagle has landed\r\n"
	eom = False
	ack = False
	rem = 0
	lenght = len(msg)

	msg_packet = struct.pack("!??HH64s", eom, ack, lenght, rem, msg)
	udp_socket.sendto(msg_packet, (host_ip, udp_port))

	
	#Avataan ja puretaan saadut viestit struct.unpack_from toiminnolla
	#Kaytetaan questions.py tiedoston answers-funktiota oikeiden vastausten toimittamiseen
	#Lopuksi kun vastausta ei ole, suljetaan yhteys.
	while(1):
		data_r,addr = udp_socket.recvfrom(1024)
		(eom, ack, rem, lenght, msg) =  struct.unpack_from("!??HH64s", data_r, 0) #struct.unpack aiheutti virheilmoituksen
		print msg #Tulostetaan kysymys, jotta voi seurata ohjelman toimintaa
		message_out = answer(msg)
		message = struct.pack("!??HH64s", eom, ack, rem, lenght, message_out)
		udp_socket.sendto(message, (host_ip, udp_port))
		print message #Kuten myos vastaus, jolloin tiedetaan, etta ohjelma toimii oikein.
		if not message_out: 
			break
	
	#Suljetaan kumpikin yhteys kun ohjelma on valmis		
	udp_socket.close()
	tcp_socket.close()
	print "Closing..."
		

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "You pressed ctrl+c"
		sys.exit(1)