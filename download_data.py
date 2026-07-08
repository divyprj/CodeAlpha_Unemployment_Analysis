import os
import requests

DATA_DIR = "data"
FILES = {
    "Unemployment in India.csv": [
        "https://raw.githubusercontent.com/Namanbhansali59/Analyzing-Unemployment-Rates-During-COVID-19/master/Unemployment%20in%20India.csv",
        "https://raw.githubusercontent.com/codewithanirban/CBTCIP/main/Unemployment%20in%20India.csv",
        "https://raw.githubusercontent.com/Yash22222/Oasis-Infobyte-Data-Science-Internship-Tasks/main/Task%202/Unemployment%20in%20India.csv"
    ],
    "Unemployment_Rate_upto_11_2020.csv": [
        "https://raw.githubusercontent.com/Namanbhansali59/Analyzing-Unemployment-Rates-During-COVID-19/master/Unemployment_Rate_upto_11_2020.csv",
        "https://raw.githubusercontent.com/codewithanirban/CBTCIP/main/Unemployment_Rate_upto_11_2020.csv",
        "https://raw.githubusercontent.com/Yash22222/Oasis-Infobyte-Data-Science-Internship-Tasks/main/Task%202/Unemployment_Rate_upto_11_2020.csv"
    ]
}

def download_file(filename, urls):
    os.makedirs(DATA_DIR, exist_ok=True)
    target_path = os.path.join(DATA_DIR, filename)
    
    if os.path.exists(target_path):
        print(f"File {filename} already exists at {target_path}. Skipping download.")
        return True
        
    print(f"Downloading {filename}...")
    for url in urls:
        try:
            print(f"Trying URL: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                with open(target_path, 'wb') as f:
                    f.write(response.content)
                print(f"Successfully downloaded {filename} and saved to {target_path}")
                return True
            else:
                print(f"Failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading from {url}: {e}")
            
    print(f"ERROR: Could not download {filename} from any of the URLs.")
    return False

def main():
    success = True
    for filename, urls in FILES.items():
        if not download_file(filename, urls):
            success = False
            
    if success:
        print("All datasets checked and available.")
    else:
        print("Some datasets could not be retrieved. Please check network connection.")

if __name__ == "__main__":
    main()
