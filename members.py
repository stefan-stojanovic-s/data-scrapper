from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
import sqlite3


class Scrapper():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        self.driver=webdriver.Chrome('chromedriver.exe',options=chrome_options)
    
    def list_urls(self):
        for i in range (18,210):
            yield "https://members.educause.edu/search#?page="+str(i)+"&membershipstatus=Member&country=UNITED%20STATES&membertype=Organization&sortBy=relevance&sortOrder=asc"

    def create_database(self):
        connection=sqlite3.connect('members.db')
        cr=connection.cursor()
        cr.execute("CREATE table members (organisation,link,website,city,state,country,name,job_title1,job_title2)")
        connection.commit()
        connection.close()
    
    def add_to_db(self,data):
        connection=sqlite3.connect('members.db')
        sql="""INSERT INTO members (organisation,link,website,city,state,country,name,job_title1,job_title2) VALUES (?,?,?,?,?,?,?,?,?)"""
        cr=connection.cursor()
        cr.execute(sql,data)
        connection.commit()
        connection.close()

    def export_to_csv(self):
        conn=sqlite3.connect('ali.db')
        df=pd.read_sql_query('SELECT DISTINCT * from members',conn)
        df.to_csv('reports.csv')
        conn.close()
        print("report created")

    def check(self,obj):
        if obj:
            return obj[0].text
        else:
            return ""

    def collect_data(self):
        for url in self.list_urls():
            print(url)
            driver=self.driver
            driver.get(url)
            sleep(4)
            profile_link=list(map(lambda x:x.find_element_by_tag_name("a").get_attribute('href'),driver.find_elements_by_css_selector('li.search-results__item.ng-scope')))
            print(len(profile_link))
            k=0
            for profile in profile_link:
                k+=1
                driver.get(profile)
                sleep(3)
                try:
                    org=driver.find_element_by_class_name("profile__meta-name").text
                    website=self.check(driver.find_elements_by_class_name("profile__meta-title"))
                    location=driver.find_element_by_class_name("profile__meta-location").text
                    city=location.split(',')[0]
                    state=location.split(',')[1].strip()
                    country="UNITED STATES"
                    name=self.check(driver.find_elements_by_class_name('profile-people__fake-h4'))
                    job_titles=driver.find_elements_by_class_name('profile-people__fake-p')
                    #for debugging#
                    
                    print("Job title length is {}".format(len(job_titles)))
                    #----#
                    if len(job_titles) == 1:
                        job_title1=job_titles[0].text
                        job_title2=''
                    elif len(job_titles) == 2:
                        job_title1=job_titles[0].text
                        job_title2=job_titles[1].text
                    elif not job_titles:
                        job_title1=''
                        job_title2=''
        
                    data=(org,profile,website,city,state,country,name,job_title1,job_title2)
                    print("{9}.:\nOrg: {0}\nProfile:{1}\nWebsite:{2}\nCity:{3}\nState:{4}\nCountry:{5}\nName:{6}\nJob1:{7}\nJob2:{8}\n".format(org,profile,website,city,state,country,name,job_title1,job_title2,k))
                    self.add_to_db(data)
                    sleep(2)
                except:
                    print(profile)
                    self.add_to_db(('',profile,'','','','','','',''))

    def collect_boss(self):
        


scrap=Scrapper()
#scrap.create_database()
scrap.collect_data()


