import yarp
import sys
import time
from Introduction import introduction
from yarp_modules import YarpPorts


def main():
    # Initialize YARP
    if not yarp.Network.checkNetwork():
        print("❌ YARP server not found. Exiting...")
        sys.exit(1)

    yarp.Network.init()

    #run yarp module
    # ---- Step 5: Configure and run experiment module ----
    rf = yarp.ResourceFinder()
    rf.setVerbose(True)
    rf.setDefaultContext("skinDataExperiment")
    rf.setDefaultConfigFile("skinDataExperiment.ini")

    YarpModule = YarpPorts()


    if rf.configure(sys.argv):
        YarpModule.runModule(rf)
    sys.exit()


if __name__ == "__main__":
    main()
