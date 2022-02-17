import json
from operator import concat
from statistics import median, mean

CONFIG_PATH = "/home/dkefir03/labs/isp/data.json"

def read_config():
    try:
        file = open(CONFIG_PATH)
    except FileNotFoundError:
        print("No such file")
        exit()
    data = json.load(file)
    file.close()
    return data

def remove_spec_chars(text: str):
    chars = "@#$%^&*,;:"
    for c in chars:
        text = text.replace(c, "")
    return text    

def split_to_sents_arr(text: str) -> list:
    sents = []
    for sent in remove_spec_chars(text).split("."):
        if len(sent) > 0:
            words = sent.split(" ")
            words = list(filter(len, words))
            sents.append(words)
    return sents

def average_sent_words_count(sents: list[list]) -> int:
    return int(mean([len(sent) for sent in sents]))

def median_sent_words_count(sents: list[list]) -> int:
    return int(median([len(sent) for sent in sents]))

def words_count_dict(sents: list[list]) -> dict[str, int]:
    words_dict = {}
    for sent in sents:
        for word in sent:
            if word in words_dict:
                words_dict[word] += 1
            else:
                words_dict[word] = 1
    return words_dict

def grams_count_dict(sents: list[list], n: int) -> dict[str, int]:
    grams = {}
    for sent in sents:
        gram = ""
        for i in range(len(sent)):
            if i+n <= len(sent):
                for j in range(n):
                    gram += concat(sent[i+j], " ")
                gram = gram.strip()
                if gram in grams:
                    grams[gram] += 1
                else:
                    grams[gram] = 1
                gram = ""
    return grams

def print_result(sents: list[list], k: int, n: int):
    words = words_count_dict(sents)
    grams = grams_count_dict(sents, n)
    grams = dict(sorted(grams.items(), key=lambda x:x[1], reverse=True))
    average_count = average_sent_words_count(sents)
    median_count = median_sent_words_count(sents)
    print("Text readed from {}\n".format(CONFIG_PATH))
    print("Words repeat count:")
    for word in words:
        print(" {} = {}".format(word, words[word]), end="")
    print()
    print("Average words count per sentence: {}".format(average_count))
    print("Median words count per sentence: {}".format(median_count))
    print("Top {} {}-grams in text:".format(k, n))
    for i, (key, value) in enumerate(grams.items()):
        if i == k:
            break
        print(" {} = {}".format(key, value))

def main():
    json = read_config()
    k, n, text = int(json["k"]), int(json["n"]), str(json["text"])
    sents = split_to_sents_arr(text)
    print_result(sents, k, n)

if __name__ == "__main__":
    main()