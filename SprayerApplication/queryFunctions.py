def sortByList(list1,list2):
    zipped_lists = zip(list1, list2)
    sorted_pairs = sorted(zipped_lists, reverse=True)

    tuples = zip(*sorted_pairs)
    list1, list2 = [ list(tuple) for tuple in  tuples]
    return list2
def filterQuery(result):
    weeds = []
    last = result[0][0]
    sprayNames =[last]
    sprayPrices = [result[0][2]]
    weedRow =[]
    orderByList =[]
    for row in result:            
        if last==row[0]:
            weedRow.append(row[1])
        else:
            last=row[0]
            weeds.append(weedRow)
            orderByList.append(len(weedRow))
            weedRow=[row[1]]
            sprayNames.append(last)
            sprayPrices.append(row[2])

    weeds.append(weedRow)
    zippedList =list(zip(sprayNames,sprayPrices,weeds))
    orderByList.append(len(weedRow))
    zippedList = sortByList(orderByList,zippedList)
    return zippedList
def main():
    result =[['2 4-d lv 4 winfield united','dandelion',21.00],
    ['2 4-d amine 4 albaugh','bitterweed',31.00],
    ['2 4-d amine 4 albaugh','broomweed',31.00],
    ['2 4-d amine 4 albaugh','dandelion',31.00],
    ['2 4-d amine alligare  llc','bitterweed',20.00],
    ['2 4-d amine alligare  llc','broomweed',20.00],
    ['2 4-d amine alligare  llc','dandelion',20.00],
    ['dagger','dandelion',10.00]]
    zippedList=filterQuery(result=result)
    print(zippedList)

if __name__==("__main__"):
    main()