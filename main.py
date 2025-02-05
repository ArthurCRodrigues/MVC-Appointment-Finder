from locationRetriever import Filter
from datetime import datetime
if __name__ == "__main__":
    while True:
        ans = int(input("Select a day range for your appointment: "))
        if ans > 0:
            break
        print("Please input a valid day range")
    locs = Filter(ans)
    for x in locs.filter():
        print(x,"\n")