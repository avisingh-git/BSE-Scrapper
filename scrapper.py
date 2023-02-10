import selenium
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
from bs4 import BeautifulSoup

def driver_setup():
    
    options = webdriver.ChromeOptions()

    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.page_load_strategy = 'normal'
    #chrome_driver_binary = "C:/Users/SRSolutions/Desktop/chromedriver.exe"
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    return driver

def remove_tags(html):
 
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
 
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
 
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

def worker(dateIn):
    url="https://bsestarmf.in/RptNavMaster.aspx"
    driver=driver_setup()
    driver.maximize_window()
    time.sleep(2)
    driver.get(url)
    templist = [] 
    i=2
    try:
            driver.execute_script("""
            console.stdlog = console.log.bind(console);
            console.logs = [];
            console.log = function(){
                console.logs.push(Array.from(arguments));
                console.stdlog.apply(console, arguments);
            }
            """)

            time.sleep(2)
            inStr="document.getElementById('txtToDate').value = \""+dateIn+"\";"


            driver.execute_script(inStr)
            time.sleep(1)
            checkAvail=driver.find_element("xpath", '//*[@id="btnSubmit"]')
            checkAvail.click()
            time.sleep(10)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            while(1): 
                    try:
                        
                        NAV_DATE=soup.select("#gvNavDetails > tbody > tr:nth-child("+str(i)+") > td:nth-child(1)")[0].get_text()
            
                        SCHEME_CODE=soup.select("#gvNavDetails > tbody > tr:nth-child("+str(i)+") > td:nth-child(2)")[0].get_text()

                        SCHEME_NAME=soup.select("#gvNavDetails > tbody > tr:nth-child("+str(i)+") > td:nth-child(3)")[0].get_text()

                        RTA_SCHEME_CODE=soup.select("#gvNavDetails > tbody > tr:nth-child("+str(i)+") > td:nth-child(4)")[0].get_text()

                        DIV_REINVESTFLAG=soup.select("#gvNavDetails > tbody > tr:nth-child("+str(i)+") > td:nth-child(5)")[0].get_text()

                        ISIN=soup.select("#gvNavDetails > tbody > tr:nth-child("+str(i)+") > td:nth-child(6)")[0].get_text()

                        NAV_VALUE=soup.select("#gvNavDetails > tbody > tr:nth-child("+str(i)+") > td:nth-child(7)")[0].get_text()

                        RTA_CODE=soup.select("#gvNavDetails > tbody > tr:nth-child("+str(i)+") > td:nth-child(8)")[0].get_text()
                        
                        Table_dict={ 'NAV_DATE': NAV_DATE,
                                    'SCHEME_CODE':SCHEME_CODE,
                                    'SCHEME_NAME':SCHEME_NAME,
                                    'RTA_SCHEME_CODE':RTA_SCHEME_CODE,
                                    'DIV_REINVESTFLAG':DIV_REINVESTFLAG,
                                   'ISIN':ISIN,
                                    'NAV_VALUE':NAV_VALUE,
                                    'RTA_CODE':RTA_CODE}
                        
                        templist.append(Table_dict) 
                        df = pd.DataFrame.from_dict(templist)
                        
                        i+=1
                        df.to_csv(r"C:\Users\SRSolutions\Desktop\scrap\table.csv") #CSV file location
                        driver.quit()                     
                    # if there are no more table data to scrape
                    except Exception as e:
                                        print("Out of scope") 
                                        print(e)
                                        break
    except Exception as e:
        print("Error caught")
        print(e)
dateIn="08-Feb-2023" #same format as the BSE website 
worker(dateIn)
