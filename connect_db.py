import json
import mysql.connector


def get_connection():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        return connection

    except FileNotFoundError:
        print("Файл конфигурации не найден.")
        return None
    except mysql.connector.Error as error:
        print("Ошибка при подключении к базе данных: {}".format(error))
        return None


def get_data():
    try:
        cursor = connection.cursor()
        query = """
                    SELECT 
                        c.id, 
                        c.price, 
                        GROUP_CONCAT(DISTINCT ct.id_type SEPARATOR ',') AS id_types,
                        GROUP_CONCAT(DISTINCT cc.id_cuisine SEPARATOR ',') AS id_cuisines
                    FROM 
                        cuisinebot.companies c
                    LEFT JOIN 
                        cuisinebot.companies_cuisine cc ON c.id = cc.id_company
                    LEFT JOIN 
                        cuisinebot.companies_type ct ON c.id = ct.id_company
                    GROUP BY 
                        c.id, c.price
                    HAVING
                        id_types IS NOT NULL AND id_cuisines IS NOT NULL;
                """
        cursor.execute(query)
        results = cursor.fetchall()
        X = []
        y = []
        for result in results:
            X.append([result[0], result[1], result[2], result[3]])
            y.append("label_suitability")
        return X, y

    except mysql.connector.Error as error:
        print("Ошибка при работе с базой данных: {}".format(error))


connection = get_connection()

if connection:
    X, y = get_data()

