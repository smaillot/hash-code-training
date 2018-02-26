import numpy
import matplotlib.pylab

with open('logs_big.out', 'r') as f:
    tab = []
    n = int(f.readline().split(" ")[0])
    for i in range(n):
        tab.append([float(j) for j in f.readline().split(" ")])
        
before, after, time1, time2 = [[i[j] for i in tab] for j in range(4)]

figure(1)

hist(after, bins=500, alpha=0.6, cumulative=-1)
hist(before, bins=500, alpha=0.6, cumulative=-1)
legend(['after', 'before'])
title('score')

figure(2)

hist(time1, bins=500, alpha=0.6, cumulative=1)
hist(time2, bins=500, alpha=0.6, cumulative=1)
legend(['before', 'after'])
title('time')

figure(3)

plot(before, after, '.', alpha=0.6)
xlabel('before')
ylabel('after')
title('score')

def cumul(data1, data2):
    best = 0
    best2 = 0
    out1 = []
    out2 = []
    out3 = []
    out4 = []
    for i in range(len(data1)):
        if data1[i] > data1[best]:
            best = i
        if data2[i] > data2[best2]:
            best2 = i
        out1.append(data1[best])
        out2.append(data2[best])
        out3.append(data1[best2])
        out4.append(data2[best2])
    return out1, out2, out3, out4

figure(4)

y1, y2, z1, z2 = cumul(before, after)
x = range(len(y1))

plot(x, y1, color='red')
plot(x, y2, color='orange')
plot(x, after, color='cyan')
plot(x, z2, color='blue')
legend(['best before', 'corresponding after', 'after', 'best after'])