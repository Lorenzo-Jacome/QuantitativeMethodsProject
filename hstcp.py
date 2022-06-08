import numpy as np
import matplotlib.pyplot as plt

class hstcpNetwork:
    HWhs = 83000 #High-window threshold
    LWhs = 31 #Low-window threshold
    Rhs = 0.1 #Decrease congestion window after loss above LWhs
    cwnd = 1 #Congestion window

    def alphaIncrease(self, cwnd):
        return((cwnd ** 2) * (0.078 / (cwnd**1.2)) * 2 * (self.betaIncrease(cwnd) / (2-self.betaIncrease(cwnd))) + 0.5)

    def betaIncrease(self, cwnd):
        return((self.Rhs - 0.5) * ((np.log10(cwnd) - np.log10(self.LWhs)) / (np.log10(self.HWhs) - np.log10(self.LWhs))) + 0.5)

    #Main function to increase congestion window
    def IncreaseProcedures(self):
        self.cwnd = self.cwnd + (self.alphaIncrease(self.cwnd) / self.cwnd)

    #TODO: Function for decrease procedure:
    #TODO: Timeout procedure

#TODO: Simulate exchange of packages:

increaseArray = []
test = hstcpNetwork()

while test.cwnd <= 1530:
    increaseArray.append(test.cwnd)
    test.IncreaseProcedures()

plt.plot(increaseArray)
plt.ylabel('some numbers')
plt.show()