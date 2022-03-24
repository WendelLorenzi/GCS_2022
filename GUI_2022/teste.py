import time

def segundo():
    time.sleep(5)
    print("retornou")
    return 1

b=0
while True:
    a= segundo()
    b= a + b
    print(b)