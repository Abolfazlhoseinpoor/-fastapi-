import requests

response = requests.get("https://wttr.in/Tehran?format=j1", timeout=10)
data = response.json()
print(data.keys())


print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")

print(data["current_condition"][0])

print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")

current = data["current_condition"][0]
print(f"دما: {current['temp_C']}°C")
print(f"وضعیت: {current['weatherDesc'][0]["value"]}")