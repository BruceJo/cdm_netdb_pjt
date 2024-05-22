import time
import os
import sys

def do_something():
    while True:
        time.sleep(3)
        print(2)

def check_status():
    try:
        with open(status_path, 'r') as sts:
            last_line = sts.readlines()[-1]
        return True if last_line == 'init' else False

    except:
        pass

def write_status():
    with open(status_path, 'w') as sts:
        sts.write("idle")

if __name__ == '__main__':
    status_path = sys.argv[1]
    run_status = 'idle'
    isrun_init = check_status() 

    if check_status():      # 0 : run | idle, 1 : init
        print('> run GetActivityLog ~ SetPreResult <')
        write_status()



    
    # do_something()