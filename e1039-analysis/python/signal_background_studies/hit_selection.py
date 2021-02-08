import uproot4
import awkward1 as ak
import numpy as np
import matplotlib.pyplot as plt

root = uproot4.concatenate("combined_data/track_*.root:save/rawEvent",["fTriggerBits","fAllHits.pos","fAllHits.driftDistance","fAllHits.detectorID"],library="ak",how="zip")

def TrigMask(file, bit1=65, bit2=67):
    '''returns list of indices of valid events based on TriggerBits'''
    validEvents = np.array([])
    for i in range(len(file)):
        if (file[i]["fTriggerBits"] == bit1) or (file[i]["fTriggerBits"] == bit2):
            validEvents = np.append(validEvents,i)
    return validEvents

def hitSelect(file, trigger=None):
    st1 = 0
    st2 = 0
    st3 = 0
    st4 = 0
    
    if trigger=None:   # look at all hits in the file
        for i in range(len(file)):   # loop thru all events
            st_flag = 0
            validEvent = file[i]["fAllHits"].detectorID
            for j in range(len(validEvent)):   # loop through hits in validEvent
                if (validEvent[j] == 31) or (validEvent[j] == 32):   # h1bt
                    st_flag = 1
                if (validEvent[j] == 37) or (validEvent[j] == 38):   # h2bt
                    st_flag = 2
                if (validEvent[j] == 39) or (validEvent[j] == 40):   # h3bt
                    st_flag = 3
                if (validEvent[j] == 45) or (validEvent[j] == 46):
                    st_flag = 4
            # check which flag triggered
            if (st_flag == 4):
                st4 += 1
            elif (st_flag == 3):
                st3 += 1
            elif (st_flag == 2):
                st2 += 1
            elif (st_flag == 1):
                st1 += 1
            else:
                pass
        
    else:   # look only at hits with given trigger
        trigHits = TrigMask(file)
        for i in range(len(trigHits)):   # loop through hits with given triggerBits
            st_flag = 0
            validEvent = file[trigHits[i]]["fAllHits"].detectorID
            for j in range(len(validEvent)):
                if (validEvent[j] == 31) or (validEvent[j] == 32):   # h1bt
                    st_flag = 1
                if (validEvent[j] == 37) or (validEvent[j] == 38):   # h2bt
                    st_flag = 2
                if (validEvent[j] == 39) or (validEvent[j] == 40):   # h3bt
                    st_flag = 3
                if (validEvent[j] == 45) or (validEvent[j] == 46):
                    st_flag = 4
            # check which flag triggered
            if (st_flag == 4):
                st4 += 1
            elif (st_flag == 3):
                st3 += 1
            elif (st_flag == 2):
                st2 += 1
            elif (st_flag == 1):
                st1 += 1
            else:
                pass
   
    # plot
    data = [st1,st2,st3,st4]
    labels = ["st1","st2","st3","st4"]
    x = np.arange(len(labels))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(x,data)
    ax.set_title("Number of Events with hits up to station")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    
    #plt.savefig("hit_selection")