import numpy as np
import random
import matplotlib.pyplot as plt

class hstcpNetwork:
    HWhs = 83000 #High-window threshold
    LWhs = 31 #Low-window threshold
    Rhs = 0.1 #Decrease congestion window after loss above LWhs
    cwnd = 70000 #Congestion window
    sst = 10 #Slow start threshold
    cwndInit = 0 #Congestion window initial value
    timeout = 300

    #Constructor function:
    def __init__(self, cwndInit, sst, timeout):
        self.cwnd = cwndInit
        self. cwndInit = cwndInit
        self.sst = sst
        self.timeout = timeout

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

    #Function for congestion window increase when cwnd is under the slow start threshold
    def sstIncrease(self):
        self.cwnd = self.cwnd + self.cwnd

def threeWayHandshake(transmissionRounds):
    serverSideTCP = hstcpNetwork(30, 30, 300)
    roundsCounter = 0
    connectionIdleTimeout = 0
    cwndData = []
    unACKData = []

    cwndData.append(serverSideTCP.cwnd)

    file = open("hstcp_history.txt", "w")
    file.write("-----INITIAL DATA----\n")
    file.write("High Window Threshold: " + str(serverSideTCP.HWhs) + " Low Window Threshold: " + str(serverSideTCP.LWhs) + " RHs: " + str(serverSideTCP.Rhs) + "\n")
    file.write("Congestion Window Initial value: " + str(serverSideTCP.cwndInit) + " Slow Start Threshold: " + str(serverSideTCP.sst))
    file.write("\n---------------")

    while roundsCounter <= transmissionRounds:
        file.write("\nRound: " + str(roundsCounter) + " cwnd: " + str(serverSideTCP.cwnd) + " sst: " + str(serverSideTCP.sst))
    
        ack = False
        unACKprob = (serverSideTCP.cwnd * 100) / (serverSideTCP.HWhs + 1)
        connectionIdleTimeout = random.randrange(1, 302)
        
        chanceCalc = random.randrange(0, 101)
        if unACKprob <= chanceCalc:
            ack = True
        else:
            ack = False

        if connectionIdleTimeout > serverSideTCP.timeout:
            serverSideTCP.TimeoutProcedures()
            file.write("\nNetwork feedback: TIMEOUT")
        elif ack == False:
            serverSideTCP.DecreaseProcedures()
            unACKData.append(roundsCounter)
            file.write("\nNetwork feedback: unACK")
            #print("UnACK", unACKprob, " ", chanceCalc)
        elif ack and serverSideTCP.cwnd < serverSideTCP.sst:
            serverSideTCP.sstIncrease()
            file.write("\nNetwork feedback: ACK (SST)")
            #print("SST INCREASE")
        elif ack:
            serverSideTCP.IncreaseProcedures()
            file.write("\nNetwork feedback: ACK")
            #print("hs increase")

        cwndData.append(serverSideTCP.cwnd)
        roundsCounter += 1

    file.close()

    #Data presentation
    print("done")  
    plt.plot(cwndData, "#0ad2f5")

    ax = plt.subplot(111)
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    plt.ylabel('Congestion Window \n(CWND)')
    plt.xlabel('Transmission round')
    plt.grid(axis='y')
    #plt.show()
    plt.savefig('hstcp_history_graph.png')


threeWayHandshake(7500)