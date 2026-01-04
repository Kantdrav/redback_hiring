-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: interviewflow
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assessments`
--

DROP TABLE IF EXISTS `assessments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `interview_id` int DEFAULT NULL,
  `score_numeric` float DEFAULT NULL,
  `score_json` text COLLATE utf8mb4_unicode_ci,
  `feedback_text` text COLLATE utf8mb4_unicode_ci,
  `submitted_by` int DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `interview_id` (`interview_id`),
  KEY `submitted_by` (`submitted_by`),
  CONSTRAINT `assessments_ibfk_1` FOREIGN KEY (`interview_id`) REFERENCES `interviews` (`id`),
  CONSTRAINT `assessments_ibfk_2` FOREIGN KEY (`submitted_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessments`
--

LOCK TABLES `assessments` WRITE;
/*!40000 ALTER TABLE `assessments` DISABLE KEYS */;
INSERT INTO `assessments` VALUES (1,1,10,'{\"total_marks\": 15.0, \"obtained_marks\": 10.0, \"detail\": {\"1\": {\"correct\": true, \"marks_awarded\": 5.0, \"marks_total\": 5.0}, \"2\": {\"correct\": false, \"marks_awarded\": 0.0, \"marks_total\": 5.0}, \"3\": {\"correct\": true, \"marks_awarded\": 5.0, \"marks_total\": 5.0}}}','MCQ Auto-graded',3,'2025-12-22 07:39:34'),(2,2,NULL,'{}','',9,'2025-12-26 08:47:36'),(3,3,20,'{\"total_marks\": 20.0, \"obtained_marks\": 20.0, \"detail\": {\"4\": {\"correct\": true, \"marks_awarded\": 10.0, \"marks_total\": 10.0}, \"5\": {\"correct\": true, \"marks_awarded\": 10.0, \"marks_total\": 10.0}}}','MCQ Auto-graded',9,'2025-12-26 08:50:51'),(4,4,20,'{\"total_marks\": 20.0, \"obtained_marks\": 20.0, \"detail\": {\"4\": {\"correct\": true, \"marks_awarded\": 10.0, \"marks_total\": 10.0}, \"5\": {\"correct\": true, \"marks_awarded\": 10.0, \"marks_total\": 10.0}}}','MCQ Auto-graded',9,'2025-12-27 15:13:34'),(5,5,10,'{\"total_marks\": 15.0, \"obtained_marks\": 10.0, \"detail\": {\"1\": {\"correct\": true, \"marks_awarded\": 5.0, \"marks_total\": 5.0}, \"2\": {\"correct\": false, \"marks_awarded\": 0.0, \"marks_total\": 5.0}, \"3\": {\"correct\": true, \"marks_awarded\": 5.0, \"marks_total\": 5.0}}}','MCQ Auto-graded',9,'2025-12-30 10:51:51'),(6,6,0,'{\"total_marks\": 20.0, \"obtained_marks\": 0.0, \"detail\": {\"4\": {\"correct\": false, \"marks_awarded\": 0.0, \"marks_total\": 10.0}, \"5\": {\"correct\": false, \"marks_awarded\": 0.0, \"marks_total\": 10.0}}}','MCQ Auto-graded',3,'2026-01-02 08:52:11'),(7,7,20,'{\"total_marks\": 30.0, \"obtained_marks\": 20.0, \"detail\": {\"6\": {\"correct\": true, \"marks_awarded\": 10.0, \"marks_total\": 10.0, \"chosen_answer\": 1, \"correct_answer\": 1}, \"7\": {\"correct\": true, \"marks_awarded\": 10.0, \"marks_total\": 10.0, \"chosen_answer\": 0, \"correct_answer\": 0}, \"8\": {\"correct\": false, \"marks_awarded\": 0.0, \"marks_total\": 10.0, \"chosen_answer\": 0, \"correct_answer\": 1}}, \"answers\": {\"6\": 1, \"7\": 0, \"8\": 0}}','PASSED ✓\n\nMCQ Auto-graded',7,'2026-01-02 09:38:57');
/*!40000 ALTER TABLE `assessments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `entity_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `entity_id` int DEFAULT NULL,
  `action` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `payload_json` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
INSERT INTO `audit_logs` VALUES (1,'job',1,'apply',3,'{\"job_title\": \"Data Scientist\"}','2025-12-13 10:49:08'),(2,'interview',1,'assign',7,'{\"candidate_id\": 4, \"round_id\": 1}','2025-12-22 07:27:17'),(3,'job',3,'apply',9,'{\"job_title\": \"Clinical Psychologist\"}','2025-12-26 07:49:06'),(4,'interview',2,'assign',7,'{\"candidate_id\": 6, \"round_id\": 2}','2025-12-26 07:58:46'),(5,'interview',3,'assign',7,'{\"candidate_id\": 6, \"round_id\": 2}','2025-12-26 08:04:51'),(6,'interview',4,'assign',7,'{\"candidate_id\": 6, \"round_id\": 2}','2025-12-26 08:39:04'),(7,'job',1,'apply',9,'{\"job_title\": \"Data Scientist\"}','2025-12-30 10:46:40'),(8,'interview',5,'assign',7,'{\"candidate_id\": 6, \"round_id\": 1}','2025-12-30 10:49:10'),(9,'job',3,'apply',3,'{\"job_title\": \"Clinical Psychologist\"}','2026-01-02 08:50:15'),(10,'job',2,'apply',3,'{\"job_title\": \"IT\"}','2026-01-02 08:50:30'),(11,'interview',6,'assign',7,'{\"candidate_id\": 10, \"round_id\": 2}','2026-01-02 08:51:39'),(12,'interview',7,'assign',7,'{\"candidate_id\": 6, \"round_id\": 3}','2026-01-02 09:03:35'),(13,'interview',7,'grade',7,'{\"score\": 20.0}','2026-01-02 09:36:29'),(14,'interview',7,'grade',7,'{\"score\": 20.0, \"status\": \"passed\"}','2026-01-02 09:38:57');
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidate_test_results`
--

DROP TABLE IF EXISTS `candidate_test_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidate_test_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `interview_schedule_id` int NOT NULL,
  `round_index` int DEFAULT NULL,
  `round_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `language_tested` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `score` float DEFAULT NULL,
  `max_score` float DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `test_data_json` text COLLATE utf8mb4_unicode_ci,
  `submitted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `interview_schedule_id` (`interview_schedule_id`),
  CONSTRAINT `candidate_test_results_ibfk_1` FOREIGN KEY (`interview_schedule_id`) REFERENCES `interview_schedules` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidate_test_results`
--

LOCK TABLES `candidate_test_results` WRITE;
/*!40000 ALTER TABLE `candidate_test_results` DISABLE KEYS */;
/*!40000 ALTER TABLE `candidate_test_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidates`
--

DROP TABLE IF EXISTS `candidates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `resume_path` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `applied_job_id` int DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `match_score` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `experience_years` float DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `applied_job_id` (`applied_job_id`),
  CONSTRAINT `candidates_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `candidates_ibfk_2` FOREIGN KEY (`applied_job_id`) REFERENCES `jobs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidates`
--

LOCK TABLES `candidates` WRITE;
/*!40000 ALTER TABLE `candidates` DISABLE KEYS */;
INSERT INTO `candidates` VALUES (3,8,'Akash','akash@mail.com','123456789','/home/kantdravi/Desktop/redback_it_sol/redback/hire/uploads/resumes/1765948981_Ravi_Kant_Resume.pdf',NULL,'applied',50,'2025-12-17 10:53:01',0),(4,3,'Ravi Kant','ravikant@gmail.com','','/home/kantdravi/Desktop/redback_it_sol/redback/hire/uploads/resumes/1766367432_Ravi_Kant_SDE_Intern_Resume.pdf',1,'applied',80,'2025-12-22 07:07:12',0),(5,9,'Angeline Gifty Joy','angelinekant@gmail.com',NULL,NULL,3,'applied',0,'2025-12-26 07:49:06',0),(6,9,'Angeline Gifty Joy','angelinekant@gmail.com','','/home/kantdravi/Desktop/redback_it_sol/redback/hire/uploads/resumes/1766715985_gift_resume.pdf',NULL,'applied',50,'2025-12-26 07:56:25',0),(7,9,'Angeline Gifty Joy','angelinekant@gmail.com',NULL,NULL,1,'applied',0,'2025-12-30 10:46:40',0),(8,9,'Angeline Gifty Joy','angelinekant@gmail.com','','/home/kantdravi/Desktop/redback_it_sol/redback/hire/uploads/resumes/1767071839_gift_resume.pdf',NULL,'applied',50,'2025-12-30 10:47:20',0),(9,3,'Ravi Kant','ravikant@gmail.com',NULL,NULL,3,'applied',0,'2026-01-02 08:50:15',0),(10,3,'Ravi Kant','ravikant@gmail.com',NULL,NULL,2,'applied',0,'2026-01-02 08:50:30',0);
/*!40000 ALTER TABLE `candidates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview_plans`
--

DROP TABLE IF EXISTS `interview_plans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interview_plans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `round_order_json` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `job_id` (`job_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `interview_plans_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`),
  CONSTRAINT `interview_plans_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview_plans`
--

LOCK TABLES `interview_plans` WRITE;
/*!40000 ALTER TABLE `interview_plans` DISABLE KEYS */;
/*!40000 ALTER TABLE `interview_plans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview_schedules`
--

DROP TABLE IF EXISTS `interview_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interview_schedules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `candidate_id` int NOT NULL,
  `interview_plan_id` int NOT NULL,
  `current_round_index` int DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `invited_at` datetime DEFAULT NULL,
  `started_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `overall_score` float DEFAULT NULL,
  `feedback_json` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `candidate_id` (`candidate_id`),
  KEY `interview_plan_id` (`interview_plan_id`),
  CONSTRAINT `interview_schedules_ibfk_1` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`),
  CONSTRAINT `interview_schedules_ibfk_2` FOREIGN KEY (`interview_plan_id`) REFERENCES `interview_plans` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview_schedules`
--

LOCK TABLES `interview_schedules` WRITE;
/*!40000 ALTER TABLE `interview_schedules` DISABLE KEYS */;
/*!40000 ALTER TABLE `interview_schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interviews`
--

DROP TABLE IF EXISTS `interviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `round_id` int DEFAULT NULL,
  `candidate_id` int DEFAULT NULL,
  `interviewer_id` int DEFAULT NULL,
  `scheduled_at_utc` datetime DEFAULT NULL,
  `duration` int DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `round_id` (`round_id`),
  KEY `candidate_id` (`candidate_id`),
  KEY `interviewer_id` (`interviewer_id`),
  CONSTRAINT `interviews_ibfk_1` FOREIGN KEY (`round_id`) REFERENCES `rounds` (`id`),
  CONSTRAINT `interviews_ibfk_2` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`),
  CONSTRAINT `interviews_ibfk_3` FOREIGN KEY (`interviewer_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interviews`
--

LOCK TABLES `interviews` WRITE;
/*!40000 ALTER TABLE `interviews` DISABLE KEYS */;
INSERT INTO `interviews` VALUES (1,1,4,7,'2025-12-22 13:00:00',30,'completed','2025-12-22 07:27:17'),(2,2,6,7,'2025-12-26 13:31:00',30,'completed','2025-12-26 07:58:46'),(3,2,6,7,'2025-12-26 13:34:00',30,'completed','2025-12-26 08:04:51'),(4,2,6,7,'2025-12-26 14:10:00',30,'completed','2025-12-26 08:39:04'),(5,1,6,7,'2025-12-30 16:20:00',30,'completed','2025-12-30 10:49:10'),(6,2,10,7,'2026-01-02 14:22:00',30,'completed','2026-01-02 08:51:39'),(7,3,6,7,'2026-01-02 14:34:00',30,'completed','2026-01-02 09:03:35');
/*!40000 ALTER TABLE `interviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `dept` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,'Data Scientist','cs','Vellore','Data scientist','open',2,'2025-12-13 10:41:44'),(2,'IT','CS','Vellore','it work','open',6,'2025-12-17 10:47:46'),(3,'Clinical Psychologist','Psychology','Vellore','It is for the support of the staffs and to promote mental health to the company.','open',6,'2025-12-26 07:48:15'),(4,'DevOps','IT','Vellore','DevOps','open',1,'2025-12-27 15:11:49');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mcq_questions`
--

DROP TABLE IF EXISTS `mcq_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mcq_questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `round_id` int DEFAULT NULL,
  `question_text` text COLLATE utf8mb4_unicode_ci,
  `choices_json` text COLLATE utf8mb4_unicode_ci,
  `correct_index` int DEFAULT NULL,
  `marks` float DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `round_id` (`round_id`),
  CONSTRAINT `mcq_questions_ibfk_1` FOREIGN KEY (`round_id`) REFERENCES `rounds` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mcq_questions`
--

LOCK TABLES `mcq_questions` WRITE;
/*!40000 ALTER TABLE `mcq_questions` DISABLE KEYS */;
INSERT INTO `mcq_questions` VALUES (1,1,'What is python ?','[\"Its a programming language\", \"Its a snake\", \"i dont know\", \"None\"]',0,5,'2025-12-16 06:03:41'),(2,1,'What is the full form of the ALU?','[\"Dont know\", \"Arithmetic Logic Unit\", \"All of the above\", \"None\"]',1,5,'2025-12-16 06:04:58'),(3,1,'what is the difference between dictionary and list?','[\"the dictionary is key value pair and the list is collection of items in arry.\", \"i dont know\", \"all the above\", \"None of the above\"]',0,5,'2025-12-17 11:00:02'),(4,2,'Who developed CBT?','[\"Albert Bandura\", \"Arnold Beck\", \"Ravi Kant\", \"None\"]',1,10,'2025-12-26 07:39:51'),(5,2,'Who is the father of Psychodynamic Therapy?','[\"None\", \"Carl Roger\", \"Sigmund Freud\", \"All of the above.\"]',2,10,'2025-12-26 07:43:09'),(6,3,'what is html?','[\"i dont know \", \"hyper text markup language\", \"html\", \"none\"]',1,10,'2026-01-02 09:05:34'),(7,3,'What is 200 response code?','[\"its is when successfully returned.\", \"error\", \"dont know\", \"none\"]',0,10,'2026-01-02 09:06:29'),(8,3,'where html is used ?','[\"it backend technollogy\", \"its frontend technology\", \"i dont know\", \"None of the above\"]',1,10,'2026-01-02 09:07:55');
/*!40000 ALTER TABLE `mcq_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programming_languages`
--

DROP TABLE IF EXISTS `programming_languages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programming_languages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programming_languages`
--

LOCK TABLES `programming_languages` WRITE;
/*!40000 ALTER TABLE `programming_languages` DISABLE KEYS */;
/*!40000 ALTER TABLE `programming_languages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_bank_items`
--

DROP TABLE IF EXISTS `question_bank_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_bank_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bank_id` int NOT NULL,
  `question_text` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `question_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `difficulty` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `choices_json` text COLLATE utf8mb4_unicode_ci,
  `correct_answer` text COLLATE utf8mb4_unicode_ci,
  `time_limit_seconds` int DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bank_id` (`bank_id`),
  CONSTRAINT `question_bank_items_ibfk_1` FOREIGN KEY (`bank_id`) REFERENCES `question_banks` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_bank_items`
--

LOCK TABLES `question_bank_items` WRITE;
/*!40000 ALTER TABLE `question_bank_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `question_bank_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_banks`
--

DROP TABLE IF EXISTS `question_banks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_banks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `language_id` int NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `question_count` int DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `language_id` (`language_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `question_banks_ibfk_1` FOREIGN KEY (`language_id`) REFERENCES `programming_languages` (`id`),
  CONSTRAINT `question_banks_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_banks`
--

LOCK TABLES `question_banks` WRITE;
/*!40000 ALTER TABLE `question_banks` DISABLE KEYS */;
/*!40000 ALTER TABLE `question_banks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `round_templates`
--

DROP TABLE IF EXISTS `round_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `round_templates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `duration_minutes` int DEFAULT NULL,
  `config_json` text COLLATE utf8mb4_unicode_ci,
  `enabled` tinyint(1) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `round_templates_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `round_templates`
--

LOCK TABLES `round_templates` WRITE;
/*!40000 ALTER TABLE `round_templates` DISABLE KEYS */;
/*!40000 ALTER TABLE `round_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rounds`
--

DROP TABLE IF EXISTS `rounds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rounds` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plan_id` int DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration_minutes` int DEFAULT NULL,
  `config_json` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rounds`
--

LOCK TABLES `rounds` WRITE;
/*!40000 ALTER TABLE `rounds` DISABLE KEYS */;
INSERT INTO `rounds` VALUES (1,NULL,0,'Python','mcq',30,'{}','2025-12-16 06:01:14'),(2,NULL,0,'Psychology','mcq',30,'{}','2025-12-26 07:36:54'),(3,NULL,0,'Web Developement ','mcq',30,'{}','2025-12-30 10:50:19');
/*!40000 ALTER TABLE `rounds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scoring_policies`
--

DROP TABLE IF EXISTS `scoring_policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scoring_policies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `policy_json` text COLLATE utf8mb4_unicode_ci,
  `enabled` tinyint(1) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `scoring_policies_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scoring_policies`
--

LOCK TABLES `scoring_policies` WRITE;
/*!40000 ALTER TABLE `scoring_policies` DISABLE KEYS */;
/*!40000 ALTER TABLE `scoring_policies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_impersonations`
--

DROP TABLE IF EXISTS `user_impersonations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_impersonations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int NOT NULL,
  `target_user_id` int NOT NULL,
  `action` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `details_json` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `error_message` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `target_user_id` (`target_user_id`),
  CONSTRAINT `user_impersonations_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_impersonations_ibfk_2` FOREIGN KEY (`target_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_impersonations`
--

LOCK TABLES `user_impersonations` WRITE;
/*!40000 ALTER TABLE `user_impersonations` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_impersonations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin@redback.local','pbkdf2:sha256:600000$DDDl068j2OlJKVsr$e9fbef448a5e3623ab208796d081d616bdc45401177929d39ec47b56a4d63ae3','Redback Administrator','admin',NULL,'2025-12-13 10:23:32','2025-12-13 10:35:15'),(2,'raj_hr@gmail.com','pbkdf2:sha256:600000$6rWPXgNOUW6wgAZ3$7f2de2e24236710a2f59322a0e372c331b9e89338487af612a9295777d134ceb','Raj','hr',NULL,'2025-12-13 10:40:40','2025-12-13 10:40:40'),(3,'ravikant@gmail.com','pbkdf2:sha256:600000$yNooHOnh1PfjARyf$ab4732bdc07d23a5cf877f3ed80f050f80666629f293c41167ed12108535cd8b','Ravi Kant','candidate',NULL,'2025-12-13 10:42:34','2025-12-13 10:42:34'),(4,'indu@redback','pbkdf2:sha256:600000$5flTiAr8O0292tLr$4faa60e87345c36b45227f2e79d26ab5ec80fbbbcffb14300c041e33c3999de9','Indu','interviewer',NULL,'2025-12-13 10:56:01','2025-12-13 10:56:01'),(5,'sweety@mail.com','pbkdf2:sha256:600000$2P6tH62bct50HjJO$2c5c8c57cf99787dafd368d2bd7805d31aea357972f498f66fad0fced8d2c114','Sweety','candidate',NULL,'2025-12-17 09:55:26','2025-12-17 09:55:26'),(6,'hr1@gmail.com','pbkdf2:sha256:600000$Tao7J2rGNKM3vAII$1becf9dc2e3f6790f39d130b6da037bcffaf39fba264e2d216487383df3ee667','hr1','hr',NULL,'2025-12-17 10:46:27','2025-12-17 10:46:27'),(7,'interviewer1@gmail.com','pbkdf2:sha256:600000$OqGaLTG36yumZiJk$ebaf5687f0f69307293637c5f11b1967b9df0e47de4e09dac9f15cda7520b091','Interviewer','interviewer',NULL,'2025-12-17 10:50:23','2025-12-17 10:50:23'),(8,'akash@mail.com','pbkdf2:sha256:600000$mRt3YNHPS0FKBOAZ$5b2a252253961278db17e7af3576f05bf860a352475beb75199b1e863f705b39','Akash','candidate',NULL,'2025-12-17 10:51:49','2025-12-17 10:51:49'),(9,'angelinekant@gmail.com','pbkdf2:sha256:600000$qhFDGeUbIyEcUDeM$75071eb17ecdd55d609b7fb2761cfbabc17a885277ccd927e5161a6e2a37bcb2','Angeline Gifty Joy','candidate',NULL,'2025-12-26 07:44:58','2025-12-26 07:44:58');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `website_visits`
--

DROP TABLE IF EXISTS `website_visits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `website_visits` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `ip_address` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `endpoint` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `method` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status_code` int DEFAULT NULL,
  `response_time_ms` float DEFAULT NULL,
  `visited_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `website_visits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=807 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `website_visits`
--

LOCK TABLES `website_visits` WRITE;
/*!40000 ALTER TABLE `website_visits` DISABLE KEYS */;
INSERT INTO `website_visits` VALUES (1,7,'127.0.0.1','unknown','/','GET',200,42.1703,'2025-12-22 07:49:24'),(2,7,'127.0.0.1','unknown','/jobs/','GET',200,8.66103,'2025-12-22 07:49:26'),(3,NULL,'127.0.0.1','unknown','/logout','GET',302,2.01488,'2025-12-22 07:49:33'),(4,NULL,'127.0.0.1','unknown','/login','GET',200,2.45762,'2025-12-22 07:49:33'),(5,1,'127.0.0.1','unknown','/login','POST',302,133.92,'2025-12-22 07:49:52'),(6,1,'127.0.0.1','unknown','/admin','GET',302,0.104189,'2025-12-22 07:49:52'),(7,1,'127.0.0.1','unknown','/admin/users','GET',200,11.0173,'2025-12-22 07:49:52'),(8,1,'127.0.0.1','unknown','/admin/users/7','GET',200,47.2,'2025-12-22 07:50:27'),(9,1,'127.0.0.1','unknown','/admin/users/6','GET',200,4.21906,'2025-12-22 07:50:40'),(10,1,'127.0.0.1','unknown','/admin/users','GET',200,3.45492,'2025-12-22 07:50:43'),(11,1,'127.0.0.1','unknown','/admin/users/1','GET',200,4.31108,'2025-12-22 07:51:01'),(12,1,'127.0.0.1','unknown','/login','GET',200,2.81477,'2025-12-22 07:51:09'),(13,7,'127.0.0.1','unknown','/login','POST',302,130.342,'2025-12-22 07:51:32'),(14,7,'127.0.0.1','unknown','/','GET',200,2.42901,'2025-12-22 07:51:32'),(15,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,18.1277,'2025-12-22 07:51:34'),(16,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,21.127,'2025-12-22 07:51:41'),(17,7,'127.0.0.1','unknown','/interviewer/candidates/4','GET',200,14.8461,'2025-12-22 07:51:44'),(18,7,'127.0.0.1','unknown','/','GET',200,1.91402,'2025-12-22 07:56:06'),(19,7,'127.0.0.1','unknown','/','GET',200,1.82867,'2025-12-22 07:56:22'),(20,7,'127.0.0.1','unknown','/interviewer/candidates/4/assign-interview','GET',200,9.94062,'2025-12-22 08:06:43'),(21,7,'127.0.0.1','unknown','/interviewer/candidates/3','GET',200,3.78227,'2025-12-22 08:06:50'),(22,7,'127.0.0.1','unknown','/','GET',200,2.48885,'2025-12-22 08:06:53'),(23,7,'127.0.0.1','unknown','/jobs/','GET',200,3.52955,'2025-12-22 08:06:56'),(24,7,'127.0.0.1','unknown','/','GET',200,105.888,'2025-12-26 07:30:42'),(25,7,'127.0.0.1','unknown','/favicon.ico','GET',404,0.190496,'2025-12-26 07:30:43'),(26,NULL,'127.0.0.1','unknown','/logout','GET',302,2.63929,'2025-12-26 07:31:15'),(27,NULL,'127.0.0.1','unknown','/login','GET',200,3.70574,'2025-12-26 07:31:15'),(28,7,'127.0.0.1','unknown','/login','POST',302,183.218,'2025-12-26 07:32:10'),(29,7,'127.0.0.1','unknown','/','GET',200,2.65694,'2025-12-26 07:32:10'),(30,7,'127.0.0.1','unknown','/jobs/','GET',200,18.8084,'2025-12-26 07:32:14'),(31,7,'127.0.0.1','unknown','/jobs/1','GET',200,18.7469,'2025-12-26 07:32:21'),(32,7,'127.0.0.1','unknown','/jobs/','GET',200,4.89616,'2025-12-26 07:32:30'),(33,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,34.0948,'2025-12-26 07:32:38'),(34,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,29.6566,'2025-12-26 07:33:14'),(35,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,5.90777,'2025-12-26 07:33:21'),(36,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,10.4485,'2025-12-26 07:33:23'),(37,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,6.14095,'2025-12-26 07:33:24'),(38,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,19.3639,'2025-12-26 07:33:42'),(39,7,'127.0.0.1','unknown','/interviewer/candidates/3','GET',200,22.2745,'2025-12-26 07:34:00'),(40,7,'127.0.0.1','unknown','/interviewer/candidates/3/assign-interview','GET',200,14.8032,'2025-12-26 07:34:18'),(41,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,11.1396,'2025-12-26 07:34:47'),(42,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,12.3096,'2025-12-26 07:34:59'),(43,7,'127.0.0.1','unknown','/interviews/quiz/create','GET',200,31.9576,'2025-12-26 07:35:05'),(44,7,'127.0.0.1','unknown','/interviews/quiz/create','POST',302,12.2433,'2025-12-26 07:36:54'),(45,7,'127.0.0.1','unknown','/interviews/quiz/2/questions','GET',200,22.2311,'2025-12-26 07:36:54'),(46,7,'127.0.0.1','unknown','/interviews/mcq/2/create','GET',200,30.7248,'2025-12-26 07:37:01'),(47,7,'127.0.0.1','unknown','/interviews/mcq/2/create','POST',302,225.667,'2025-12-26 07:39:51'),(48,7,'127.0.0.1','unknown','/interviews/quiz/2/questions','GET',200,6.26206,'2025-12-26 07:39:51'),(49,7,'127.0.0.1','unknown','/interviews/mcq/2/create','GET',200,5.22876,'2025-12-26 07:39:54'),(50,7,'127.0.0.1','unknown','/interviews/mcq/2/create','POST',302,10.927,'2025-12-26 07:43:09'),(51,7,'127.0.0.1','unknown','/interviews/quiz/2/questions','GET',200,5.17011,'2025-12-26 07:43:09'),(52,NULL,'127.0.0.1','unknown','/logout','GET',302,2.59233,'2025-12-26 07:43:23'),(53,NULL,'127.0.0.1','unknown','/login','GET',200,0.656843,'2025-12-26 07:43:23'),(54,NULL,'127.0.0.1','unknown','/register','GET',200,4.60362,'2025-12-26 07:43:32'),(55,NULL,'127.0.0.1','unknown','/register','POST',302,192.604,'2025-12-26 07:44:58'),(56,NULL,'127.0.0.1','unknown','/login','GET',200,0.499487,'2025-12-26 07:44:58'),(57,9,'127.0.0.1','unknown','/login','POST',302,178.159,'2025-12-26 07:45:18'),(58,9,'127.0.0.1','unknown','/','GET',200,2.96569,'2025-12-26 07:45:18'),(59,9,'127.0.0.1','unknown','/jobs/','GET',200,7.7157,'2025-12-26 07:45:34'),(60,NULL,'127.0.0.1','unknown','/logout','GET',302,2.56848,'2025-12-26 07:45:44'),(61,NULL,'127.0.0.1','unknown','/login','GET',200,0.502825,'2025-12-26 07:45:44'),(62,6,'127.0.0.1','unknown','/login','POST',302,181.266,'2025-12-26 07:46:10'),(63,6,'127.0.0.1','unknown','/','GET',200,2.88725,'2025-12-26 07:46:10'),(64,6,'127.0.0.1','unknown','/jobs/','GET',200,4.37427,'2025-12-26 07:46:12'),(65,6,'127.0.0.1','unknown','/jobs/create','GET',200,5.71728,'2025-12-26 07:46:23'),(66,6,'127.0.0.1','unknown','/jobs/create','POST',302,10.1101,'2025-12-26 07:48:15'),(67,6,'127.0.0.1','unknown','/jobs/','GET',200,4.63891,'2025-12-26 07:48:15'),(68,NULL,'127.0.0.1','unknown','/logout','GET',302,11.3218,'2025-12-26 07:48:31'),(69,NULL,'127.0.0.1','unknown','/login','GET',200,0.616312,'2025-12-26 07:48:32'),(70,9,'127.0.0.1','unknown','/login','POST',302,181.41,'2025-12-26 07:48:51'),(71,9,'127.0.0.1','unknown','/','GET',200,2.949,'2025-12-26 07:48:51'),(72,9,'127.0.0.1','unknown','/jobs/','GET',200,6.75797,'2025-12-26 07:48:56'),(73,9,'127.0.0.1','unknown','/candidate/apply/3','POST',302,32.2626,'2025-12-26 07:49:06'),(74,9,'127.0.0.1','unknown','/candidate/job-board','GET',200,34.7321,'2025-12-26 07:49:06'),(75,9,'127.0.0.1','unknown','/jobs/3','GET',200,6.62541,'2025-12-26 07:49:12'),(76,9,'127.0.0.1','unknown','/jobs/','GET',200,6.42872,'2025-12-26 07:49:33'),(77,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,28.7402,'2025-12-26 07:49:36'),(78,NULL,'127.0.0.1','unknown','/logout','GET',302,2.85053,'2025-12-26 07:49:45'),(79,NULL,'127.0.0.1','unknown','/login','GET',200,0.77033,'2025-12-26 07:49:45'),(80,7,'127.0.0.1','unknown','/login','POST',302,177.369,'2025-12-26 07:50:01'),(81,7,'127.0.0.1','unknown','/','GET',200,3.34144,'2025-12-26 07:50:01'),(82,9,'127.0.0.1','unknown','/login','POST',302,178.842,'2025-12-26 07:56:03'),(83,9,'127.0.0.1','unknown','/','GET',200,3.20864,'2025-12-26 07:56:03'),(84,9,'127.0.0.1','unknown','/rag/upload_resume','GET',200,13.5064,'2025-12-26 07:56:10'),(85,9,'127.0.0.1','unknown','/rag/upload_resume','POST',302,650.911,'2025-12-26 07:56:26'),(86,9,'127.0.0.1','unknown','/rag/resume/6/report','GET',200,31.147,'2025-12-26 07:56:26'),(87,9,'127.0.0.1','unknown','/rag/resume/6/download','GET',302,4.49634,'2025-12-26 07:56:55'),(88,9,'127.0.0.1','unknown','/rag/resume/6/report','GET',200,9.27424,'2025-12-26 07:56:55'),(89,9,'127.0.0.1','unknown','/rag/upload_resume','GET',200,5.01466,'2025-12-26 07:57:02'),(90,NULL,'127.0.0.1','unknown','/logout','GET',302,2.55585,'2025-12-26 07:57:08'),(91,NULL,'127.0.0.1','unknown','/login','GET',200,0.649214,'2025-12-26 07:57:08'),(92,7,'127.0.0.1','unknown','/login','POST',302,184.79,'2025-12-26 07:57:26'),(93,7,'127.0.0.1','unknown','/','GET',200,2.56538,'2025-12-26 07:57:26'),(94,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,9.8691,'2025-12-26 07:57:28'),(95,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,8.32415,'2025-12-26 07:57:33'),(96,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,7.01928,'2025-12-26 07:57:42'),(97,7,'127.0.0.1','unknown','/','GET',200,2.98548,'2025-12-26 07:57:46'),(98,7,'127.0.0.1','unknown','/jobs/','GET',200,5.55611,'2025-12-26 07:57:48'),(99,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,10.0927,'2025-12-26 07:57:52'),(100,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,7.20835,'2025-12-26 07:57:53'),(101,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,6.42943,'2025-12-26 07:57:55'),(102,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','GET',200,6.19388,'2025-12-26 07:58:01'),(103,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','POST',302,27.1623,'2025-12-26 07:58:46'),(104,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,6.62661,'2025-12-26 07:58:46'),(105,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,7.57551,'2025-12-26 07:59:04'),(106,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,6.74295,'2025-12-26 07:59:14'),(107,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','GET',200,5.55873,'2025-12-26 07:59:17'),(108,NULL,'127.0.0.1','unknown','/logout','GET',302,4.06718,'2025-12-26 07:59:26'),(109,NULL,'127.0.0.1','unknown','/login','GET',200,0.541925,'2025-12-26 07:59:26'),(110,9,'127.0.0.1','unknown','/login','POST',302,176.991,'2025-12-26 07:59:48'),(111,9,'127.0.0.1','unknown','/','GET',200,3.09682,'2025-12-26 07:59:48'),(112,9,'127.0.0.1','unknown','/interviews/dashboard','GET',302,2.79951,'2025-12-26 07:59:50'),(113,9,'127.0.0.1','unknown','/jobs/','GET',200,6.08277,'2025-12-26 07:59:50'),(114,9,'127.0.0.1','unknown','/jobs/3','GET',200,6.03843,'2025-12-26 07:59:54'),(115,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,11.3418,'2025-12-26 07:59:56'),(116,9,'127.0.0.1','unknown','/interviews/execute/2','GET',200,21.0714,'2025-12-26 08:00:05'),(117,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,8.75735,'2025-12-26 08:00:15'),(118,9,'127.0.0.1','unknown','/jobs/','GET',200,5.76377,'2025-12-26 08:00:15'),(119,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,11.6663,'2025-12-26 08:00:22'),(120,9,'127.0.0.1','unknown','/interviews/execute/2','GET',200,8.42285,'2025-12-26 08:00:23'),(121,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,6.40702,'2025-12-26 08:00:28'),(122,9,'127.0.0.1','unknown','/jobs/','GET',200,5.56445,'2025-12-26 08:00:28'),(123,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,9.68051,'2025-12-26 08:00:49'),(124,9,'127.0.0.1','unknown','/interviews/execute/2','GET',200,9.62973,'2025-12-26 08:00:51'),(125,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,5.94187,'2025-12-26 08:01:06'),(126,9,'127.0.0.1','unknown','/jobs/','GET',200,6.71721,'2025-12-26 08:01:06'),(127,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,11.5254,'2025-12-26 08:01:10'),(128,9,'127.0.0.1','unknown','/candidate/dashboard','GET',200,24.1542,'2025-12-26 08:01:11'),(129,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,9.69982,'2025-12-26 08:01:14'),(130,9,'127.0.0.1','unknown','/interviews/execute/2','GET',200,8.60143,'2025-12-26 08:01:15'),(131,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,6.01864,'2025-12-26 08:01:19'),(132,9,'127.0.0.1','unknown','/jobs/','GET',200,6.09374,'2025-12-26 08:01:19'),(133,9,'127.0.0.1','unknown','/jobs/3','GET',200,6.68311,'2025-12-26 08:01:29'),(134,9,'127.0.0.1','unknown','/jobs/','GET',200,6.8171,'2025-12-26 08:01:35'),(135,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,12.0564,'2025-12-26 08:01:38'),(136,9,'127.0.0.1','unknown','/interviews/execute/2','GET',200,9.17506,'2025-12-26 08:01:42'),(137,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,6.24418,'2025-12-26 08:02:09'),(138,9,'127.0.0.1','unknown','/jobs/','GET',200,6.15311,'2025-12-26 08:02:09'),(139,9,'127.0.0.1','unknown','/jobs/3','GET',200,6.47783,'2025-12-26 08:02:13'),(140,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,11.9772,'2025-12-26 08:02:18'),(141,9,'127.0.0.1','unknown','/interviews/execute/2','GET',200,8.82864,'2025-12-26 08:02:20'),(142,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,5.51295,'2025-12-26 08:02:29'),(143,9,'127.0.0.1','unknown','/jobs/','GET',200,6.03843,'2025-12-26 08:02:29'),(144,NULL,'127.0.0.1','unknown','/logout','GET',302,2.67482,'2025-12-26 08:02:31'),(145,NULL,'127.0.0.1','unknown','/login','GET',200,0.558376,'2025-12-26 08:02:31'),(146,7,'127.0.0.1','unknown','/login','POST',302,182.363,'2025-12-26 08:02:45'),(147,7,'127.0.0.1','unknown','/','GET',200,2.96807,'2025-12-26 08:02:45'),(148,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,13.0439,'2025-12-26 08:02:46'),(149,7,'127.0.0.1','unknown','/interviews/execute/2','GET',302,3.86834,'2025-12-26 08:02:54'),(150,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,13.4695,'2025-12-26 08:02:54'),(151,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,11.5867,'2025-12-26 08:02:59'),(152,7,'127.0.0.1','unknown','/interviews/execute/2','GET',302,4.68135,'2025-12-26 08:03:02'),(153,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,13.217,'2025-12-26 08:03:02'),(154,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,9.44519,'2025-12-26 08:03:05'),(155,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,6.82473,'2025-12-26 08:03:09'),(156,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,11.1907,'2025-12-26 08:03:15'),(157,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,4.63152,'2025-12-26 08:03:18'),(158,7,'127.0.0.1','unknown','/interviews/quiz/2/questions','GET',200,6.00576,'2025-12-26 08:03:29'),(159,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,4.93813,'2025-12-26 08:03:32'),(160,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,13.0069,'2025-12-26 08:03:33'),(161,7,'127.0.0.1','unknown','/','GET',200,2.87962,'2025-12-26 08:03:39'),(162,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,12.4719,'2025-12-26 08:03:40'),(163,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,6.89602,'2025-12-26 08:03:45'),(164,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,9.05037,'2025-12-26 08:03:48'),(165,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','GET',200,6.40655,'2025-12-26 08:03:50'),(166,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','POST',302,47.8485,'2025-12-26 08:04:51'),(167,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,6.06179,'2025-12-26 08:04:51'),(168,7,'127.0.0.1','unknown','/interviewer/interviews/3','GET',302,4.20666,'2025-12-26 08:05:12'),(169,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,12.805,'2025-12-26 08:05:12'),(170,7,'127.0.0.1','unknown','/interviews/execute/3','GET',302,4.84848,'2025-12-26 08:05:43'),(171,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,13.984,'2025-12-26 08:05:43'),(172,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,12.413,'2025-12-26 08:05:46'),(173,NULL,'127.0.0.1','unknown','/logout','GET',302,2.59399,'2025-12-26 08:05:50'),(174,NULL,'127.0.0.1','unknown','/login','GET',200,0.509024,'2025-12-26 08:05:50'),(175,9,'127.0.0.1','unknown','/login','POST',302,179.331,'2025-12-26 08:06:07'),(176,9,'127.0.0.1','unknown','/','GET',200,3.09873,'2025-12-26 08:06:07'),(177,9,'127.0.0.1','unknown','/interviews/dashboard','GET',302,2.61521,'2025-12-26 08:06:08'),(178,9,'127.0.0.1','unknown','/jobs/','GET',200,5.78952,'2025-12-26 08:06:08'),(179,9,'127.0.0.1','unknown','/jobs/3','GET',200,7.67207,'2025-12-26 08:06:10'),(180,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,9.89652,'2025-12-26 08:06:15'),(181,9,'127.0.0.1','unknown','/interviews/execute/2','GET',200,8.7657,'2025-12-26 08:06:21'),(182,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,5.91707,'2025-12-26 08:06:23'),(183,9,'127.0.0.1','unknown','/jobs/','GET',200,6.39439,'2025-12-26 08:06:23'),(184,9,'127.0.0.1','unknown','/jobs/3','GET',200,5.99766,'2025-12-26 08:06:33'),(185,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,9.87959,'2025-12-26 08:06:36'),(186,9,'127.0.0.1','unknown','/interviews/execute/3','GET',200,8.97288,'2025-12-26 08:06:40'),(187,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,5.64098,'2025-12-26 08:06:42'),(188,9,'127.0.0.1','unknown','/jobs/','GET',200,5.78976,'2025-12-26 08:06:42'),(189,NULL,'127.0.0.1','unknown','/logout','GET',302,3.18694,'2025-12-26 08:06:58'),(190,NULL,'127.0.0.1','unknown','/login','GET',200,0.565767,'2025-12-26 08:06:58'),(191,7,'127.0.0.1','unknown','/login','POST',302,183.343,'2025-12-26 08:07:08'),(192,7,'127.0.0.1','unknown','/','GET',200,2.97832,'2025-12-26 08:07:08'),(193,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,14.905,'2025-12-26 08:07:10'),(194,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,7.47752,'2025-12-26 08:07:15'),(195,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,6.26588,'2025-12-26 08:07:20'),(196,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','GET',200,5.934,'2025-12-26 08:07:23'),(197,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','GET',200,97.5986,'2025-12-26 08:29:07'),(198,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','GET',200,98.9289,'2025-12-26 08:38:16'),(199,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','POST',302,35.8171,'2025-12-26 08:39:04'),(200,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,20.9577,'2025-12-26 08:39:04'),(201,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,26.9973,'2025-12-26 08:46:26'),(202,NULL,'127.0.0.1','unknown','/logout','GET',302,2.53081,'2025-12-26 08:46:37'),(203,NULL,'127.0.0.1','unknown','/login','GET',200,4.06528,'2025-12-26 08:46:37'),(204,NULL,'127.0.0.1','unknown','/login','POST',302,181.49,'2025-12-26 08:46:51'),(205,NULL,'127.0.0.1','unknown','/login','GET',200,0.631809,'2025-12-26 08:46:51'),(206,9,'127.0.0.1','unknown','/login','POST',302,179.905,'2025-12-26 08:47:09'),(207,9,'127.0.0.1','unknown','/','GET',200,7.77388,'2025-12-26 08:47:09'),(208,9,'127.0.0.1','unknown','/interviews/dashboard','GET',302,2.71249,'2025-12-26 08:47:11'),(209,9,'127.0.0.1','unknown','/jobs/','GET',200,22.0628,'2025-12-26 08:47:11'),(210,9,'127.0.0.1','unknown','/jobs/3','GET',200,21.2984,'2025-12-26 08:47:13'),(211,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,32.3436,'2025-12-26 08:47:17'),(212,9,'127.0.0.1','unknown','/interviews/execute/2','GET',200,20.0188,'2025-12-26 08:47:21'),(213,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,9.13835,'2025-12-26 08:47:23'),(214,9,'127.0.0.1','unknown','/jobs/','GET',200,6.27565,'2025-12-26 08:47:23'),(215,9,'127.0.0.1','unknown','/interviews/execute/2','GET',200,8.42929,'2025-12-26 08:47:31'),(216,9,'127.0.0.1','unknown','/interviews/execute/2','POST',302,18.7345,'2025-12-26 08:47:36'),(217,9,'127.0.0.1','unknown','/interviews/dashboard','GET',302,2.45094,'2025-12-26 08:47:36'),(218,9,'127.0.0.1','unknown','/jobs/','GET',200,5.67436,'2025-12-26 08:47:36'),(219,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,10.273,'2025-12-26 08:47:43'),(220,9,'127.0.0.1','unknown','/interviews/execute/3','GET',200,8.67319,'2025-12-26 08:47:45'),(221,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,6.01745,'2025-12-26 08:47:50'),(222,9,'127.0.0.1','unknown','/jobs/','GET',200,5.49245,'2025-12-26 08:47:50'),(223,9,'127.0.0.1','unknown','/interviews/execute/3','GET',200,8.09574,'2025-12-26 08:47:52'),(224,9,'127.0.0.1','unknown','/interviews/mcq/take/2','GET',302,75.063,'2025-12-26 08:50:32'),(225,9,'127.0.0.1','unknown','/jobs/','GET',200,39.1128,'2025-12-26 08:50:32'),(226,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,35.1105,'2025-12-26 08:50:36'),(227,9,'127.0.0.1','unknown','/interviews/execute/3','GET',200,24.1721,'2025-12-26 08:50:38'),(228,9,'127.0.0.1','unknown','/interviews/mcq/take/interview/3','GET',200,12.5489,'2025-12-26 08:50:39'),(229,9,'127.0.0.1','unknown','/interviews/mcq/take/interview/3','POST',302,29.1317,'2025-12-26 08:50:51'),(230,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,10.905,'2025-12-26 08:50:51'),(231,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,10.3095,'2025-12-26 08:51:00'),(232,9,'127.0.0.1','unknown','/interviews/execute/4','GET',200,8.28052,'2025-12-26 08:51:02'),(233,9,'127.0.0.1','unknown','/interviews/mcq/take/interview/4','GET',200,7.43961,'2025-12-26 08:51:04'),(234,NULL,'127.0.0.1','unknown','/logout','GET',302,2.75564,'2025-12-26 08:51:11'),(235,NULL,'127.0.0.1','unknown','/login','GET',200,3.3505,'2025-12-26 08:51:11'),(236,NULL,'127.0.0.1','unknown','/','GET',200,22.3997,'2025-12-27 15:09:15'),(237,NULL,'127.0.0.1','unknown','/favicon.ico','GET',404,0.290155,'2025-12-27 15:09:15'),(238,NULL,'127.0.0.1','unknown','/login','GET',200,3.95179,'2025-12-27 15:09:28'),(239,1,'127.0.0.1','unknown','/login','POST',302,184.458,'2025-12-27 15:09:51'),(240,1,'127.0.0.1','unknown','/admin','GET',302,0.122786,'2025-12-27 15:09:51'),(241,1,'127.0.0.1','unknown','/admin/users','GET',200,17.3931,'2025-12-27 15:09:51'),(242,1,'127.0.0.1','unknown','/admin/users/1','GET',200,52.0043,'2025-12-27 15:09:57'),(243,1,'127.0.0.1','unknown','/admin/users','GET',200,5.12481,'2025-12-27 15:10:01'),(244,1,'127.0.0.1','unknown','/hr/dashboard','GET',403,2.9335,'2025-12-27 15:10:51'),(245,1,'127.0.0.1','unknown','/hr/candidates','GET',403,2.89392,'2025-12-27 15:10:57'),(246,1,'127.0.0.1','unknown','/hr/interview-plans','GET',403,3.00741,'2025-12-27 15:11:02'),(247,1,'127.0.0.1','unknown','/jobs/','GET',200,17.0541,'2025-12-27 15:11:10'),(248,1,'127.0.0.1','unknown','/jobs/create','GET',200,6.87599,'2025-12-27 15:11:13'),(249,1,'127.0.0.1','unknown','/jobs/create','POST',302,11.2922,'2025-12-27 15:11:49'),(250,1,'127.0.0.1','unknown','/jobs/','GET',200,4.63986,'2025-12-27 15:11:49'),(251,1,'127.0.0.1','unknown','/jobs/4','GET',200,16.8915,'2025-12-27 15:12:00'),(252,1,'127.0.0.1','unknown','/jobs/','GET',200,4.77672,'2025-12-27 15:12:03'),(253,1,'127.0.0.1','unknown','/hr/interview-plans','GET',403,2.62451,'2025-12-27 15:12:13'),(254,1,'127.0.0.1','unknown','/interviews/quizzes','GET',200,16.9113,'2025-12-27 15:12:17'),(255,NULL,'127.0.0.1','unknown','/logout','GET',302,3.06058,'2025-12-27 15:12:29'),(256,NULL,'127.0.0.1','unknown','/login','GET',200,0.50354,'2025-12-27 15:12:29'),(257,9,'127.0.0.1','unknown','/login','POST',302,186.424,'2025-12-27 15:12:42'),(258,9,'127.0.0.1','unknown','/','GET',200,2.86269,'2025-12-27 15:12:42'),(259,9,'127.0.0.1','unknown','/jobs/','GET',200,8.1408,'2025-12-27 15:12:48'),(260,9,'127.0.0.1','unknown','/jobs/3','GET',200,8.20208,'2025-12-27 15:12:58'),(261,9,'127.0.0.1','unknown','/jobs/','GET',200,5.48506,'2025-12-27 15:13:05'),(262,9,'127.0.0.1','unknown','/jobs/3','GET',200,6.59442,'2025-12-27 15:13:07'),(263,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,43.0367,'2025-12-27 15:13:10'),(264,9,'127.0.0.1','unknown','/interviews/execute/4','GET',200,23.1411,'2025-12-27 15:13:15'),(265,9,'127.0.0.1','unknown','/interviews/mcq/take/interview/4','GET',200,12.0606,'2025-12-27 15:13:20'),(266,9,'127.0.0.1','unknown','/interviews/mcq/take/interview/4','POST',302,57.6782,'2025-12-27 15:13:34'),(267,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,9.62281,'2025-12-27 15:13:34'),(268,NULL,'127.0.0.1','unknown','/logout','GET',302,2.66552,'2025-12-27 15:13:51'),(269,NULL,'127.0.0.1','unknown','/login','GET',200,0.494003,'2025-12-27 15:13:51'),(270,6,'127.0.0.1','unknown','/login','POST',302,178.807,'2025-12-27 15:38:13'),(271,6,'127.0.0.1','unknown','/','GET',200,3.22223,'2025-12-27 15:38:13'),(272,6,'127.0.0.1','unknown','/jobs/','GET',200,4.30512,'2025-12-27 15:38:16'),(273,6,'127.0.0.1','unknown','/jobs/','GET',200,4.70829,'2025-12-27 15:38:41'),(274,6,'127.0.0.1','unknown','/interviews/dashboard','GET',302,1.7941,'2025-12-27 15:38:44'),(275,6,'127.0.0.1','unknown','/jobs/','GET',200,4.18305,'2025-12-27 15:38:44'),(276,6,'127.0.0.1','unknown','/interviews/dashboard','GET',302,2.563,'2025-12-27 15:38:54'),(277,6,'127.0.0.1','unknown','/jobs/','GET',200,3.86643,'2025-12-27 15:38:54'),(278,6,'127.0.0.1','unknown','/jobs/','GET',200,3.93867,'2025-12-27 15:38:59'),(279,6,'127.0.0.1','unknown','/jobs/1','GET',200,3.81231,'2025-12-27 15:39:01'),(280,NULL,'127.0.0.1','unknown','/','GET',200,21.3892,'2025-12-29 11:19:57'),(281,NULL,'127.0.0.1','unknown','/favicon.ico','GET',404,0.307083,'2025-12-29 11:19:57'),(282,NULL,'127.0.0.1','unknown','/login','GET',200,3.03912,'2025-12-29 11:20:05'),(283,1,'127.0.0.1','unknown','/login','POST',302,187.069,'2025-12-29 11:20:37'),(284,1,'127.0.0.1','unknown','/admin','GET',302,0.112057,'2025-12-29 11:20:37'),(285,1,'127.0.0.1','unknown','/admin/users','GET',200,17.4613,'2025-12-29 11:20:37'),(286,1,'127.0.0.1','unknown','/hr/dashboard','GET',403,2.66266,'2025-12-29 11:21:01'),(287,1,'127.0.0.1','unknown','/hr/interview-plans','GET',403,2.73395,'2025-12-29 11:21:08'),(288,1,'127.0.0.1','unknown','/hr/candidates','GET',403,2.74968,'2025-12-29 11:21:37'),(289,1,'127.0.0.1','unknown','/interviews/quizzes','GET',200,14.4248,'2025-12-29 11:21:44'),(290,1,'127.0.0.1','unknown','/interviews/quiz/1/questions','GET',200,21.4095,'2025-12-29 11:21:47'),(291,1,'127.0.0.1','unknown','/admin/users','GET',200,5.30744,'2025-12-29 11:21:54'),(292,1,'127.0.0.1','unknown','/hr/dashboard','GET',403,2.57802,'2025-12-29 11:21:56'),(293,NULL,'127.0.0.1','unknown','/','GET',200,24.1129,'2025-12-30 09:10:57'),(294,NULL,'127.0.0.1','unknown','/favicon.ico','GET',404,0.206232,'2025-12-30 09:10:57'),(295,NULL,'127.0.0.1','unknown','/login','GET',200,4.3149,'2025-12-30 09:11:06'),(296,1,'127.0.0.1','unknown','/login','POST',302,186.833,'2025-12-30 09:11:21'),(297,1,'127.0.0.1','unknown','/admin','GET',302,0.238895,'2025-12-30 09:11:21'),(298,1,'127.0.0.1','unknown','/admin/users','GET',200,16.6974,'2025-12-30 09:11:21'),(299,1,'127.0.0.1','unknown','/interviews/quizzes','GET',200,16.036,'2025-12-30 09:12:53'),(300,1,'127.0.0.1','unknown','/hr/dashboard','GET',403,2.76661,'2025-12-30 09:12:55'),(301,NULL,'127.0.0.1','unknown','/logout','GET',302,2.66528,'2025-12-30 09:13:05'),(302,NULL,'127.0.0.1','unknown','/login','GET',200,0.518322,'2025-12-30 09:13:05'),(303,6,'127.0.0.1','unknown','/login','POST',302,178.106,'2025-12-30 09:13:25'),(304,6,'127.0.0.1','unknown','/','GET',200,3.20506,'2025-12-30 09:13:25'),(305,6,'127.0.0.1','unknown','/jobs/','GET',200,58.9237,'2025-12-30 09:13:27'),(306,6,'127.0.0.1','unknown','/hr/dashboard','GET',200,49.5191,'2025-12-30 09:20:42'),(307,6,'127.0.0.1','unknown','/hr/jobs','GET',200,33.6955,'2025-12-30 09:20:48'),(308,6,'127.0.0.1','unknown','/hr/interview-plans','GET',200,12.8,'2025-12-30 09:20:54'),(309,6,'127.0.0.1','unknown','/hr/candidates','GET',200,18.6656,'2025-12-30 09:21:11'),(310,6,'127.0.0.1','unknown','/hr/jobs','GET',200,4.87471,'2025-12-30 09:21:20'),(311,6,'127.0.0.1','unknown','/interviews/quizzes','GET',200,12.6147,'2025-12-30 09:21:25'),(312,6,'127.0.0.1','unknown','/jobs/','GET',200,15.753,'2025-12-30 09:21:29'),(313,6,'127.0.0.1','unknown','/hr/dashboard','GET',200,9.1269,'2025-12-30 09:21:34'),(314,NULL,'127.0.0.1','unknown','/logout','GET',302,2.52938,'2025-12-30 09:21:41'),(315,NULL,'127.0.0.1','unknown','/login','GET',200,3.39031,'2025-12-30 09:21:41'),(316,7,'127.0.0.1','unknown','/login','POST',302,184.11,'2025-12-30 09:22:48'),(317,7,'127.0.0.1','unknown','/','GET',200,7.57027,'2025-12-30 09:22:48'),(318,7,'127.0.0.1','unknown','/jobs/','GET',200,4.50397,'2025-12-30 09:22:52'),(319,7,'127.0.0.1','unknown','/jobs/1','GET',200,18.9593,'2025-12-30 09:22:55'),(320,7,'127.0.0.1','unknown','/jobs/','GET',200,4.65846,'2025-12-30 09:22:57'),(321,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,3.49545,'2025-12-30 09:22:58'),(322,7,'127.0.0.1','unknown','/jobs/1','GET',200,3.74293,'2025-12-30 09:23:05'),(323,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,31.6939,'2025-12-30 09:23:12'),(324,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,20.8912,'2025-12-30 09:23:15'),(325,NULL,'127.0.0.1','unknown','/logout','GET',302,2.85816,'2025-12-30 10:44:34'),(326,NULL,'127.0.0.1','unknown','/login','GET',200,0.425339,'2025-12-30 10:44:34'),(327,7,'127.0.0.1','unknown','/login','POST',302,288.656,'2025-12-30 10:44:54'),(328,7,'127.0.0.1','unknown','/','GET',200,3.16381,'2025-12-30 10:44:54'),(329,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,18.1177,'2025-12-30 10:45:05'),(330,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,39.4764,'2025-12-30 10:45:23'),(331,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,8.75902,'2025-12-30 10:45:27'),(332,7,'127.0.0.1','unknown','/interviewer/candidates/4','GET',200,28.7235,'2025-12-30 10:45:46'),(333,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,16.1345,'2025-12-30 10:46:09'),(334,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,16.1436,'2025-12-30 10:46:13'),(335,NULL,'127.0.0.1','unknown','/logout','GET',302,2.68126,'2025-12-30 10:46:19'),(336,NULL,'127.0.0.1','unknown','/login','GET',200,0.495911,'2025-12-30 10:46:19'),(337,9,'127.0.0.1','unknown','/login','POST',302,278.044,'2025-12-30 10:46:29'),(338,9,'127.0.0.1','unknown','/','GET',200,3.09706,'2025-12-30 10:46:29'),(339,9,'127.0.0.1','unknown','/jobs/','GET',200,6.51789,'2025-12-30 10:46:31'),(340,9,'127.0.0.1','unknown','/candidate/apply/1','POST',302,34.0745,'2025-12-30 10:46:40'),(341,9,'127.0.0.1','unknown','/candidate/job-board','GET',200,36.855,'2025-12-30 10:46:40'),(342,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,39.0177,'2025-12-30 10:46:50'),(343,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,14.6141,'2025-12-30 10:46:53'),(344,9,'127.0.0.1','unknown','/candidate/dashboard','GET',200,27.7207,'2025-12-30 10:46:55'),(345,9,'127.0.0.1','unknown','/candidate/my-applications','GET',200,17.9374,'2025-12-30 10:46:57'),(346,9,'127.0.0.1','unknown','/candidate/my-applications','GET',200,10.4308,'2025-12-30 10:47:04'),(347,9,'127.0.0.1','unknown','/rag/upload_resume','GET',200,20.2384,'2025-12-30 10:47:07'),(348,9,'127.0.0.1','unknown','/rag/upload_resume','POST',302,851.668,'2025-12-30 10:47:21'),(349,9,'127.0.0.1','unknown','/rag/resume/8/report','GET',200,36.5884,'2025-12-30 10:47:21'),(350,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,13.6383,'2025-12-30 10:47:32'),(351,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,13.7994,'2025-12-30 10:47:37'),(352,9,'127.0.0.1','unknown','/rag/upload_resume','GET',200,6.52909,'2025-12-30 10:47:38'),(353,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,10.0112,'2025-12-30 10:47:39'),(354,9,'127.0.0.1','unknown','/candidate/dashboard','GET',200,11.4341,'2025-12-30 10:47:42'),(355,9,'127.0.0.1','unknown','/candidate/my-applications','GET',200,10.5331,'2025-12-30 10:47:44'),(356,9,'127.0.0.1','unknown','/rag/upload_resume','GET',200,6.25825,'2025-12-30 10:47:47'),(357,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,15.3785,'2025-12-30 10:47:48'),(358,NULL,'127.0.0.1','unknown','/logout','GET',302,2.93279,'2025-12-30 10:47:51'),(359,NULL,'127.0.0.1','unknown','/login','GET',200,0.598192,'2025-12-30 10:47:51'),(360,7,'127.0.0.1','unknown','/login','POST',302,272.047,'2025-12-30 10:48:00'),(361,7,'127.0.0.1','unknown','/','GET',200,2.17247,'2025-12-30 10:48:00'),(362,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,14.4069,'2025-12-30 10:48:03'),(363,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,10.3979,'2025-12-30 10:48:05'),(364,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,7.43937,'2025-12-30 10:48:10'),(365,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','GET',200,20.7534,'2025-12-30 10:48:17'),(366,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','POST',302,22.6338,'2025-12-30 10:49:10'),(367,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,11.9495,'2025-12-30 10:49:10'),(368,NULL,'127.0.0.1','unknown','/logout','GET',302,3.21746,'2025-12-30 10:49:16'),(369,NULL,'127.0.0.1','unknown','/login','GET',200,0.61059,'2025-12-30 10:49:16'),(370,7,'127.0.0.1','unknown','/login','POST',302,281.999,'2025-12-30 10:49:48'),(371,7,'127.0.0.1','unknown','/','GET',200,3.53336,'2025-12-30 10:49:48'),(372,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,5.31507,'2025-12-30 10:49:50'),(373,7,'127.0.0.1','unknown','/interviews/quiz/create','GET',200,7.42149,'2025-12-30 10:49:54'),(374,7,'127.0.0.1','unknown','/interviews/quiz/create','POST',302,14.4155,'2025-12-30 10:50:19'),(375,7,'127.0.0.1','unknown','/interviews/quiz/3/questions','GET',200,25.8694,'2025-12-30 10:50:19'),(376,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,6.16884,'2025-12-30 10:50:31'),(377,NULL,'127.0.0.1','unknown','/logout','GET',302,2.66886,'2025-12-30 10:50:41'),(378,NULL,'127.0.0.1','unknown','/login','GET',200,0.73123,'2025-12-30 10:50:41'),(379,9,'127.0.0.1','unknown','/login','POST',302,292.893,'2025-12-30 10:50:51'),(380,9,'127.0.0.1','unknown','/','GET',200,2.98738,'2025-12-30 10:50:51'),(381,9,'127.0.0.1','unknown','/interviews/dashboard','GET',302,2.12121,'2025-12-30 10:50:53'),(382,9,'127.0.0.1','unknown','/jobs/','GET',200,4.70638,'2025-12-30 10:50:53'),(383,9,'127.0.0.1','unknown','/','GET',200,3.78728,'2025-12-30 10:50:54'),(384,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,13.9592,'2025-12-30 10:50:58'),(385,9,'127.0.0.1','unknown','/interviews/execute/5','GET',200,19.7361,'2025-12-30 10:51:08'),(386,9,'127.0.0.1','unknown','/interviews/mcq/take/interview/5','GET',200,17.6213,'2025-12-30 10:51:11'),(387,9,'127.0.0.1','unknown','/interviews/mcq/take/interview/5','POST',302,27.6463,'2025-12-30 10:51:51'),(388,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,10.5898,'2025-12-30 10:51:51'),(389,NULL,'127.0.0.1','unknown','/logout','GET',302,3.27039,'2025-12-30 10:52:20'),(390,NULL,'127.0.0.1','unknown','/login','GET',200,0.433922,'2025-12-30 10:52:20'),(391,NULL,'127.0.0.1','unknown','/login','POST',302,276.217,'2025-12-30 10:52:31'),(392,NULL,'127.0.0.1','unknown','/login','GET',200,0.422239,'2025-12-30 10:52:31'),(393,7,'127.0.0.1','unknown','/login','POST',302,281.072,'2025-12-30 10:52:44'),(394,7,'127.0.0.1','unknown','/','GET',200,2.09188,'2025-12-30 10:52:44'),(395,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,17.9689,'2025-12-30 10:52:46'),(396,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,15.5621,'2025-12-30 10:52:49'),(397,7,'127.0.0.1','unknown','/interviewer/interviews/5','GET',302,4.90403,'2025-12-30 10:53:00'),(398,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,10.494,'2025-12-30 10:53:00'),(399,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,6.73604,'2025-12-30 10:53:04'),(400,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,11.7533,'2025-12-30 10:53:05'),(401,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,3.15404,'2025-12-30 10:53:08'),(402,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,17.8521,'2025-12-30 10:53:10'),(403,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,9.70984,'2025-12-30 10:53:14'),(404,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,9.82285,'2025-12-30 10:53:21'),(405,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,17.8139,'2025-12-30 10:53:30'),(406,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,9.43756,'2025-12-30 10:53:36'),(407,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,12.8391,'2025-12-30 10:53:47'),(408,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,11.3683,'2025-12-30 10:53:52'),(409,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,7.97725,'2025-12-30 10:54:02'),(410,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,5.63455,'2025-12-30 10:54:09'),(411,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,15.0397,'2025-12-30 10:54:12'),(412,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,13.3891,'2025-12-30 10:54:15'),(413,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,12.4202,'2025-12-30 10:54:17'),(414,7,'127.0.0.1','unknown','/interviewer/interviews/5','GET',302,5.08642,'2025-12-30 10:54:20'),(415,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,10.231,'2025-12-30 10:54:20'),(416,7,'127.0.0.1','unknown','/','GET',200,53.9396,'2025-12-30 10:59:04'),(417,7,'127.0.0.1','unknown','/favicon.ico','GET',404,0.169039,'2025-12-30 10:59:04'),(418,NULL,'127.0.0.1','unknown','/logout','GET',302,1.55139,'2025-12-30 10:59:08'),(419,NULL,'127.0.0.1','unknown','/login','GET',200,1.6942,'2025-12-30 10:59:08'),(420,6,'127.0.0.1','unknown','/login','POST',302,137.415,'2025-12-30 10:59:44'),(421,6,'127.0.0.1','unknown','/','GET',200,1.8487,'2025-12-30 10:59:44'),(422,6,'127.0.0.1','unknown','/interviews/dashboard','GET',302,1.77979,'2025-12-30 10:59:47'),(423,6,'127.0.0.1','unknown','/jobs/','GET',200,12.9278,'2025-12-30 10:59:47'),(424,6,'127.0.0.1','unknown','/hr/dashboard','GET',200,28.5254,'2025-12-30 10:59:52'),(425,6,'127.0.0.1','unknown','/jobs/','GET',200,3.41868,'2025-12-30 11:00:08'),(426,6,'127.0.0.1','unknown','/hr/candidates','GET',200,12.2092,'2025-12-30 11:00:15'),(427,6,'127.0.0.1','unknown','/hr/interview-plans','GET',200,8.98337,'2025-12-30 11:00:23'),(428,6,'127.0.0.1','unknown','/hr/dashboard','GET',200,5.73254,'2025-12-30 11:00:28'),(429,NULL,'127.0.0.1','unknown','/logout','GET',302,1.79029,'2025-12-30 11:00:31'),(430,NULL,'127.0.0.1','unknown','/login','GET',200,0.324726,'2025-12-30 11:00:31'),(431,7,'127.0.0.1','unknown','/login','POST',302,136.284,'2025-12-30 11:00:41'),(432,7,'127.0.0.1','unknown','/','GET',200,1.6737,'2025-12-30 11:00:41'),(433,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,26.6693,'2025-12-30 11:00:42'),(434,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,15.4257,'2025-12-30 11:00:48'),(435,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,16.0937,'2025-12-30 11:00:54'),(436,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,30.0372,'2025-12-30 11:01:23'),(437,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,8.53586,'2025-12-30 11:01:25'),(438,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,3.48902,'2025-12-30 11:01:27'),(439,7,'127.0.0.1','unknown','/rag/upload_resume','GET',200,9.09042,'2025-12-30 11:01:30'),(440,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,8.54635,'2025-12-30 11:01:31'),(441,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,19.5937,'2025-12-30 11:01:35'),(442,7,'127.0.0.1','unknown','/interviewer/interviews/5','GET',302,3.2959,'2025-12-30 11:02:19'),(443,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,7.17115,'2025-12-30 11:02:19'),(444,NULL,'127.0.0.1','unknown','/logout','GET',302,5.80835,'2025-12-30 11:02:25'),(445,NULL,'127.0.0.1','unknown','/login','GET',200,0.34523,'2025-12-30 11:02:25'),(446,NULL,'127.0.0.1','unknown','/login','POST',302,135.533,'2025-12-30 11:02:35'),(447,NULL,'127.0.0.1','unknown','/login','GET',200,0.421524,'2025-12-30 11:02:35'),(448,1,'127.0.0.1','unknown','/login','POST',302,134.867,'2025-12-30 11:02:48'),(449,1,'127.0.0.1','unknown','/admin','GET',302,0.0934601,'2025-12-30 11:02:48'),(450,1,'127.0.0.1','unknown','/admin/users','GET',200,10.8781,'2025-12-30 11:02:48'),(451,1,'127.0.0.1','unknown','/hr/candidates','GET',403,1.70994,'2025-12-30 11:03:13'),(452,1,'127.0.0.1','unknown','/hr/interview-plans','GET',403,1.70064,'2025-12-30 11:03:18'),(453,1,'127.0.0.1','unknown','/interviews/quizzes','GET',200,2.96521,'2025-12-30 11:03:21'),(454,1,'127.0.0.1','unknown','/hr/interview-plans','GET',403,1.90926,'2025-12-30 11:03:32'),(455,1,'127.0.0.1','unknown','/hr/dashboard','GET',403,1.62649,'2025-12-30 11:03:39'),(456,1,'127.0.0.1','unknown','/interviews/quizzes','GET',200,2.9397,'2025-12-30 11:03:45'),(457,1,'127.0.0.1','unknown','/admin/users/9','GET',200,23.6931,'2025-12-30 11:04:12'),(458,9,'127.0.0.1','unknown','/login','POST',302,135.316,'2025-12-30 11:05:06'),(459,9,'127.0.0.1','unknown','/','GET',200,1.81246,'2025-12-30 11:05:06'),(460,9,'127.0.0.1','unknown','/interviews/dashboard','GET',302,1.53351,'2025-12-30 11:05:07'),(461,9,'127.0.0.1','unknown','/jobs/','GET',200,4.19617,'2025-12-30 11:05:07'),(462,9,'127.0.0.1','unknown','/jobs/','GET',200,3.98993,'2025-12-30 11:05:11'),(463,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,25.8255,'2025-12-30 11:05:13'),(464,9,'127.0.0.1','unknown','/candidate/dashboard','GET',200,18.2576,'2025-12-30 11:05:17'),(465,9,'127.0.0.1','unknown','/candidate/my-applications','GET',200,8.42214,'2025-12-30 11:05:20'),(466,9,'127.0.0.1','unknown','/candidate/dashboard','GET',200,7.51281,'2025-12-30 11:05:21'),(467,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,7.18474,'2025-12-30 11:05:23'),(468,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,7.35044,'2025-12-30 11:05:58'),(469,9,'127.0.0.1','unknown','/jobs/','GET',200,3.81708,'2025-12-30 11:06:12'),(470,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,7.93505,'2025-12-30 11:06:20'),(471,NULL,'127.0.0.1','unknown','/logout','GET',302,2.14362,'2025-12-30 11:06:23'),(472,NULL,'127.0.0.1','unknown','/login','GET',200,0.353813,'2025-12-30 11:06:23'),(473,7,'127.0.0.1','unknown','/login','POST',302,136.103,'2025-12-30 11:09:25'),(474,7,'127.0.0.1','unknown','/','GET',200,1.8146,'2025-12-30 11:09:25'),(475,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,8.35228,'2025-12-30 11:09:26'),(476,7,'127.0.0.1','unknown','/','GET',200,62.8932,'2026-01-01 06:27:18'),(477,7,'127.0.0.1','unknown','/favicon.ico','GET',404,0.192642,'2026-01-01 06:27:18'),(478,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,30.3574,'2026-01-01 06:27:40'),(479,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,8.08692,'2026-01-01 06:27:54'),(480,NULL,'127.0.0.1','unknown','/logout','GET',302,44.4911,'2026-01-01 06:32:20'),(481,NULL,'127.0.0.1','unknown','/login','GET',200,15.0058,'2026-01-01 06:32:20'),(482,7,'127.0.0.1','unknown','/login','POST',302,134.914,'2026-01-01 06:33:07'),(483,7,'127.0.0.1','unknown','/','GET',200,4.70901,'2026-01-01 06:33:07'),(484,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,21.1711,'2026-01-01 06:33:09'),(485,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,19.4628,'2026-01-01 06:33:15'),(486,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.16917,'2026-01-01 06:33:20'),(487,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,3.79848,'2026-01-01 06:33:22'),(488,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,8.20184,'2026-01-01 06:33:25'),(489,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,8.33321,'2026-01-01 06:33:29'),(490,7,'127.0.0.1','unknown','/jobs/','GET',200,10.6509,'2026-01-01 06:33:32'),(491,7,'127.0.0.1','unknown','/','GET',200,1.98269,'2026-01-01 06:33:35'),(492,7,'127.0.0.1','unknown','/jobs/','GET',200,2.57635,'2026-01-01 06:33:37'),(493,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,2.8944,'2026-01-01 06:33:43'),(494,NULL,'127.0.0.1','unknown','/logout','GET',302,2.08592,'2026-01-01 06:33:45'),(495,NULL,'127.0.0.1','unknown','/login','GET',200,0.328302,'2026-01-01 06:33:45'),(496,9,'127.0.0.1','unknown','/login','POST',302,130.477,'2026-01-01 06:34:03'),(497,9,'127.0.0.1','unknown','/','GET',200,1.73926,'2026-01-01 06:34:03'),(498,9,'127.0.0.1','unknown','/interviews/dashboard','GET',302,1.61886,'2026-01-01 06:34:05'),(499,9,'127.0.0.1','unknown','/jobs/','GET',200,4.06241,'2026-01-01 06:34:05'),(500,9,'127.0.0.1','unknown','/jobs/','GET',200,3.76987,'2026-01-01 06:34:09'),(501,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,24.5016,'2026-01-01 06:34:15'),(502,9,'127.0.0.1','unknown','/candidate/dashboard','GET',200,19.3989,'2026-01-01 06:34:20'),(503,9,'127.0.0.1','unknown','/candidate/my-applications','GET',200,8.59022,'2026-01-01 06:34:23'),(504,NULL,'127.0.0.1','unknown','/logout','GET',302,2.05374,'2026-01-01 06:35:04'),(505,NULL,'127.0.0.1','unknown','/login','GET',200,0.392914,'2026-01-01 06:35:04'),(506,7,'127.0.0.1','unknown','/login','POST',302,133.11,'2026-01-01 06:35:51'),(507,7,'127.0.0.1','unknown','/','GET',200,1.59097,'2026-01-01 06:35:51'),(508,7,'127.0.0.1','unknown','/jobs/','GET',200,2.71749,'2026-01-01 06:35:53'),(509,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,2.90561,'2026-01-01 06:35:56'),(510,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,7.78031,'2026-01-01 06:35:58'),(511,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,17.2417,'2026-01-01 06:36:01'),(512,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,25.0704,'2026-01-01 06:36:09'),(513,7,'127.0.0.1','unknown','/','GET',200,1.99795,'2026-01-01 06:38:39'),(514,NULL,'127.0.0.1','unknown','/logout','GET',302,1.84608,'2026-01-01 06:42:05'),(515,NULL,'127.0.0.1','unknown','/login','GET',200,0.370502,'2026-01-01 06:42:05'),(516,9,'127.0.0.1','unknown','/login','POST',302,129.454,'2026-01-01 06:42:18'),(517,9,'127.0.0.1','unknown','/','GET',200,1.61052,'2026-01-01 06:42:18'),(518,9,'127.0.0.1','unknown','/jobs/','GET',200,3.82423,'2026-01-01 06:42:21'),(519,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,11.4963,'2026-01-01 06:42:23'),(520,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,9.22799,'2026-01-01 06:42:29'),(521,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,24.3585,'2026-01-01 06:57:35'),(522,9,'127.0.0.1','unknown','/','GET',200,1.93787,'2026-01-01 07:03:59'),(523,NULL,'127.0.0.1','unknown','/logout','GET',302,1.69039,'2026-01-01 07:04:04'),(524,NULL,'127.0.0.1','unknown','/login','GET',200,0.416517,'2026-01-01 07:04:04'),(525,NULL,'127.0.0.1','unknown','/','GET',200,11.6198,'2026-01-02 08:49:17'),(526,NULL,'127.0.0.1','unknown','/favicon.ico','GET',404,0.15521,'2026-01-02 08:49:17'),(527,NULL,'127.0.0.1','unknown','/login','GET',200,2.42162,'2026-01-02 08:49:29'),(528,3,'127.0.0.1','unknown','/login','POST',302,138.038,'2026-01-02 08:49:57'),(529,3,'127.0.0.1','unknown','/','GET',200,3.81351,'2026-01-02 08:49:57'),(530,3,'127.0.0.1','unknown','/jobs/','GET',200,18.012,'2026-01-02 08:49:59'),(531,3,'127.0.0.1','unknown','/interviews/dashboard','GET',302,2.12693,'2026-01-02 08:50:02'),(532,3,'127.0.0.1','unknown','/jobs/','GET',200,3.38984,'2026-01-02 08:50:02'),(533,3,'127.0.0.1','unknown','/candidate/interviews','GET',200,36.35,'2026-01-02 08:50:04'),(534,3,'127.0.0.1','unknown','/jobs/','GET',200,3.89647,'2026-01-02 08:50:08'),(535,3,'127.0.0.1','unknown','/candidate/apply/3','POST',302,48.1012,'2026-01-02 08:50:15'),(536,3,'127.0.0.1','unknown','/candidate/job-board','GET',200,21.9696,'2026-01-02 08:50:15'),(537,3,'127.0.0.1','unknown','/candidate/apply/2','POST',302,23.0539,'2026-01-02 08:50:30'),(538,3,'127.0.0.1','unknown','/candidate/job-board','GET',200,4.52685,'2026-01-02 08:50:30'),(539,NULL,'127.0.0.1','unknown','/logout','GET',302,1.56927,'2026-01-02 08:50:38'),(540,NULL,'127.0.0.1','unknown','/login','GET',200,0.324726,'2026-01-02 08:50:38'),(541,7,'127.0.0.1','unknown','/login','POST',302,129.467,'2026-01-02 08:50:50'),(542,7,'127.0.0.1','unknown','/','GET',200,1.66488,'2026-01-02 08:50:50'),(543,7,'127.0.0.1','unknown','/jobs/','GET',200,3.01003,'2026-01-02 08:50:52'),(544,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,18.3949,'2026-01-02 08:50:54'),(545,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,15.2647,'2026-01-02 08:50:56'),(546,7,'127.0.0.1','unknown','/interviewer/candidates/10','GET',200,16.5105,'2026-01-02 08:51:05'),(547,7,'127.0.0.1','unknown','/interviewer/candidates/10/assign-interview','GET',200,10.7234,'2026-01-02 08:51:12'),(548,7,'127.0.0.1','unknown','/interviewer/candidates/10/assign-interview','POST',302,30.6957,'2026-01-02 08:51:39'),(549,7,'127.0.0.1','unknown','/interviewer/candidates/10','GET',200,5.20539,'2026-01-02 08:51:39'),(550,NULL,'127.0.0.1','unknown','/logout','GET',302,1.63627,'2026-01-02 08:51:43'),(551,NULL,'127.0.0.1','unknown','/login','GET',200,0.404119,'2026-01-02 08:51:43'),(552,3,'127.0.0.1','unknown','/login','POST',302,130.065,'2026-01-02 08:51:54'),(553,3,'127.0.0.1','unknown','/','GET',200,1.61791,'2026-01-02 08:51:54'),(554,3,'127.0.0.1','unknown','/interviews/dashboard','GET',302,1.67632,'2026-01-02 08:51:55'),(555,3,'127.0.0.1','unknown','/jobs/','GET',200,3.90053,'2026-01-02 08:51:55'),(556,3,'127.0.0.1','unknown','/candidate/interviews','GET',200,7.60961,'2026-01-02 08:51:58'),(557,3,'127.0.0.1','unknown','/interviews/execute/6','GET',200,22.4683,'2026-01-02 08:52:01'),(558,3,'127.0.0.1','unknown','/interviews/mcq/take/interview/6','GET',200,8.71444,'2026-01-02 08:52:04'),(559,3,'127.0.0.1','unknown','/interviews/mcq/take/interview/6','POST',302,19.4759,'2026-01-02 08:52:11'),(560,3,'127.0.0.1','unknown','/candidate/interviews','GET',200,7.76315,'2026-01-02 08:52:11'),(561,3,'127.0.0.1','unknown','/candidate/dashboard','GET',200,15.1663,'2026-01-02 08:52:17'),(562,3,'127.0.0.1','unknown','/candidate/interviews','GET',200,9.4862,'2026-01-02 08:52:20'),(563,NULL,'127.0.0.1','unknown','/logout','GET',302,3.47996,'2026-01-02 08:52:24'),(564,NULL,'127.0.0.1','unknown','/login','GET',200,0.331879,'2026-01-02 08:52:24'),(565,7,'127.0.0.1','unknown','/login','POST',302,131.829,'2026-01-02 08:52:36'),(566,7,'127.0.0.1','unknown','/','GET',200,2.01654,'2026-01-02 08:52:36'),(567,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,8.77452,'2026-01-02 08:52:37'),(568,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,5.58257,'2026-01-02 08:52:40'),(569,7,'127.0.0.1','unknown','/interviewer/candidates/10','GET',200,6.3107,'2026-01-02 08:52:43'),(570,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,4.94099,'2026-01-02 08:52:54'),(571,7,'127.0.0.1','unknown','/interviewer/candidates/9','GET',200,4.3838,'2026-01-02 08:52:59'),(572,7,'127.0.0.1','unknown','/interviewer/candidates/10','GET',200,5.71156,'2026-01-02 08:53:06'),(573,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,101.249,'2026-01-02 08:53:39'),(574,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,58.0082,'2026-01-02 08:53:39'),(575,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,100.683,'2026-01-02 08:53:39'),(576,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,79.3684,'2026-01-02 08:53:39'),(577,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,7.7486,'2026-01-02 08:53:40'),(578,7,'127.0.0.1','unknown','/','GET',200,4.63843,'2026-01-02 08:53:44'),(579,7,'127.0.0.1','unknown','/jobs/','GET',200,10.1292,'2026-01-02 08:53:46'),(580,7,'127.0.0.1','unknown','/','GET',200,1.96719,'2026-01-02 08:53:47'),(581,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,22.3923,'2026-01-02 08:53:49'),(582,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,20.3629,'2026-01-02 08:53:52'),(583,7,'127.0.0.1','unknown','/interviewer/interviews/6','GET',302,3.31879,'2026-01-02 08:53:56'),(584,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.96327,'2026-01-02 08:53:56'),(585,7,'127.0.0.1','unknown','/interviewer/interviews/6','GET',302,2.64096,'2026-01-02 08:54:00'),(586,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.54421,'2026-01-02 08:54:00'),(587,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,10.205,'2026-01-02 08:54:05'),(588,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,3.4616,'2026-01-02 08:54:10'),(589,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,10.3159,'2026-01-02 08:54:11'),(590,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,3.17049,'2026-01-02 08:54:11'),(591,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,3.23248,'2026-01-02 08:54:13'),(592,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.98933,'2026-01-02 08:54:14'),(593,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.87632,'2026-01-02 08:54:16'),(594,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,3.27563,'2026-01-02 08:54:17'),(595,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,2.99072,'2026-01-02 08:54:18'),(596,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.91876,'2026-01-02 08:54:19'),(597,7,'127.0.0.1','unknown','/interviewer/interviews/6','GET',302,3.67999,'2026-01-02 08:54:31'),(598,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.24308,'2026-01-02 08:54:31'),(599,7,'127.0.0.1','unknown','/interviewer/interviews/5','GET',302,2.50196,'2026-01-02 08:54:33'),(600,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.38272,'2026-01-02 08:54:33'),(601,7,'127.0.0.1','unknown','/interviewer/interviews/5','GET',302,2.8882,'2026-01-02 08:54:34'),(602,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.1768,'2026-01-02 08:54:34'),(603,7,'127.0.0.1','unknown','/interviewer/interviews/5','GET',302,2.43735,'2026-01-02 08:54:34'),(604,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.11362,'2026-01-02 08:54:34'),(605,7,'127.0.0.1','unknown','/interviewer/interviews/5','GET',302,2.98047,'2026-01-02 08:54:34'),(606,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.01873,'2026-01-02 08:54:34'),(607,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,10.7608,'2026-01-02 08:54:36'),(608,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,9.32741,'2026-01-02 08:54:42'),(609,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,5.78856,'2026-01-02 08:54:43'),(610,7,'127.0.0.1','unknown','/interviewer/candidates/10','GET',200,19.9978,'2026-01-02 08:54:59'),(611,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,8.05974,'2026-01-02 08:55:04'),(612,7,'127.0.0.1','unknown','/interviewer/candidates/4','GET',200,6.46448,'2026-01-02 08:55:16'),(613,7,'127.0.0.1','unknown','/interviewer/candidates/4','GET',200,57.5836,'2026-01-02 09:00:06'),(614,7,'127.0.0.1','unknown','/interviewer/candidates/4','GET',200,5.0993,'2026-01-02 09:00:06'),(615,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,15.1372,'2026-01-02 09:00:19'),(616,7,'127.0.0.1','unknown','/interviewer/candidates/10','GET',200,5.85151,'2026-01-02 09:00:23'),(617,7,'127.0.0.1','unknown','/interviewer/candidates/9','GET',200,3.91555,'2026-01-02 09:00:27'),(618,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,4.32062,'2026-01-02 09:00:35'),(619,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,4.98366,'2026-01-02 09:00:38'),(620,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,4.85778,'2026-01-02 09:00:39'),(621,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,4.8604,'2026-01-02 09:00:39'),(622,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,5.17917,'2026-01-02 09:00:39'),(623,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,4.55141,'2026-01-02 09:00:40'),(624,7,'127.0.0.1','unknown','/interviewer/candidates/4','GET',200,81.3916,'2026-01-02 09:00:56'),(625,7,'127.0.0.1','unknown','/interviewer/candidates/5','GET',200,5.39327,'2026-01-02 09:01:07'),(626,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,8.36968,'2026-01-02 09:01:11'),(627,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,13.1378,'2026-01-02 09:02:24'),(628,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,5.48387,'2026-01-02 09:02:26'),(629,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,4.60577,'2026-01-02 09:02:44'),(630,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,8.11529,'2026-01-02 09:02:48'),(631,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','GET',200,10.8593,'2026-01-02 09:03:04'),(632,7,'127.0.0.1','unknown','/interviewer/candidates/6/assign-interview','POST',302,23.149,'2026-01-02 09:03:35'),(633,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,9.66549,'2026-01-02 09:03:36'),(634,NULL,'127.0.0.1','unknown','/logout','GET',302,1.87039,'2026-01-02 09:03:41'),(635,NULL,'127.0.0.1','unknown','/login','GET',200,2.32148,'2026-01-02 09:03:41'),(636,9,'127.0.0.1','unknown','/login','POST',302,133.767,'2026-01-02 09:03:49'),(637,9,'127.0.0.1','unknown','/','GET',200,4.83203,'2026-01-02 09:03:49'),(638,9,'127.0.0.1','unknown','/interviews/dashboard','GET',302,1.84226,'2026-01-02 09:03:51'),(639,9,'127.0.0.1','unknown','/jobs/','GET',200,12.5215,'2026-01-02 09:03:51'),(640,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,28.8889,'2026-01-02 09:03:55'),(641,9,'127.0.0.1','unknown','/interviews/execute/7','GET',200,13.9463,'2026-01-02 09:03:57'),(642,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,11.0884,'2026-01-02 09:04:09'),(643,9,'127.0.0.1','unknown','/interviews/execute/7','GET',200,5.72395,'2026-01-02 09:04:12'),(644,NULL,'127.0.0.1','unknown','/logout','GET',302,1.77813,'2026-01-02 09:04:21'),(645,NULL,'127.0.0.1','unknown','/login','GET',200,0.402451,'2026-01-02 09:04:21'),(646,7,'127.0.0.1','unknown','/login','POST',302,129.879,'2026-01-02 09:04:30'),(647,7,'127.0.0.1','unknown','/','GET',200,2.3644,'2026-01-02 09:04:30'),(648,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,7.38573,'2026-01-02 09:04:32'),(649,7,'127.0.0.1','unknown','/interviews/quiz/3/questions','GET',200,12.7053,'2026-01-02 09:04:35'),(650,7,'127.0.0.1','unknown','/interviews/mcq/3/create','GET',200,6.94251,'2026-01-02 09:04:37'),(651,7,'127.0.0.1','unknown','/interviews/mcq/3/create','POST',302,8.79312,'2026-01-02 09:05:34'),(652,7,'127.0.0.1','unknown','/interviews/quiz/3/questions','GET',200,3.06153,'2026-01-02 09:05:34'),(653,7,'127.0.0.1','unknown','/interviews/mcq/3/create','GET',200,2.92325,'2026-01-02 09:05:36'),(654,7,'127.0.0.1','unknown','/interviews/mcq/3/create','POST',302,8.43596,'2026-01-02 09:06:29'),(655,7,'127.0.0.1','unknown','/interviews/quiz/3/questions','GET',200,3.22247,'2026-01-02 09:06:29'),(656,7,'127.0.0.1','unknown','/interviews/mcq/3/create','GET',200,2.51913,'2026-01-02 09:06:30'),(657,7,'127.0.0.1','unknown','/interviews/mcq/3/create','POST',302,13.2864,'2026-01-02 09:07:55'),(658,7,'127.0.0.1','unknown','/interviews/quiz/3/questions','GET',200,3.44658,'2026-01-02 09:07:55'),(659,NULL,'127.0.0.1','unknown','/logout','GET',302,1.96075,'2026-01-02 09:07:58'),(660,NULL,'127.0.0.1','unknown','/login','GET',200,0.322819,'2026-01-02 09:07:58'),(661,9,'127.0.0.1','unknown','/login','POST',302,135.89,'2026-01-02 09:08:13'),(662,9,'127.0.0.1','unknown','/','GET',200,1.74594,'2026-01-02 09:08:13'),(663,9,'127.0.0.1','unknown','/interviews/dashboard','GET',302,1.92595,'2026-01-02 09:08:14'),(664,9,'127.0.0.1','unknown','/jobs/','GET',200,4.13489,'2026-01-02 09:08:14'),(665,9,'127.0.0.1','unknown','/candidate/interviews','GET',200,11.7934,'2026-01-02 09:08:16'),(666,9,'127.0.0.1','unknown','/interviews/execute/7','GET',200,3.50714,'2026-01-02 09:08:18'),(667,9,'127.0.0.1','unknown','/interviews/mcq/take/interview/7','GET',200,7.81035,'2026-01-02 09:08:20'),(668,9,'127.0.0.1','unknown','/interviews/mcq/take/interview/7','POST',302,20.3919,'2026-01-02 09:08:29'),(669,9,'127.0.0.1','unknown','/interviews/assessment/7/results','GET',200,87.9266,'2026-01-02 09:09:58'),(670,NULL,'127.0.0.1','unknown','/logout','GET',302,1.71781,'2026-01-02 09:10:11'),(671,NULL,'127.0.0.1','unknown','/login','GET',200,2.49815,'2026-01-02 09:10:11'),(672,7,'127.0.0.1','unknown','/login','POST',302,133.117,'2026-01-02 09:10:21'),(673,7,'127.0.0.1','unknown','/','GET',200,4.83632,'2026-01-02 09:10:21'),(674,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,21.235,'2026-01-02 09:10:22'),(675,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,15.4881,'2026-01-02 09:10:23'),(676,7,'127.0.0.1','unknown','/interviewer/candidates/7','GET',200,16.9961,'2026-01-02 09:10:33'),(677,7,'127.0.0.1','unknown','/interviewer/candidates/8','GET',200,3.8929,'2026-01-02 09:10:38'),(678,7,'127.0.0.1','unknown','/interviewer/candidates/5','GET',200,4.57788,'2026-01-02 09:11:07'),(679,7,'127.0.0.1','unknown','/interviewer/candidates/9','GET',200,3.46184,'2026-01-02 09:11:18'),(680,7,'127.0.0.1','unknown','/interviewer/candidates/6','GET',200,12.764,'2026-01-02 09:11:23'),(681,7,'127.0.0.1','unknown','/jobs/','GET',200,10.2262,'2026-01-02 09:13:28'),(682,7,'127.0.0.1','unknown','/','GET',200,1.85561,'2026-01-02 09:13:31'),(683,7,'127.0.0.1','unknown','/jobs/','GET',200,3.45278,'2026-01-02 09:13:45'),(684,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,8.23879,'2026-01-02 09:13:49'),(685,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,10.1054,'2026-01-02 09:13:54'),(686,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,22.9051,'2026-01-02 09:14:01'),(687,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,4.03976,'2026-01-02 09:14:05'),(688,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.67701,'2026-01-02 09:14:07'),(689,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,3.74007,'2026-01-02 09:14:08'),(690,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.28164,'2026-01-02 09:14:10'),(691,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,3.11327,'2026-01-02 09:14:17'),(692,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.14049,'2026-01-02 09:14:17'),(693,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.46379,'2026-01-02 09:14:39'),(694,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.95377,'2026-01-02 09:14:42'),(695,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.37271,'2026-01-02 09:14:42'),(696,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.66072,'2026-01-02 09:14:49'),(697,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,11.0426,'2026-01-02 09:14:49'),(698,7,'127.0.0.1','unknown','/interviews/execute/7','GET',302,2.64215,'2026-01-02 09:14:56'),(699,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,10.0541,'2026-01-02 09:14:56'),(700,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,11.318,'2026-01-02 09:15:03'),(701,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,3.03459,'2026-01-02 09:15:06'),(702,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,3.1476,'2026-01-02 09:15:08'),(703,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,10.1244,'2026-01-02 09:15:09'),(704,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,5.50508,'2026-01-02 09:15:13'),(705,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,10.5529,'2026-01-02 09:15:38'),(706,7,'127.0.0.1','unknown','/interviews/execute/7','GET',302,2.82383,'2026-01-02 09:15:44'),(707,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,14.5946,'2026-01-02 09:15:44'),(708,7,'127.0.0.1','unknown','/interviews/execute/7','GET',302,2.93899,'2026-01-02 09:15:51'),(709,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,10.6943,'2026-01-02 09:15:51'),(710,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,5.88918,'2026-01-02 09:16:21'),(711,7,'127.0.0.1','unknown','/interviewer/candidates/8','GET',200,4.25291,'2026-01-02 09:16:42'),(712,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,5.19896,'2026-01-02 09:16:49'),(713,7,'127.0.0.1','unknown','/interviewer/candidates/8','GET',200,3.58272,'2026-01-02 09:16:53'),(714,7,'127.0.0.1','unknown','/interviewer/candidates/8','GET',200,3.66211,'2026-01-02 09:17:43'),(715,7,'127.0.0.1','unknown','/interviews/quizzes','GET',200,2.88057,'2026-01-02 09:17:46'),(716,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,10.5941,'2026-01-02 09:17:47'),(717,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,10.0932,'2026-01-02 09:17:49'),(718,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,3.35073,'2026-01-02 09:17:52'),(719,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.09257,'2026-01-02 09:17:53'),(720,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.70557,'2026-01-02 09:17:59'),(721,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.31907,'2026-01-02 09:17:59'),(722,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.179768,'2026-01-02 09:19:20'),(723,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,3.19099,'2026-01-02 09:19:28'),(724,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.61471,'2026-01-02 09:19:28'),(725,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.154972,'2026-01-02 09:19:28'),(726,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.88558,'2026-01-02 09:19:35'),(727,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.72986,'2026-01-02 09:19:35'),(728,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.188112,'2026-01-02 09:19:35'),(729,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,3.84402,'2026-01-02 09:19:40'),(730,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.94158,'2026-01-02 09:19:40'),(731,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.162363,'2026-01-02 09:19:40'),(732,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.48575,'2026-01-02 09:19:45'),(733,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.30381,'2026-01-02 09:19:45'),(734,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.180721,'2026-01-02 09:19:45'),(735,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,3.10278,'2026-01-02 09:19:55'),(736,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.182629,'2026-01-02 09:19:55'),(737,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.51076,'2026-01-02 09:19:59'),(738,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.169516,'2026-01-02 09:19:59'),(739,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.54488,'2026-01-02 09:20:02'),(740,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.37183,'2026-01-02 09:20:02'),(741,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.224113,'2026-01-02 09:20:02'),(742,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,47.9066,'2026-01-02 09:21:48'),(743,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,40.7772,'2026-01-02 09:21:48'),(744,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.231266,'2026-01-02 09:21:48'),(745,7,'127.0.0.1','unknown','/interviewer/interviews/5','GET',302,3.40724,'2026-01-02 09:21:56'),(746,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.22847,'2026-01-02 09:21:56'),(747,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.35486,'2026-01-02 09:21:58'),(748,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.07326,'2026-01-02 09:21:58'),(749,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,3.48186,'2026-01-02 09:21:59'),(750,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.12046,'2026-01-02 09:21:59'),(751,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,3.3927,'2026-01-02 09:22:00'),(752,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.51362,'2026-01-02 09:22:00'),(753,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.6896,'2026-01-02 09:22:01'),(754,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.68535,'2026-01-02 09:22:01'),(755,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.89917,'2026-01-02 09:22:04'),(756,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.35388,'2026-01-02 09:22:04'),(757,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,45.5258,'2026-01-02 09:23:42'),(758,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,38.172,'2026-01-02 09:23:42'),(759,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.81549,'2026-01-02 09:23:43'),(760,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.97353,'2026-01-02 09:23:43'),(761,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,46.0014,'2026-01-02 09:23:57'),(762,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,40.7653,'2026-01-02 09:23:57'),(763,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.8069,'2026-01-02 09:23:59'),(764,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.20653,'2026-01-02 09:23:59'),(765,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.45047,'2026-01-02 09:24:00'),(766,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.86202,'2026-01-02 09:24:00'),(767,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.68269,'2026-01-02 09:24:00'),(768,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.63242,'2026-01-02 09:24:00'),(769,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.65908,'2026-01-02 09:24:00'),(770,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.91876,'2026-01-02 09:24:00'),(771,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.70391,'2026-01-02 09:24:00'),(772,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,8.82888,'2026-01-02 09:24:00'),(773,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',302,2.51889,'2026-01-02 09:24:04'),(774,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.26089,'2026-01-02 09:24:04'),(775,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',200,74.348,'2026-01-02 09:24:50'),(776,7,'127.0.0.1','unknown','/interviews/assessment/7/results','GET',302,2.63524,'2026-01-02 09:24:54'),(777,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,22.4953,'2026-01-02 09:24:54'),(778,7,'127.0.0.1','unknown','/interviewer/interviews/7/grade','GET',302,2.80809,'2026-01-02 09:25:10'),(779,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,22.7158,'2026-01-02 09:25:10'),(780,7,'127.0.0.1','unknown','/interviews/assessment/7/results','GET',302,2.80094,'2026-01-02 09:25:22'),(781,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,11.4384,'2026-01-02 09:25:22'),(782,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.15378,'2026-01-02 09:25:31'),(783,7,'127.0.0.1','unknown','/interviews/assessment/7/results','GET',302,3.18885,'2026-01-02 09:25:40'),(784,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,9.77945,'2026-01-02 09:25:40'),(785,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.170469,'2026-01-02 09:25:40'),(786,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,14.5676,'2026-01-02 09:25:49'),(787,7,'127.0.0.1','unknown','/.well-known/appspecific/com.chrome.devtools.json','GET',404,0.195265,'2026-01-02 09:25:49'),(788,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,11.1377,'2026-01-02 09:26:02'),(789,7,'127.0.0.1','unknown','/interviewer/candidates','GET',200,6.38652,'2026-01-02 09:26:03'),(790,7,'127.0.0.1','unknown','/interviews/dashboard','GET',200,10.1271,'2026-01-02 09:26:07'),(791,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.32908,'2026-01-02 09:26:10'),(792,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',200,5.63288,'2026-01-02 09:26:14'),(793,7,'127.0.0.1','unknown','/interviews/assessment/7/results','GET',200,56.9544,'2026-01-02 09:28:32'),(794,7,'127.0.0.1','unknown','/interviewer/interviews/7/grade','GET',302,48.131,'2026-01-02 09:29:33'),(795,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,37.6854,'2026-01-02 09:29:33'),(796,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',200,20.1421,'2026-01-02 09:30:10'),(797,7,'127.0.0.1','unknown','/interviews/assessment/7/results','GET',200,22.6295,'2026-01-02 09:30:14'),(798,7,'127.0.0.1','unknown','/interviewer/interviews/7/grade','GET',302,2.5506,'2026-01-02 09:33:19'),(799,7,'127.0.0.1','unknown','/interviewer/interviews','GET',200,9.39131,'2026-01-02 09:33:19'),(800,7,'127.0.0.1','unknown','/interviewer/interviews/7/grade','GET',200,18.9166,'2026-01-02 09:36:08'),(801,7,'127.0.0.1','unknown','/interviewer/interviews/7/grade','POST',302,20.843,'2026-01-02 09:36:29'),(802,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',200,20.9508,'2026-01-02 09:36:29'),(803,7,'127.0.0.1','unknown','/interviewer/interviews/7/grade','GET',200,5.95927,'2026-01-02 09:36:42'),(804,7,'127.0.0.1','unknown','/interviewer/interviews/7/grade','GET',200,51.657,'2026-01-02 09:38:45'),(805,7,'127.0.0.1','unknown','/interviewer/interviews/7/grade','POST',302,22.7234,'2026-01-02 09:38:57'),(806,7,'127.0.0.1','unknown','/interviewer/interviews/7','GET',200,18.2996,'2026-01-02 09:38:57');
/*!40000 ALTER TABLE `website_visits` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-02 16:20:40
