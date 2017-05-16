from selenium import webdriver
import re
import time
import getpass

def initiatedrivers():
    driver = webdriver.Chrome()
    driver.set_window_size(480, 480)
    driver.set_window_position(800, 0)
    return driver

def insta_login(driver):
    uname = input("Username : ")
    paswd = getpass.getpass()
    driver.get("http://instagram.com/accounts/login/")
    uname_html = driver.find_element_by_name("username")
    uname_html.send_keys(uname)
    paswd_html = driver.find_element_by_name("password")
    paswd_html.send_keys(paswd)
    paswd_html.submit()
    return driver

    
def scroll(driver):
    driver.execute_script('window.scrollTo(0,0);')
    time.sleep(3)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(1)


def scroll_with_range(driver,n):
    for i in range(n):
        scroll(driver)
        time.sleep(15)

 
def write_source_to_file(usr_name,driver):
    src_code = driver.page_source
    fob = open('/home/usr/InstaCrawl/source.txt','w')
    fob.write(usr_name+"\n")
    fob.write(src_code)
    fob.close()

def main():
    login = input('Do you want to login? [y/n]\n').upper()
    d = initiatedrivers()
    if login == 'Y':
        d = insta_login(d)

    usr = input('Enter username you want to scrape..\n');
    d.get('http://instagram.com/'+usr)
    
    src_code = d.page_source
    pattern = re.compile('\d+ Posts')
    num = pattern.findall(src_code)[0]
    num = int(num.split(' ')[0])
    '''
    not working since instagram changed its source code
    #num_of_files = re.findall(r'\"media":\s*{"count":\s*\d+',src_code)
    #print(num_of_files)
    #num = int(re.findall(r'\d+',num_of_files[0])[0])
    '''

    print(usr + " has " + str(num) + " pictures! ")

    path_not_exist = True
    if (path.exists('/home/ash-ishh/Programz/python/InstaCrawl/'+usr)):
         pass
       #path_not_exist = False 
    time.sleep(5)

    if(num > 12 and  path_not_exist):
        #button class name is frequently changed by instagram so inpect element to verify it is same.
        #button = d.find_element_by_class_name('_oidfu').click() #click load more
        #button = d.find_element_by_class_name("l8imhp _glz1g").click() #click load more
        #button = d.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/a').click()
        scroll_with_range(d,1) #scrole 1 time
        button = d.find_element_by_link_text("Load more")
        location = button.location
        size = button.size
        x,y = location['x'],location['y']
        height,width = size['height'],size['width']

        action = webdriver.common.action_chains.ActionChains(d)
        action.move_to_element_with_offset(button, width//2, height//2) #add offset since button location is not clickable
        action.click()
        action.perform()

        scroll_with_range(d,num//12) #12 images loads per page 
 
    quit_scroll = 0
    while(quit_scroll != 'q'):
        quit_scroll = input("Enter 'q' if page is fully loaded..else enter how many times you want to scroll..")
        try:
            quit_scroll = int(quit_scroll)
            d.get('http://instagram.com/'+usr)
            d.find_element_by_class_name('_oidfu').click()
            scroll_with_range(d,quit_scroll)
        except:
            pass

    write_source_to_file(usr,d)    

if __name__ == "__main__":
    main()
    print("Done! Now you can excecute InstCrawl.sh to download all the pictures :)")
