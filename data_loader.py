import os
import json
from pprint import pprint
import csv
import codecs

data_directory = "./data/facebook-alexandrumeterez/messages/"

def extract_messages(file_json):
    lines = {}
    messages = file_json['messages']
    line_id = 0
    if "participants" not in file_json:
        pprint(file_json)
    participants = [participant["name"] for participant in file_json['participants']]

    for message in messages:
        if "sender_name" not in message:
            continue
        sender_name = message['sender_name']
        if "content" not in message:
            continue
        content = message['content']
        line_obj = {"sender_name": sender_name, "content": content}
        lines[line_id] = line_obj
        line_id += 1
    return lines, participants


def load_conversations(all_data):
    conversations = []

    for directory in os.listdir(all_data):
        with open(data_directory + directory + "/message.json", 'r') as f:
            file_json = json.load(f)
            lines, participants = extract_messages(file_json)
            if len(lines) < 5:
                continue
            conv_obj = {"lines": lines, "participants": participants}
            conversations.append(conv_obj)
    return conversations


def extract_sentence_pairs(conversations):
    qa_pairs = []
    for conversation in conversations:
        # Iterate over all the lines of the conversation
        for i in range(len(conversation["lines"]) - 1):  # We ignore the last line (no answer for it)
            inputLine = conversation["lines"][i]["content"].strip()
            targetLine = conversation["lines"][i+1]["content"].strip()
            # Filter wrong samples (if one of the lists is empty)
            if inputLine and targetLine and len(inputLine) > 0 and len(targetLine) > 0:
                qa_pairs.append([inputLine, targetLine])
    return qa_pairs

if __name__ == "__main__":
    conversations = load_conversations(data_directory)
    pairs = extract_sentence_pairs(conversations)
    pairs = list(filter(lambda x: len(x) == 2, pairs))
    delimiter = '\t'
    # Unescape the delimiter
    delimiter = str(codecs.decode(delimiter, "unicode_escape"))
    with open("./data/datafile", 'w', encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile, delimiter=delimiter)
        for pair in pairs:
            writer.writerow(pair)