import time
 
def fast_print(text):
 
    for letter in text:
        if letter == ' ':
            print(letter, end = '')
        else:
            time.sleep(0.01)
            print(letter, end = '')
    print()
 
def slow_print(text):
 
    for letter in text:
        if letter == ' ':
            print(letter, end = '')
        else:
            time.sleep(0.02)
            print(letter, end = '')
    print()
 
def slower_print(text):
 
    for letter in text:
        if letter == ' ':
            print(letter, end = '')
        else:
            time.sleep(0.05)
            print(letter, end = '')
    print()
 
def very_slow_print(text):
 
    for letter in text:
        if letter == ' ':
            print(letter, end = '')
        else:
            time.sleep(0.5)
            print(letter, end = '')
    print()

def sentence_print(sentence_list):
    for sentence in sentence_list:
        time.sleep(0.8)
        slower_print(sentence)
 