CREATE TABLE `question` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT,
  `question_kategori` varchar(45) NOT NULL,
  `question_text` varchar(200) NOT NULL,
  PRIMARY KEY (`question_id`),
  CONSTRAINT `fk_question_id` FOREIGN KEY (`question_id`) REFERENCES `linking_table` (`question_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci


CREATE TABLE `quiz` (
  `quiz_id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_name` varchar(45) NOT NULL,
  `quiz_beskrivelse` varchar(45) NOT NULL,
  `antall_questions` int(11) NOT NULL,
  PRIMARY KEY (`quiz_id`),
  CONSTRAINT `fk_quiz_id` FOREIGN KEY (`quiz_id`) REFERENCES `linking_table` (`quiz_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci


CREATE TABLE `answer_options` (
  `option_id` int(11) NOT NULL AUTO_INCREMENT,
  `option_text` varchar(200) NOT NULL,
  PRIMARY KEY (`option_id`),
  CONSTRAINT `fk_options_id` FOREIGN KEY (`option_id`) REFERENCES `linking_table` (`option_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci


CREATE TABLE `linking_table` (
  `question_id` int(11) NOT NULL,
  `quiz_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL,
  PRIMARY KEY (`question_id`,`quiz_id`,`option_id`),
  UNIQUE KEY `question_id_UNIQUE` (`question_id`),
  UNIQUE KEY `quiz_id_UNIQUE` (`quiz_id`),
  UNIQUE KEY `option_id_UNIQUE` (`option_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci