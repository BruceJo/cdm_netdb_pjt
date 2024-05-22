import sys
import time

if __name__ == '__main__':
    i = int(sys.argv[1])
    print(f"{i}번째 작업 시작")
    time.sleep(i+1)
    print(f"> {i}번째 작업 종료")