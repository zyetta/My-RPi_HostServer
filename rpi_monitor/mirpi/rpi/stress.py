from time import time
i = 1
j = 1
time_now = time()

while((time()-time_now) < 30*1000):
    i += 1
    j = 1 / i + j
    print(j)