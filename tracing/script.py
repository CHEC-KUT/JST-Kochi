def GeneralDataProcessing():
    generalDict = {}
    mark = 0
    kb = define_ex_kb()

    # Initialization
    for i in dataIndex():
        try:
            tlogData = pd.read_csv(tlogFolder_ + 'tlog_' + i + '.csv').dropna()
            fingerData = pd.read_csv(fingerFolder_ + 'finger_' + i + '.csv')

        except FileNotFoundError as e:
            print('except:', e)
            continue
        ubs = re.compile(r'(\d+)_(\d+)_(\d+)')
        current_user = ubs.match(i).group(1)
        current_block = ubs.match(i).group(2)
        current_sentence = ubs.match(i).group(3)
        print(current_sentence)
        if current_user not in generalDict:
            generalDict[current_user] = {}
        if current_block not in generalDict[current_user]:
            generalDict[current_user][current_block] = {}
        if current_sentence not in generalDict[current_user][current_block]:
            generalDict[current_user][current_block][current_sentence] = {}            
            generalDict[current_user][current_block][current_sentence]['systemtime'] = []
            generalDict[current_user][current_block][current_sentence]['wordtime'] = []
            generalDict[current_user][current_block][current_sentence]['key'] = []
            generalDict[current_user][current_block][current_sentence]['x'] = []
            generalDict[current_user][current_block][current_sentence]['y'] = []
            generalDict[current_user][current_block][current_sentence]['xf'] = []
            generalDict[current_user][current_block][current_sentence]['yf'] = []
            generalDict[current_user][current_block][current_sentence]['t'] = []
        lastActionItem = next(fingerData.iterrows()); lastTlogItem = next(tlogData.iterrows())

        for j in tlogData.iterrows():
            if len(j[1]['message']) == 1:
                if kb.key2xy(j[1]['message']) == False: continue
                generalDict[current_user][current_block][current_sentence]['systemtime'].append(j[1]['systemtime'])
                generalDict[current_user][current_block][current_sentence]['wordtime'].append(j[1]['wordtime'] + timeDeviation)
                generalDict[current_user][current_block][current_sentence]['key'].append(j[1]['message'])
                generalDict[current_user][current_block][current_sentence]['x'].append([kb.key2xy(j[1]['message'])[0]])
                generalDict[current_user][current_block][current_sentence]['y'].append([kb.key2xy(j[1]['message'])[1]])
                generalDict[current_user][current_block][current_sentence]['xf'].append([kb.key2xy(j[1]['message'])[0]])
                generalDict[current_user][current_block][current_sentence]['yf'].append([kb.key2xy(j[1]['message'])[1]])
                generalDict[current_user][current_block][current_sentence]['t'].append([j[1]['wordtime'] + timeDeviation])
            if len(j[1]['message']) > 1:
                v = compareChar(j[1]['message'], lastTlogItem[1]['message'])
                if v != 0:
                    if v == 1 and mark == 0:
                        keyPair = j[1]['message'][-2:]; key = j[1]['message'][-1:]
                    if v == 1 and mark != 0:
                        keyPair = '<' + j[1]['message'][-1:]; key = j[1]['message'][-1:]; mark = 0
                    if v == -1:
                        keyPair = lastTlogItem[1]['message'][-1:] + '<'; key = '<' 
                        mark += 1
                        if mark > 1:
                            keyPair = '<<'; key = '<'
                    if kb.key2xy(keyPair[0]) == False or kb.key2xy(keyPair[1]) == False: continue
                    generalDict[current_user][current_block][current_sentence]['systemtime'].append(j[1]['systemtime'])
                    generalDict[current_user][current_block][current_sentence]['wordtime'].append(j[1]['wordtime'] + timeDeviation)
                    generalDict[current_user][current_block][current_sentence]['key'].append(key)
                    lastKey = kb.key2xy(keyPair[0])

                    iterMarker = 0; x = []; y = []; t = []

                    for v, k in enumerate(fingerData.iterrows()):
                        # Fix the exception data in table for first two "if"
                        if type(k[1]['trialtime']) == str:
                            k[1]['trialtime'] = float(k[1]['trialtime'].split('.')[0] +'.000')
                        if type(lastActionItem[1]['trialtime']) == str:
                            lastActionItem[1]['trialtime'] = float(lastActionItem[1]['trialtime'].split('.')[0] +'.000')
                        if k[1]['trialtime'] <= j[1]['wordtime'] + timeDeviation and k[1]['trialtime'] > timeDeviation and k[1]['trialtime'] > lastActionItem[1]['trialtime']:
                            iterMarker = 1
                            t.append(k[1]['trialtime']); x.append(x_cm2pic(k[1]['x'])); y.append(y_cm2pic(k[1]['y']))
                            lastActionItem = k
                        else:
                            if iterMarker != 0:
                                break
                    t.append(j[1]['wordtime'] + timeDeviation); x.append(kb.key2xy(key)[0]); y.append(kb.key2xy(key)[1])
                    generalDict[current_user][current_block][current_sentence]['t'].append(t)
                    generalDict[current_user][current_block][current_sentence]['x'].append(x)
                    generalDict[current_user][current_block][current_sentence]['y'].append(y)
                    
                    xf, yf = dataFixedProcessing(x, y, lastKey)
                    generalDict[current_user][current_block][current_sentence]['xf'].append(xf)
                    generalDict[current_user][current_block][current_sentence]['yf'].append(yf)
                    lastTlogItem = j            
                    print(key)
    with open(os.path.join(pklFolder, "tracingTotalDict.pkl"),"wb") as k:
        pickle.dump(generalDict, k)
    print("End")
    return generalDict
# tracingDict = {"502": {"1": {"7": {
#                                    "systemtime": [],
#                                    "wordtime": [],
#                                    "key": [],
#                                    "x": [],
#                                    "y": [],
#                                    "xf": [],
#                                    "yf": [],
#                                    "t": [],
#                                    }, "15": {...}
#                               }, "2": {...}
#                        }, "503":{...}, ...
#                }

def dataFixedProcessing(x, y, lastKey):
    kw = 130.9/2
    kh = 204/2
    xf = x[:]; yf = y[:]
    xf.insert(0, lastKey[0]); yf.insert(0, lastKey[1])

    l = len(x)
    if l > 4:
        xfd = x[1] - x[0]
        xed = x[-2] - x[-1]
        yfd = y[1] - y[0]
        yed = y[-2] - y[-1]
        if xfd >= kw:
            x1 = xfd - kw
            xf[1] = xf[0] + kw
        elif xfd <= -kw:
            x1 = xfd + kw
            xf[1] = xf[0] - kw
        else:
            x1 = 0
        if xed >= kw:
            x2 = xed - kw
            xf[-2] = xf[-1] + kw
        elif xed <= -kw:
            x2 = xed + kw
            xf[-2] = xf[-1] - kw
        else:
            x2 = 0
        if yfd >= kh:
            y1 = yfd - kh
            yf[1] = yf[0] + kh
        elif yfd <= -kh:
            y1 = yfd + kh
            yf[1] = yf[0] - kh
        else:
            y1 = 0
        if yed >= kh:
            y2 = yed - kh
            yf[-2] = yf[-1] + kh
        elif yed <= -kh:
            y2 = yed + kh
            yf[-2] = yf[-1] - kh
        else:
            y2 = 0
        xf[2:-3] = map(lambda x: (1/(l-4))*(x1-x2) + x, xf[2:-3])
        yf[2:-3] = map(lambda y: (1/(l-4))*(y1-y2) + y, yf[2:-3])                     
    return xf[1:], yf[1:]