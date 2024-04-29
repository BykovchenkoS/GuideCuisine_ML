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
                        MAX(CASE WHEN ct.id_type = 1 THEN 1 ELSE 0 END) AS type_1,
                        MAX(CASE WHEN ct.id_type = 2 THEN 1 ELSE 0 END) AS type_2,
                        MAX(CASE WHEN ct.id_type = 3 THEN 1 ELSE 0 END) AS type_3,
                        MAX(CASE WHEN ct.id_type = 4 THEN 1 ELSE 0 END) AS type_4,
                        MAX(CASE WHEN ct.id_type = 5 THEN 1 ELSE 0 END) AS type_5,
                        MAX(CASE WHEN ct.id_type = 6 THEN 1 ELSE 0 END) AS type_6,
                        MAX(CASE WHEN ct.id_type = 7 THEN 1 ELSE 0 END) AS type_7,
                        MAX(CASE WHEN ct.id_type = 8 THEN 1 ELSE 0 END) AS type_8,
                        MAX(CASE WHEN ct.id_type = 9 THEN 1 ELSE 0 END) AS type_9,
                        MAX(CASE WHEN cc.id_cuisine = 1 THEN 1 ELSE 0 END) AS cuisine_1,
                        MAX(CASE WHEN cc.id_cuisine = 2 THEN 1 ELSE 0 END) AS cuisine_2,
                        MAX(CASE WHEN cc.id_cuisine = 3 THEN 1 ELSE 0 END) AS cuisine_3,
                        MAX(CASE WHEN cc.id_cuisine = 4 THEN 1 ELSE 0 END) AS cuisine_4,
                        MAX(CASE WHEN cc.id_cuisine = 5 THEN 1 ELSE 0 END) AS cuisine_5,
                        MAX(CASE WHEN cc.id_cuisine = 6 THEN 1 ELSE 0 END) AS cuisine_6,
                        MAX(CASE WHEN cc.id_cuisine = 7 THEN 1 ELSE 0 END) AS cuisine_7,
                        MAX(CASE WHEN cc.id_cuisine = 8 THEN 1 ELSE 0 END) AS cuisine_8,
                        MAX(CASE WHEN cc.id_cuisine = 9 THEN 1 ELSE 0 END) AS cuisine_9,
                        MAX(CASE WHEN cc.id_cuisine = 10 THEN 1 ELSE 0 END) AS cuisine_10,
                        MAX(CASE WHEN cc.id_cuisine = 11 THEN 1 ELSE 0 END) AS cuisine_11,
                        MAX(CASE WHEN cc.id_cuisine = 12 THEN 1 ELSE 0 END) AS cuisine_12,
                        MAX(CASE WHEN cc.id_cuisine = 13 THEN 1 ELSE 0 END) AS cuisine_13,
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
            X.append([
                result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7],
                result[8], result[9], result[10], result[11], result[12], result[13], result[14], result[15],
                result[16], result[17], result[18], result[19], result[20], result[21], result[22], result[23]
            ])
            y.append("0")
        return X, y

    except mysql.connector.Error as error:
        print("Ошибка при работе с базой данных: {}".format(error))


connection = get_connection()

if connection:
    X, y = get_data()
    print(X)
