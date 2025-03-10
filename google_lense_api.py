import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import pyperclip
import os
from tqdm import tqdm
import os

from flask import Flask, request
from flask import jsonify

path = r"/usr/bin/chromedriver" 
chrome_options = Options()
chrome_options.add_argument("--headless")


app = Flask(__name__)
 
@app.route('/ocr_it' , methods=['POST'])
def initialization():
    current_dir =  os.getcwd()
    
    image = request.files["image"]
    image_path = os.path.join( current_dir , image.filename )
    image.save( image_path )
    
    try:
        ocr_response = ocr_it( file_path = image_path )
        os.remove( image_path )
        return jsonify( {"result": ocr_response })
    except Exception as e :
        os.remove( image_path )
        print( e )
        return jsonify( {"result":"Could Not OCR IT !"})
    
    
    

def ocr_it( file_path = None ):

        
    ############################## HEADLESS MODE ######################################
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service ,  options=chrome_options )

    ############################## NORMAL MODE ######################################

    # service = Service(executable_path=path)
    # driver = webdriver.Chrome(service=service )

    #################################################################################

    driver.get('https://lens.google.com/')
    # time.sleep(5)


    file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
    file_input.send_keys(file_path)

    time.sleep( 5 )
    div_elements = driver.find_elements(By.XPATH, "//div[@data-ved and @aria-label and not(@tabindex)]" )


    extracted_string = ""
    # Print out each div's attributes
    for div in div_elements:
        try:
            # print("data-ved:", div.get_attribute("data-ved"))
            # print("aria-label:", aria_label )
            # print("-" * 40)

            aria_label = div.get_attribute("aria-label")
            extracted_string += " " + aria_label
        
        except Exception as e:
            print( f"Exception : {e}") 
            print("-" * 40)

    # extracted_string = " ".join( list( set( extracted_string.split() ) ) )
    extracted_string = extracted_string.replace( "মুছে ফেলুন" , "")
    extracted_string = extracted_string.replace( "ভয়েস দ্বারা সার্চ" , "")
    extracted_string = extracted_string.replace( "ছবি দিয়ে সার্চ করুন" , "")
    extracted_string = extracted_string.replace( "আপনি কোন বিষয়ে মতামত দিতে চান তা বেছে নিন" , "")

    driver.close()
     
    return extracted_string




if __name__ == '__main__':
    app.run(host =  "172.17.18.97" , port = "5000" , debug=True)
