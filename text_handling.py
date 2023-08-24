import os
import json
import re
import os

TEXT_PATH = "texts"
SEQUENCES_PATH = "sequences.json"
ASCII_ART_PATH = "ascii-art"

INSERT_REGEX = re.compile(r"(?<!\\)\$([a-zA-Z_\-0-9]+);")


def terminal_format(content: str):
	words_raw = re.split(r" +", content)
	words = []
	i = -1
	while True:
		try:
			i += 1
			if (split_index := words_raw[i].rfind("\n")) != -1:
				words.append(words_raw[i][:split_index + 1])
				words.append(words_raw[i][split_index + 1:])
			else:
				words.append(words_raw[i])
		except IndexError:
			break
	t_w = os.get_terminal_size().columns
	lines = []
	line = ""
	for word in words:
		if len(line) + len(word) > t_w and not line.endswith("\n"):
			lines.append(line + "\n")
			line = ""
		line += word
		if word.endswith("\n"):
			lines.append(line)
			line = ""
			continue
		else:
			if len(line) < t_w:
				line += " "
	if line != "":
		lines.append(line)
	return "".join(lines)


def get_ascii_art(uid: str):
	with open(os.path.join(ASCII_ART_PATH, uid + ".txt"), 'rb') as f:
		return f.read().decode('utf-8')


def get_text(uid: str, **kwargs):
	p = os.path.join(TEXT_PATH, uid.replace(".", "/") + ".txt")
	with open(p, "r") as f:
		content = f.read()
	return terminal_format(content)


def get_sequence(uid: str, **kwargs):
	p = os.path.join(TEXT_PATH, SEQUENCES_PATH)
	with open(p, "r") as f:
		sequences = json.load(f)
	addr_split = uid.split(".")
	data = sequences
	for addr_access in addr_split:
		if isinstance(data, list):
			data = data[int(addr_access)]
		elif isinstance(data, dict):
			data = data[addr_access]
	if isinstance(data, str):
		for match in INSERT_REGEX.finditer(data):
			data = str(data).replace(match.group(0), kwargs[match.group(1)])
	if isinstance(data, list):
		return data
	return terminal_format(data)
