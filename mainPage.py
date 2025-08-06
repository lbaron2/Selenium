def readSens() -> None:
    #reads in values that are not supposed to be on github through a file called "sensitive.txt", such as website access passwords or API keys
    import os
    global sensitive

    sensitive = {}
    if "sensitive.txt" in os.listdir():
        with open(r"sensitive.txt", "r") as txt:
            for line in txt:
                words = line.strip().split(":")
                sensitive[words[0].upper()] = words[1]
                
def mainWebsiteTest():
    pass

if __name__ == "__main__":
    readSens()
    mainWebsiteTest()