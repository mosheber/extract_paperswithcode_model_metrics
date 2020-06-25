from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
from selenium.webdriver.common.action_chains import ActionChains

import os
import sys

url = sys.argv[1]

driver = webdriver.Chrome()
# driver.maximize_window()
files = os.listdir('.')

def go_to_main():
    driver.get(url)
go_to_main()



def get_res_per_model(model_row,dataset_name):
    tds = model_row.find_elements_by_css_selector('td')
    return {
        'rank':tds[0].text,
        'method':tds[1].text,
        'metric':tds[2].text,
        'dataset_name':dataset_name
    }

def get_dataset_file_name(name):
    return name+'.pkl'

def get_models_per_dataset(row_element):
    dataset_elem = row_element.find_element_by_css_selector('div.dataset')
    dataset_name = dataset_elem.text
    if(get_dataset_file_name(dataset_name) in files):
        print('already did {}'.format(dataset_name))
        return []
    print('in {}'.format(dataset_name))
    dataset_elem.click()
    time.sleep(2)
    model_table_rows = driver.find_elements_by_css_selector('.view-sota-table tbody tr')
    models = [get_res_per_model(x,dataset_name) for x in model_table_rows]
    go_to_main()
    time.sleep(2)

    with open(get_dataset_file_name(dataset_name),'wb') as f:
        pickle.dump(models,f)  
    return models
    
    
    
try:

    all_models = []

    dataset_rows = driver.find_elements_by_css_selector(".sota-table-preview tbody tr")
    dataset_rows_len = len(dataset_rows)

    for i in range(dataset_rows_len):
        print(i)
        try:
            time.sleep(2)
            dataset_rows = driver.find_elements_by_css_selector(".sota-table-preview tbody tr")
            cur = dataset_rows[i]
            # actions = ActionChains(driver)
            # actions.move_to_element(cur).perform()
            
            models = get_models_per_dataset(cur)
            all_models.append(models)
      
        except Exception as e:
            print('\t error')
            print(e)
    
    with open('all_models.pkl','wb') as f:
        pickle.dump(all_models,f)
except Exception as e:
    print(e)

driver.close()
