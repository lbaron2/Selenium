import tests
import setup
import datetime

def run():
    driver = setup.setup()
    pages = setup.findAllPages(driver)

    time = datetime.datetime.today().strftime("%Y-%m-%d_%I-%M-%S_%p")
    fileName =f"reports/report_{time}.html"
    with open(f"{fileName}","w+") as output: 

        errorCount = 0
        pageError = 0

        for page in pages:
            driver.get(page)
            priorErrorCount = errorCount
            isNewPage = True;            

            print(f"<h2><a src={page}></h2>",end="<br>",file=output)

            # errorCount += setup.ifError(tests.ifConnects(driver),page,"Connection",output)
            # errorCount += setup.ifError(tests.if404(driver),page,"404",output)
            # errorCount += setup.ifError(tests.ifMetaDesc(driver),page,"Meta Description",output)
            imgs = tests.findImgs(driver)

            for img in imgs:
                errorCount += setup.ifError(tests.ifHasAlt(img),page,isNewPage,f"an image without an alt tag <img style= 'width:100px; height:100px;' src={img.get_attribute("src")}><br>",output)

            print(f"<br>", file=output)
            if(setup.errorCountDifferent(errorCount,priorErrorCount)):
                pageError +=1

        print(f"Out of {len(pages)}, there were {pageError} page(s) with errors a total number of {errorCount} errors across all pages",end="<br>", file=output)
        print(f"The seen pages were: {pages}", end="<br>",file=output)
        print(f"This report was done at: {time}", end="<br>",file=output)
        print("<br>", file=output)

    setup.close(driver)
    removeNonErrorPages(fileName)

def removeNonErrorPages(fileName):
    lines = []
    with open(f"{fileName}", "r") as oldFile:
        lines = oldFile.readlines()
    
    with open(f"{fileName}", "w+") as  newFile:        
        for i in range(0, len(lines)):
            currentLine = lines[i]
            if("</h2><br><br>" in currentLine):
                continue
            print(lines[i],file=newFile)

if __name__ == "__main__":
    removeNonErrorPages("reports/report_2026-03-19_09-56-05_AM.html")

            
