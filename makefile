all: server client lossy_link

server: server.py
	python3 server.py

client: client.py
	python3 client.py

lossy_link: lossy_link-linux
	./lossy_link-linux 127.0.0.1:12122 127.0.0.1:13133
