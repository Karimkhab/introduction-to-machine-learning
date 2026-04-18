from threading import Thread
import time

cost = 0

def best_function():
    global cost
    print('Иди нахуй!')
    time.sleep(2)
    cost += 1
    print(f'Да да иди иди нахуй!{cost}')

def main():
    threads = [Thread(target=best_function) for _ in range(5)]
    for thread in threads:
        thread.start()
        time.sleep(1)


if __name__ == "__main__":
    main()
