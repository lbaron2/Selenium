import tests
import setup
import datetime

if __name__ == "__main__":
    
    setup.readSens()
    driver = setup.setup()
    pages = setup.findAllPages(driver)
    
    with open(f"report.md","w+") as output: 

        errorCount = 0
        pageError = 0

        for page in pages:
            driver.get(page)
            priorErrorCount = errorCount

            errorCount += setup.ifError(tests.ifConnects(driver),page,"Connection",output)
            errorCount += setup.ifError(tests.if404(driver),page,"404",output)
            errorCount += setup.ifError(tests.ifMetaDesc(driver),page,"Meta Description",output)

            imgs = tests.findImgs(driver)

            for img in imgs:
                errorCount += setup.ifError(tests.checkIfHasAlt(img),page,f"{img} does not have an alt tag",output)
            
            if(errorCount != priorErrorCount):
                pageError += 1
                print(file=output)
            


        print(f"Out of {len(pages)}, there were {pageError} page(s) with errors a total number of {errorCount} errors across all pages", file=output)


    setup.close(driver)
