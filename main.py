from colorama import Fore, init
import os

if os.name == 'nt':
	init(convert=True)


def get_ascii_art(name: str):
	with open("ascii-art/" + name + ".txt", 'r') as f:
		return f.read()
