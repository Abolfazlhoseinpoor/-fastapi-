import requests
try:
    response = requests.get("https://wttr.in/Tehran?format=j1",timeout= 10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("time out")
    data = None
except requests.exceptions.HTTPError as e:
    print(f"error http {e}")
    data = None
except requests.exceptions.ConnectionError:
    print("internet vojod nadarad!")
    data = None
except requests.exceptions.RequestException as e:
    print(f"error koli system : {e}")
    data = None    
if data is not None:  
    print("="*30)
    print(f"shoma dar country : {data["nearest_area"][0]["country"][0]["value"]}")
    print(f"shoma dar city : {data["nearest_area"][0]["areaName"][0]["value"]}")
    print(f"rotobat hava : {data["current_condition"][0]["humidity"]}")
    print(f"damaye hava in shahr : {data["current_condition"][0]["temp_C"]}C")
