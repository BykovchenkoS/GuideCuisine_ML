import requests
#pip install Flask
#pip install requests


def update_recommendation(id_record):
    response = requests.get(f"http://localhost:8080/api/recommendation/update?id={id_record}")
    if response.status_code == 200:
        print(" [x] Java метод успешно выполнен")
    else:
        print(" [x] Произошла ошибка при вызове Java метода")


if __name__ == "__main__":
    update_recommendation()


