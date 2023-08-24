from colorama import Fore, init
import os
import pickle
import cpuinfo
import psutil
import text_handling as th
import time
import random
import sys

SAVE_PATH = "save.dat"

if os.name == 'nt':
	init(convert=True)

savestate = {}
first_time = True


def clear():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')


clear()


def boot_up():
	clear()
	for i in range(len(th.get_sequence("startup.booting"))):
		print(th.get_sequence(
			"startup.booting." + str(i),
			cpu=cpuinfo.get_cpu_info()["brand_raw"],
			mem=f"{round(psutil.virtual_memory().total / 1024 / 1024, 2)} MB")
		)
		time.sleep(round(random.uniform(0.2, 3), 2))

	if os.path.exists(SAVE_PATH):
		global savestate, first_time
		try:
			with open(SAVE_PATH, "rb") as f:
				savestate = pickle.load(f)
			first_time = False
		except FileNotFoundError:
			savestate = {
				"day": 0,
				"progress": 0
			}
			first_time = True
		else:
			sys.exit("Savefile could not be loaded")

	for i in range(len(th.get_sequence("startup.connecting"))):
		if i == 3:
			incorrect = True
			while incorrect:
				pin = input(th.get_sequence("general_prompts.pin"))
				if incorrect := savestate["opsec-pin"] != pin:
					print(th.get_sequence("startup.connecting.3.0"))
				else:
					print(th.get_sequence("startup.connecting.3.1"))
		elif i == 9:
			incorrect = True
			while incorrect:
				un = input(th.get_sequence("general_prompts.username"))
				pw = input(th.get_sequence("general_prompts.password"))
				if incorrect := (savestate["bls-username"] != un or savestate["bls-password"] != pw):
					print(th.get_sequence("startup.connecting.9.0"))
				else:
					print(th.get_sequence("startup.connecting.9.1"))
		else:
			print(th.get_sequence("startup.connecting." + str(i)))
			if i not in (2, 8):
				time.sleep(round(random.uniform(0.5, 5), 2))
	time.sleep(5)
	clear()


running = True

while running:
	if first_time:
		print(th.get_ascii_art("title"))
		print("")
		print(th.get_text("story.intro"))
		print("")
		input("Press enter to continue...")
	boot_up()
	print(th.get_ascii_art("title"))
	kid = str(random.randint(0, 999))
	kid = ("0" * (3 - len(kid))) + kid
	print(th.get_sequence("bls.welcome", kid=kid))

