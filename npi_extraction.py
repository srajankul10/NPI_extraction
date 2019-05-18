#import the required packages
import requests
import pandas as pd

def write_fn(first_name,last_name,postal_code,npi,cnt):
    postal_code = str(postal_code).replace(".0","")
    val = first_name + ", " + last_name + ", " + postal_code + ", " + str(npi) + ", " + cnt
    print (val)
    with open('npi_extract.txt','a') as f:
        print ("Writing " + val)
        f.write(val + "\n")
        f.close()

def npi_extraction():
    shape=df.shape
  
  #to replace blank value of input file in dataframe with null
    df.fillna("",inplace=True)
  
  #replace non alphabetic characters in name with blank (col_1 = firstname and col_2 = lastname)
    df['col_1'] = df.['col_1'].apply(lambda x: ''.join([i if 64 < ord(i) < 91 or 96 < ord(i) < 123 else "" for i in x]))
    df['col_1'] = df.['col_1'].apply(lambda x: ''.join([i if 64 < ord(i) < 91 or 96 < ord(i) < 123 else "" for i in x]))
  
    for m in range(0,shape[0]):
        first_name  = df.iat[m,0]
        last_name   = df.iat[m,1]
        postal_code = df.iat[m,2]
    
    #to handle blank postal code
        if postal_code is "": 
            PARAMS = {'first_name':first_name,'last_name':last_name,'postal_code':postal_code}
        else:
            PARAMS = {'first_name':first_name,'last_name':last_name,'postal_code':int(postal_code)}
        print (PARAMS)
    
    #sending get request and saving the response
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        print (data)
        if data['result_count'] == 1:
            npi = data['result_count'][0]['number']
            cnt = data['result_count']
            write_fn(first_name,last_name,postal_code,npi,cnt)
    
        elif data['result_count'] == 0:
            val = first_name + ", " + last_name + ", " + str(postal_code)
            with open("npi_not_found.txt", "a") as f:
                f.write(val + "\n")
                f.close()

        else:
            cnt = data['result_count']
            for i in range(0,cnt):   
                npi = data['result_count'][i]['number']
                write_fn(first_name,last_name,postal_code,npi,cnt)

if __name__ == '__main__':
  #api-endpoint
    URL="https://npiregistry.cms.hhs.gov/api/?version=2.0"
    df = pd.read_csv("npi_data.csv")
  #calling of function to extract npi
    npi_extraction()
