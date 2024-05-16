import requests

#pip install Flask
#pip install requests

def update_recommendation():
    
    #The same as postMapping rest controller in java
    response = requests.post("http://localhost:8080/api/recommendation/update")
    if response.status_code == 200:
        print(" [x] Java метод успешно выполнен")
    else:
        print(" [x] Произошла ошибка при вызове Java метода")

if __name__ == "__main__":
    update_recommendation()


