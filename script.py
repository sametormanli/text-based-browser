import sys
import os
from _collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

# write your code here
def scrape(resp):
    soup = BeautifulSoup(resp.content, 'html.parser')
    all_tags = all_tags = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    result = soup.find_all(all_tags)
    return '\n'.join(Fore.BLUE + res.text if res.name == 'a' else Style.RESET_ALL + res.text for res in result)

def main():
    history = deque()
    directory = sys.argv[1]
    if not os.path.exists(f'./{directory}'):
        os.mkdir(f'./{directory}')
    while True:
        entry = input()
        if entry[-4:] not in ('.com', '.net', '.org') and entry not in ('exit', 'back'):
            try:
                with open(f'{directory}/{entry}.txt') as text:
                    print(text.read())
            except:
                print('Error: Incorrect URL')
        elif entry == 'bloomberg.com':
            print(bloomberg_com)
            with open(f'{directory}/{entry[:-4]}', 'w') as text:
                text.write(bloomberg_com)
            history.append(entry[:-4])
        elif entry == 'nytimes.com':
            print(nytimes_com)
            with open(f'{directory}/{entry[:-4]}', 'w') as text:
                text.write(nytimes_com)
            history.append(entry[:-4])
        elif entry == 'back' and len(history) > 1:
            history.pop()
            with open(f'{directory}/{history.pop()}') as text:
                print(text.read())
        elif entry == 'exit':
            break
        else:
            if not entry.startswith('http'):
                entry = 'https://' + entry
            content = scrape(requests.get(entry))
            print(content)
            with open(os.path.join(directory, entry[8:-4]), 'w', encoding='UTF-8') as text:
                text.write(content)
            history.append(entry[8:-4])
            #print('Error: No page found')

main()