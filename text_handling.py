import os
import json

TEXT_PATH = "texts"
SEQUENCES_PATH = "sequences.json"

language = "en"


def get_text(uid: str):
	p = os.path.join(TEXT_PATH, language, uid.replace(".", "/") + ".txt")
	with open(p, "r") as f:
		return f.read()


def get_sequence(uid: str):
	p = os.path.join(TEXT_PATH, language, SEQUENCES_PATH)
	with open(p, "r") as f:
		sequences = json.load(f)

