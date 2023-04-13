import mysql.connector


def createTablesInDatabase():
    dbconfig = { 'host': '127.0.0.1',
    'user': 'user',
    'password': 'test',
    'database': 'myDb', }

    #koble til databasen og lager cursor
    connDB = mysql.connector.connect(**dbconfig)
    cursor = connDB.cursor()

    #sjekker om linking_table eksiteres
    cursor.execute("""SHOW TABLES LIKE 'linking_table'""") 
    result = cursor.fetchone() #returnerer none hvis det ikke er en tabell med navn linking_table
    if not result:
        cursor.execute(
            """
            CREATE TABLE `linking_table` (
            `question_id` int(11) NOT NULL,
            `quiz_id` int(11) NOT NULL,
            `option_id` int(11) NOT NULL,
            PRIMARY KEY (`question_id`,`quiz_id`,`option_id`),
            UNIQUE KEY `question_id_UNIQUE` (`question_id`),
            UNIQUE KEY `quiz_id_UNIQUE` (`quiz_id`),
            UNIQUE KEY `option_id_UNIQUE` (`option_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """
        )
    
    #sjekker om answer_options eksisterer
    cursor.execute("""SHOW TABLES LIKE 'answer_options'""") 
    result = cursor.fetchone() #returnerer none hvis det ikke er en tabell med navn answer_options
    if not result:
        cursor.execute(
            """
            CREATE TABLE `answer_options` (
            `option_id` int(11) NOT NULL AUTO_INCREMENT,
            `option_text` varchar(200) NOT NULL,
            PRIMARY KEY (`option_id`),
            CONSTRAINT `fk_options_id` FOREIGN KEY (`option_id`) REFERENCES `linking_table` (`option_id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """
        )


    #sjekker om quiz eksisterer
    cursor.execute("""SHOW TABLES LIKE 'quiz'""") 
    result = cursor.fetchone() #returnerer none hvis det ikke er en tabell med navn quiz
    if not result:
            cursor.execute(
                """
                CREATE TABLE `quiz` (
                `quiz_id` int(11) NOT NULL AUTO_INCREMENT,
                `quiz_name` varchar(45) NOT NULL,
                `quiz_beskrivelse` varchar(45) NOT NULL,
                `antall_questions` int(11) NOT NULL,
                PRIMARY KEY (`quiz_id`),
                CONSTRAINT `fk_quiz_id` FOREIGN KEY (`quiz_id`) REFERENCES `linking_table` (`quiz_id`) ON DELETE CASCADE ON UPDATE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
                """
            )

    #sjekker om question eksisterer
    cursor.execute("""SHOW TABLES LIKE 'question'""") 
    result = cursor.fetchone() #returnerer none hvis det ikke er en tabell med navn question
    if not result:
            cursor.execute(
                """
                CREATE TABLE `question` (
                `question_id` int(11) NOT NULL AUTO_INCREMENT,
                `question_kategori` varchar(45) NOT NULL,
                `question_text` varchar(200) NOT NULL,
                PRIMARY KEY (`question_id`),
                CONSTRAINT `fk_question_id` FOREIGN KEY (`question_id`) REFERENCES `linking_table` (`question_id`) ON DELETE CASCADE ON UPDATE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
                """
            )


    #sjekker om adminUser eksisterer
    cursor.execute("""SHOW TABLES LIKE 'adminUser'""") 
    result = cursor.fetchone() #returnerer none hvis det ikke er en tabell med navn adminUser
    if not result:
            cursor.execute(
                """
                CREATE TABLE `adminUser` (
                `id` int(11) NOT NULL,
                `username` varchar(45) NOT NULL,
                `fornavn` varchar(45) NOT NULL,
                `etternavn` varchar(45) NOT NULL,
                `hashedpassword` varchar(200) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                ALTER TABLE `adminUser`
                ADD PRIMARY KEY (`id`);
                """
            )
    
    #sjekker om user eksisterer
    cursor.execute("""SHOW TABLES LIKE 'user'""") 
    result = cursor.fetchone() #returnerer none hvis det ikke er en tabell med navn user
    if not result:
            cursor.execute(
                """
                CREATE TABLE `user` (
                `id` int(11) NOT NULL,
                `username` varchar(45) NOT NULL,
                `hashedpassword` varchar(200) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                ALTER TABLE `user`
                ADD PRIMARY KEY (`id`);
                """
            )    
    cursor.close()
    connDB.close()













