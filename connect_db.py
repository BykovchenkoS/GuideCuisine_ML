import json
import mysql.connector


def get_recommendation():
    try:
        cursor = connection.cursor();
        query = """
                    SELECT chat_id, cuisines, types, price FROM cuisinebot.recommendation WHERE companies="-1";
                """
        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            chat_id = result[0]
            cuisines = result[1]
            types = result [2]
            price = result[3]

        return chat_id, cuisines, types, price

    except mysql.connector.Error as error:
        print("Ошибка при работе с базой данных: {}".format(error))


def get_recommendation():
    try:
        cursor = connection.cursor()
        query = """
                    SELECT id, cuisines, types, price FROM cuisinebot.recommendation WHERE companies="-1" LIMIT 1;
                """
        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            id = result[0]
            cuisines = result[1]
            types = result [2]
            price = result[3]

        return id, cuisines, types, price

    except mysql.connector.Error as error:
        print("Ошибка при работе с базой данных: {}".format(error))


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


def insert_similar_ids(record_id, similar_ids):
    try:
        cursor = connection.cursor()
        query = """
                    UPDATE `cuisinebot`.`recommendation`
                    SET  `chosen_company` = %s
                    WHERE (id = %s);
                """
        cursor.execute(query, (similar_ids, record_id))
        connection.commit()
        print("Данные успешно вставлены в chosen_companies.")
    except mysql.connector.Error as error:
        print("Ошибка при вставке данных: {}".format(error))


def insert_similar_ids(record_id, similar_ids):
    try:
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO `cuisinebot`.`recommendation` (`id`, `chosen_company`)
            VALUES (%s, %s);
        """
        cursor.execute(insert_query, (record_id, similar_ids))
        connection.commit()
        print("Данные успешно вставлены в recommendation.")

        cursor.execute("SELECT latitude, longitude FROM `cuisinebot`.`recommendation` WHERE id = %s", (record_id,))
        recommendation_data = cursor.fetchone()
        latitude = recommendation_data[0]
        longitude = recommendation_data[1]

        filter_query = """
            SELECT DISTINCT c.id 
            FROM cuisinebot.companies c
            LEFT JOIN cuisinebot.opening_hours oh ON c.id = oh.id_company
            WHERE c.kid_friendly = 0 
            AND c.pet_friendly = 0 
            AND CURTIME() BETWEEN oh.open_hour AND oh.close_hour 
            AND DAYNAME(CURDATE()) = oh.day 
            AND (
                SELECT 
                    6371 * acos(
                        cos(radians(c.latitude)) * cos(radians(%s)) * cos(radians(%s) - radians(c.longitude)) +
                        sin(radians(c.latitude)) * sin(radians(%s))
                    ) 
                ) < 1;
        """
        cursor.execute(filter_query, (latitude, longitude, latitude))
        filtered_records = cursor.fetchall()

        update_query = """
            UPDATE `cuisinebot`.`recommendation`
            SET `chosen_company` = %s
            WHERE id = %s;
        """
        for row in filtered_records:
            cursor.execute(update_query, (similar_ids, row[0]))

        connection.commit()
        print("Данные успешно вставлены в chosen_companies.")
    except mysql.connector.Error as error:
        print("Ошибка при вставке данных: {}".format(error))


connection = get_connection()

if connection:
    X, y = get_data()
    record_id, user_cuisines, user_types, user_price = get_recommendation()

