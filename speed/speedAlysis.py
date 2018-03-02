def speedRangeConvergence(speedDictPath):
    with open(speedDictPath, "rb") as f:
        speedDict = pickle.load(f)
    speedRangeDict = {}
    groupNumber = 10
    for k, v in speedDict.items():
        print(k)
        speedRangeDict[k] = []
        j = 0
        groupSpeed = []
        #print(v)
        for i in v:
            j += 1
            #print(i[0])
            try:
                averageSpeed = reduce(lambda x, y: x + y, i[1])/len(i[1])
            except TypeError as e:
                print('except:', str(e) + "******" + k + "******")
                continue
            if j == groupNumber:
                speedRangeDict[k].append(averageSpeed)
                j = 0
                groupSpeed = []
        if j != 0:
            speedRangeDict[k].append(averageSpeed)
        print(speedRangeDict[k])
    with open("speedRangeDict.pkl", "wb") as f:
        pickle.dump(speedRangeDict, f)
    print(speedRangeDict)
    return speedRangeDict


def speedGraphGenerate(speedDictPath):
    with open(speedDictPath, "rb") as f:
        speedDict = pickle.load(f)
    for k, v in speedDict.items():
        plt.figure()
        plt.ylim(0,100)
        for i in range(len(v)):
            x = list(map(lambda x: x-v[i][0][0], v[i][0])); y = v[i][1]
            #plt.plot(x, y, color = color_sequence[random.randint(0, len(color_sequence)-1)])
            n = i // 10 if i <= 150 else 15
            plt.plot(x, y, color = suncolor_sequence[n])
        plt.xlabel("Time/milliseconds")
        plt.ylabel("Speed/Pixel")
        plt.title(k)
        plt.savefig(speedFolder + k + ".jpg")
        print(k)