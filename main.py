from locationRetriever import Filter
from datetime import datetime
if __name__ == "__main__":
    ans = int(input("Select a day range for your appointment: "))
    locs = Filter(ans)
    for x in locs.filter():
        print(x,"\n")