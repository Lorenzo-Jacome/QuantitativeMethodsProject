import numpy as np
import matplotlib.pyplot as plt

class hstcpNetwork:
    HWhs = 83000 #High-window threshold
    LWhs = 31 #Low-window threshold
    Rhs = 0.1 #Decrease congestion window after loss above LWhs
    cwnd = 70000 #Congestion window
    sst = 10
    cwndInit = 0 #Congestion window initial value

    #Constructor function:
    def __init__(self, cwndInit):
        self.cwndInit = cwndInit

    #Assist functions for the increase or decrease operations:
    def alphaIncrease(self, cwnd):
        return((cwnd ** 2) * (0.078 / (cwnd**1.2)) * 2 * (self.betaIncrease(cwnd) / (2-self.betaIncrease(cwnd))) + 0.5)

    def betaIncrease(self, cwnd):
        return((self.Rhs - 0.5) * ((np.log10(cwnd) - np.log10(self.LWhs)) / (np.log10(self.HWhs) - np.log10(self.LWhs))) + 0.5)

    #Main function to increase congestion window when ACKs are recieved
    def IncreaseProcedures(self):
        self.cwnd = self.cwnd + (self.alphaIncrease(self.cwnd) / self.cwnd)

    #Main function to decrease the congestion window when there are unACKs
    def DecreaseProcedures(self):
        self.cwnd = (1 - self.betaIncrease(self.cwnd)) * self.cwnd
        self.sst = self.cwnd

    #Main function for a timeout procedure
    def TimeoutProcedures(self):
        self.cwnd = (1 - self.betaIncrease(self.cwnd)) * self.cwnd

        if(self.cwnd > self.cwndInit):
            self.sst = self.cwnd
        else:
            self.sst = self.cwndInit

        self.cwnd = self.cwndInit

#TODO: Simulate exchange of packages:

increaseArray = []
test = hstcpNetwork()

while test.cwnd >= 1:
    print(test.cwnd)
    increaseArray.append(test.cwnd)
    test.DecreaseProcedures()

plt.plot(increaseArray)
plt.ylabel('some numbers')
plt.show()