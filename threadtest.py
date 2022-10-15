import threading
import time

class einThread(threading.Thread):
    def __init__(self, threadID, name, count):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.count = count
        
    def run(self):
        print(self.name + " wird gestartet." + "\n")
        print_time(self.name, 1, self.count)
        print(self.name + " wird gestoppt." + "\n")
    
def print_time(name, delay, count):
    while count:
        time.sleep(delay)
        print("%s: %s %s" % (name, time.ctime(time.time()), count) + "\n")
        count -= 1
            
thread1 = einThread(1, "Thread1", 10)
thread2 = einThread(2, "Thread2", 5)



thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("Main Thread ist fertig.")