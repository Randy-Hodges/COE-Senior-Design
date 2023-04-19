import time
from datetime import datetime

while True:
    with open("/usr/local/mytest.txt", "w") as f:
        f.write("The current timestamp is: " + str(datetime.now()) + "\n")
        print("gabagabagool")
    time.sleep(30)
