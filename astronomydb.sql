CREATE DATABASE  IF NOT EXISTS `railway` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `railway`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: junction.proxy.rlwy.net    Database: railway
-- ------------------------------------------------------
-- Server version	9.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity_logs`
--

DROP TABLE IF EXISTS `activity_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_logs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`),
  KEY `fk_user_logs` (`user_id`),
  CONSTRAINT `fk_user_logs` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_logs`
--

LOCK TABLES `activity_logs` WRITE;
/*!40000 ALTER TABLE `activity_logs` DISABLE KEYS */;
INSERT INTO `activity_logs` VALUES (1,2,'User Logged In','2026-04-13 06:22:42'),(2,8,'User Logged In','2026-04-13 06:23:58'),(3,8,'User Logged In','2026-04-13 06:40:43');
/*!40000 ALTER TABLE `activity_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificates`
--

DROP TABLE IF EXISTS `certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificates` (
  `certificate_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `quiz_id` int DEFAULT NULL,
  `pdf_path` text,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`certificate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificates`
--

LOCK TABLES `certificates` WRITE;
/*!40000 ALTER TABLE `certificates` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `description` text,
  `video_url` text,
  `playlist_url` text,
  `playlist_url1` text,
  `thumbnail` text,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Astronomy for Beginners','Learn stars, galaxies and universe','https://www.youtube.com/embed/videoseries?list=PLbMVogVj5nJROKq6v6sZq74sjty86dAQ2','PLbMVogVj5nJROKq6v6sZq74sjty86dAQ2',NULL,NULL),(2,'Astrophysics and Cosmology','Planets and their motion','https://www.youtube.com/embed/21X5lGlDOfg',NULL,NULL,NULL);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedback_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `message` text,
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leaderboard`
--

DROP TABLE IF EXISTS `leaderboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leaderboard` (
  `leaderboard_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `total_score` int DEFAULT NULL,
  PRIMARY KEY (`leaderboard_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leaderboard`
--

LOCK TABLES `leaderboard` WRITE;
/*!40000 ALTER TABLE `leaderboard` DISABLE KEYS */;
/*!40000 ALTER TABLE `leaderboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lessons`
--

DROP TABLE IF EXISTS `lessons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lessons` (
  `lesson_id` int NOT NULL AUTO_INCREMENT,
  `topic_id` int DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `position` int DEFAULT NULL,
  `video_url` text,
  PRIMARY KEY (`lesson_id`),
  KEY `topic_id` (`topic_id`),
  CONSTRAINT `lessons_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`topic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lessons`
--

LOCK TABLES `lessons` WRITE;
/*!40000 ALTER TABLE `lessons` DISABLE KEYS */;
INSERT INTO `lessons` VALUES (14,NULL,'Lesson 1',1,1,'https://www.youtube.com/embed/sViAwfeMjV0'),(15,NULL,'Lesson 2',1,2,'https://www.youtube.com/embed/0rHUDWjR5gg'),(16,NULL,'Lesson 3',1,3,'https://www.youtube.com/embed/L-Wtlev6suc'),(17,NULL,'Lesson 4',1,4,'https://www.youtube.com/embed/01QWC-rZcfE'),(18,NULL,'Lesson 5',1,5,'https://www.youtube.com/embed/AQ5vty8f9Xc'),(19,NULL,'Lesson 6',1,6,'https://www.youtube.com/embed/PRgua7xceDA'),(20,NULL,'Lesson 7',1,7,'https://www.youtube.com/embed/mYhy7eaazIk'),(21,NULL,'Lesson 8',1,8,'https://www.youtube.com/embed/TRAbZxQHlVw'),(22,NULL,'Lesson 9',1,9,'https://www.youtube.com/embed/KlWpFLfLFBI'),(23,NULL,'Lesson 10',1,10,'https://www.youtube.com/embed/TKM0P3XlMNA'),(24,NULL,'Lesson 11',1,11,'https://www.youtube.com/embed/b22HKFMIfWo'),(25,NULL,'Lesson 12',1,12,'https://www.youtube.com/embed/w-9gDALvMF4'),(26,NULL,'Lesson 13',1,13,'https://www.youtube.com/embed/mCzchPx3yF8'),(27,NULL,'Lesson 14',1,14,'https://www.youtube.com/embed/P3GkZe3nRQ0'),(28,NULL,'Lesson 15',1,15,'https://www.youtube.com/embed/ZFUgy3crCYY'),(29,NULL,'Lesson 16',1,16,'https://www.youtube.com/embed/I-88YWx71gE'),(30,NULL,'Lesson 17',1,17,'https://www.youtube.com/embed/Xwn8fQSW7-8'),(31,NULL,'Lesson 18',1,18,'https://www.youtube.com/embed/HaFaf7vbgpE'),(32,NULL,'Lesson 19',1,19,'https://www.youtube.com/embed/E8GNde5nCSg'),(33,NULL,'Lesson 20',1,20,'https://www.youtube.com/embed/1hIwD17Crko'),(34,NULL,'Lesson 21',1,21,'https://www.youtube.com/embed/auxpcdQimCs'),(35,NULL,'Lesson 22',1,22,'https://www.youtube.com/embed/yB9HHyPpKds'),(36,NULL,'Lesson 23',1,23,'https://www.youtube.com/embed/ZJscxTyI__s'),(37,NULL,'Lesson 24',1,24,'https://www.youtube.com/embed/TuDfZ2Md5x8'),(38,NULL,'Lesson 25',1,25,'https://www.youtube.com/embed/jjy-eqWM38g'),(39,NULL,'Lesson 26',1,26,'https://www.youtube.com/embed/CWMh61yutjU'),(40,NULL,'Lesson 27',1,27,'https://www.youtube.com/embed/ld75W1dz-h0'),(41,NULL,'Lesson 28',1,28,'https://www.youtube.com/embed/7ATtD8x7vV0'),(42,NULL,'Lesson 29',1,29,'https://www.youtube.com/embed/4zKVx29_A1w'),(43,NULL,'Lesson 30',1,30,'https://www.youtube.com/embed/jfvMtCHv1q4'),(44,NULL,'Lesson 31',1,31,'https://www.youtube.com/embed/Mj06h8BeeOA'),(45,NULL,'Lesson 32',1,32,'https://www.youtube.com/embed/PWx9DurgPn8'),(46,NULL,'Lesson 33',1,33,'https://www.youtube.com/embed/RrMvUL8HFlM'),(47,NULL,'Lesson 34',1,34,'https://www.youtube.com/embed/qZWPBKULkdQ'),(48,NULL,'Lesson 35',1,35,'https://www.youtube.com/embed/pIFiCLhJmig'),(49,NULL,'Lesson 36',1,36,'https://www.youtube.com/embed/an4rgJ3O21A'),(50,NULL,'Lesson 37',1,37,'https://www.youtube.com/embed/W8UI7F43_Yk'),(51,NULL,'Lesson 38',1,38,'https://www.youtube.com/embed/tj_QPnO8vpQ'),(52,NULL,'Lesson 39',1,39,'https://www.youtube.com/embed/I82ADyJC7wE'),(53,NULL,'Lesson 40',1,40,'https://www.youtube.com/embed/_O2sg-PGhEg'),(54,NULL,'Lesson 41',1,41,'https://www.youtube.com/embed/Z2zA9nPFN5A'),(55,NULL,'Lesson 42',1,42,'https://www.youtube.com/embed/9W3RsaWuCuE'),(56,NULL,'Lesson 43',1,43,'https://www.youtube.com/embed/9B7Ix2VQEGo'),(57,NULL,'Lesson 44',1,44,'https://www.youtube.com/embed/gzLM6ltw3l0'),(58,NULL,'Lesson 45',1,45,'https://www.youtube.com/embed/IGCVTSQw7WU'),(59,NULL,'Lesson 46',1,46,'https://www.youtube.com/embed/jDF-N3A60DE'),(60,NULL,'Lesson 47',1,47,'https://www.youtube.com/embed/mgdq6DOTU3M'),(61,NULL,'Lesson 48',1,48,'https://www.youtube.com/embed/0ytyMKa8aps'),(112,NULL,'Lesson 1',2,1,'https://www.youtube.com/embed/vDv3iSMdYyc'),(113,NULL,'Lesson 2',2,2,'https://www.youtube.com/embed/ggZsMEO2q0g'),(114,NULL,'Lesson 3',2,3,'https://www.youtube.com/embed/P2nw2UWV-dU'),(115,NULL,'Lesson 4',2,4,'https://www.youtube.com/embed/EW2JYlQaEzo'),(116,NULL,'Lesson 5',2,5,'https://www.youtube.com/embed/zEGYWbM9ilE'),(117,NULL,'Lesson 6',2,6,'https://www.youtube.com/embed/N40STzYBcNg'),(118,NULL,'Lesson 7',2,7,'https://www.youtube.com/embed/9_Pwhakn2pg'),(119,NULL,'Lesson 8',2,8,'https://www.youtube.com/embed/OvuFHFed5cQ'),(120,NULL,'Lesson 9',2,9,'https://www.youtube.com/embed/5M4l0Ylh3L8'),(121,NULL,'Lesson 10',2,10,'https://www.youtube.com/embed/Ppo_vqKM9Pg'),(122,NULL,'Lesson 11',2,11,'https://www.youtube.com/embed/t-dWAE3uSrk'),(123,NULL,'Lesson 12',2,12,'https://www.youtube.com/embed/ucSpyq9VuV4'),(124,NULL,'Lesson 13',2,13,'https://www.youtube.com/embed/MR_UvRdwcZ8'),(125,NULL,'Lesson 14',2,14,'https://www.youtube.com/embed/x32ZraXRPdg'),(126,NULL,'Lesson 15',2,15,'https://www.youtube.com/embed/JD7QtFSo4YA'),(127,NULL,'Lesson 16',2,16,'https://www.youtube.com/embed/aizFTBfbn6k'),(128,NULL,'Lesson 17',2,17,'https://www.youtube.com/embed/6zUsYkRfhiM'),(129,NULL,'Lesson 18',2,18,'https://www.youtube.com/embed/VG-MNB6i1cs'),(130,NULL,'Lesson 19',2,19,'https://www.youtube.com/embed/Dr9nlMoQ4Do'),(131,NULL,'Lesson 20',2,20,'https://www.youtube.com/embed/iGMYHH9pS6k'),(132,NULL,'Lesson 21',2,21,'https://www.youtube.com/embed/f5acbl1B4RI'),(133,NULL,'Lesson 22',2,22,'https://www.youtube.com/embed/HqBDLeGS6Rw'),(134,NULL,'Lesson 23',2,23,'https://www.youtube.com/embed/zaPE8EAbpjw'),(135,NULL,'Lesson 24',2,24,'https://www.youtube.com/embed/LxS-InE7hOc'),(136,NULL,'Lesson 25',2,25,'https://www.youtube.com/embed/XqJPG7_cbMY'),(137,NULL,'Lesson 26',2,26,'https://www.youtube.com/embed/9T3IHeI322o'),(138,NULL,'Lesson 27',2,27,'https://www.youtube.com/embed/6-lhklNzm3A'),(139,NULL,'Lesson 28',2,28,'https://www.youtube.com/embed/bAg-dJJY46A'),(140,NULL,'Lesson 29',2,29,'https://www.youtube.com/embed/deV7ctJWqiw'),(141,NULL,'Lesson 30',2,30,'https://www.youtube.com/embed/P6AWicrtJXM'),(142,NULL,'Lesson 31',2,31,'https://www.youtube.com/embed/ErHniHf05dg'),(143,NULL,'Lesson 32',2,32,'https://www.youtube.com/embed/hN1dn4gsJhs'),(144,NULL,'Lesson 33',2,33,'https://www.youtube.com/embed/YhYN2OcwA0U'),(145,NULL,'Lesson 34',2,34,'https://www.youtube.com/embed/3GANGKHWwL4'),(146,NULL,'Lesson 35',2,35,'https://www.youtube.com/embed/r2zZS-FeR5M'),(147,NULL,'Lesson 36',2,36,'https://www.youtube.com/embed/kUKTE-KSnV4'),(148,NULL,'Lesson 37',2,37,'https://www.youtube.com/embed/gbVblS14fnA'),(149,NULL,'Lesson 38',2,38,'https://www.youtube.com/embed/W0XKk8xrSGg'),(150,NULL,'Lesson 39',2,39,'https://www.youtube.com/embed/_y__LthMREU'),(151,NULL,'Lesson 40',2,40,'https://www.youtube.com/embed/0MCWWIbOwtM');
/*!40000 ALTER TABLE `lessons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `options`
--

DROP TABLE IF EXISTS `options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `options` (
  `option_id` int NOT NULL AUTO_INCREMENT,
  `question_id` int DEFAULT NULL,
  `option_text` text,
  `is_correct` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`option_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `options_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=337 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `options`
--

LOCK TABLES `options` WRITE;
/*!40000 ALTER TABLE `options` DISABLE KEYS */;
INSERT INTO `options` VALUES (93,27,'Astronomy is a science; astrology is a belief system.',1),(94,27,'Astronomy only studies stars.',0),(95,27,'Astrology is more accurate.',0),(96,27,'They are the same thing.',0),(97,28,'Redshift',0),(98,28,'Parallax',1),(99,28,'Precession',0),(100,28,'Retrograde motion',0),(101,29,'Earth\'s shadow',0),(102,29,'Clouds',0),(103,29,'Sun-Moon-Earth positions',1),(104,29,'Moon rotation',0),(105,30,'Mars',0),(106,30,'Venus',1),(107,30,'Mercury',0),(108,30,'Jupiter',0),(109,31,'Helium',0),(110,31,'Hydrogen',1),(111,31,'Carbon',0),(112,31,'Iron',0),(113,32,'Kepler Law',0),(114,32,'Hubble Law',1),(115,32,'Stefan Law',0),(116,32,'Wien Law',0),(117,33,'Mass vs Radius',0),(118,33,'Luminosity vs Temperature',1),(119,33,'Age vs Distance',0),(120,33,'Rotation vs Field',0),(121,34,'Conduction',0),(122,34,'Radiation',0),(123,34,'Convection',1),(124,34,'Neutrino',0),(125,35,'Singularity',0),(126,35,'Disk',0),(127,35,'Event Horizon',1),(128,35,'Ergosphere',0),(129,36,'273K',0),(130,36,'0K',0),(131,36,'2.7K',1),(132,36,'15M K',0),(133,37,'Measuring star age',0),(134,37,'Standard candles for cosmic distance',1),(135,37,'Detect black holes',0),(136,37,'Study solar flares',0),(137,38,'Astronomy is a science; astrology is a belief system.',1),(138,38,'Astronomy only studies stars.',0),(139,38,'Astrology is more accurate.',0),(140,38,'They are the same thing.',0),(141,39,'Redshift',0),(142,39,'Parallax',1),(143,39,'Precession',0),(144,39,'Retrograde motion',0),(145,40,'Earth\'s shadow',0),(146,40,'Clouds',0),(147,40,'Sun-Moon-Earth positions',1),(148,40,'Moon rotation',0),(149,41,'Mars',0),(150,41,'Venus',1),(151,41,'Mercury',0),(152,41,'Jupiter',0),(153,42,'Helium',0),(154,42,'Hydrogen',1),(155,42,'Carbon',0),(156,42,'Iron',0),(157,43,'Earth between Sun and Moon',0),(158,43,'Moon between Sun and Earth',1),(159,43,'Sun between Earth and Moon',0),(160,43,'Planet between Sun and Earth',0),(161,44,'Magnetism',0),(162,44,'Gravity',1),(163,44,'Friction',0),(164,44,'Centrifugal force',0),(165,45,'Singularity',0),(166,45,'Boundary where light cannot escape',1),(167,45,'Accretion disk',0),(168,45,'Photon sphere',0),(169,46,'Lenses',0),(170,46,'Mirrors',1),(171,46,'Prisms',0),(172,46,'Antennas',0),(173,47,'Time',0),(174,47,'Distance',1),(175,47,'Brightness',0),(176,47,'Speed',0),(177,48,'Saturn',0),(178,48,'Jupiter',1),(179,48,'Neptune',0),(180,48,'Uranus',0),(181,49,'Static universe',0),(182,49,'Expanding universe',1),(183,49,'Shrinking universe',0),(184,49,'Dark matter',0),(185,50,'New star',0),(186,50,'Cooling star',0),(187,50,'Explosive death of star',1),(188,50,'Nebula',0),(189,51,'Destroyed planet',0),(190,51,'Planet around another star',1),(191,51,'Gas planet',0),(192,51,'Asteroid belt planet',0),(193,52,'Dark energy',0),(194,52,'Big Bang radiation',1),(195,52,'Solar wind',0),(196,52,'Gamma rays',0),(197,53,'Asteroid',0),(198,53,'Comet',1),(199,53,'Meteor',0),(200,53,'Dwarf planet',0),(201,54,'Dark matter star',0),(202,54,'Dense core after supernova',1),(203,54,'Young star',0),(204,54,'Gas ball',0),(205,55,'Shadow',0),(206,55,'Hidden black holes',0),(207,55,'Invisible mass causing gravity',1),(208,55,'Energy expansion',0),(209,56,'Black hole',0),(210,56,'White dwarf',1),(211,56,'Neutron star',0),(212,56,'Supernova',0),(213,57,'Nebula stretch',0),(214,57,'Tidal stretching near black hole',1),(215,57,'Food prep',0),(216,57,'Light shift',0),(217,58,'Distance vs speed',0),(218,58,'Luminosity vs temperature',1),(219,58,'Mass vs age',0),(220,58,'Size vs orbit',0),(221,59,'Closer to sun',0),(222,59,'Greenhouse effect',1),(223,59,'More moons',0),(224,59,'Faster rotation',0),(225,60,'Large size',0),(226,60,'Periodic radiation pulses',1),(227,60,'Oxygen',0),(228,60,'No magnetic field',0),(229,61,'Object in space',0),(230,61,'Object hitting Earth',1),(231,61,'Light streak',0),(232,61,'Ice core',0),(233,62,'Black holes',0),(234,62,'Accelerating expansion',1),(235,62,'Galaxy binding',0),(236,62,'Fusion',0),(237,63,'Kepler Law',0),(238,63,'Hubble Law',1),(239,63,'Stefan Law',0),(240,63,'Wien Law',0),(241,64,'Mass vs Radius',0),(242,64,'Luminosity vs Temperature',1),(243,64,'Age vs Distance',0),(244,64,'Rotation vs Field',0),(245,65,'Conduction',0),(246,65,'Radiation',0),(247,65,'Convection',1),(248,65,'Neutrinos',0),(249,66,'Singularity',0),(250,66,'Disk',0),(251,66,'Event Horizon',1),(252,66,'Ergosphere',0),(253,67,'273K',0),(254,67,'0K',0),(255,67,'2.7K',1),(256,67,'15M K',0),(257,68,'p-p chain',0),(258,68,'CNO cycle',1),(259,68,'Triple alpha',0),(260,68,'Carbon burning',0),(261,69,'Moving towards us',0),(262,69,'Very close object',0),(263,69,'Far and moving away',1),(264,69,'Cold gas',0),(265,70,'Expansion rate',0),(266,70,'Density ratio',1),(267,70,'Age of universe',0),(268,70,'Speed of light',0),(269,71,'White dwarf',0),(270,71,'Neutron star',0),(271,71,'Black hole',1),(272,71,'Brown dwarf',0),(273,72,'Carbon',0),(274,72,'Silicon',0),(275,72,'Iron',1),(276,72,'Uranium',0),(277,73,'Thermal pressure',0),(278,73,'Radiation pressure',0),(279,73,'Electron degeneracy pressure',1),(280,73,'Neutron pressure',0),(281,74,'Universe has center',0),(282,74,'Homogeneous & isotropic',1),(283,74,'Gravity only force',0),(284,74,'Static universe',0),(285,75,'Black holes',0),(286,75,'Dark matter',1),(287,75,'Dust',0),(288,75,'Dark energy',0),(289,76,'Only hydrogen',0),(290,76,'Hydrogen & helium',1),(291,76,'Oxygen & carbon',0),(292,76,'Heavy metals',0),(293,77,'Kuiper belt',0),(294,77,'Goldilocks zone',1),(295,77,'Lagrange point',0),(296,77,'Oort cloud',0),(297,78,'Gravity',0),(298,78,'Chemical burning',0),(299,78,'Nuclear fusion',1),(300,78,'Accretion',0),(301,79,'Inflation',0),(302,79,'Recombination',1),(303,79,'Nucleosynthesis',0),(304,79,'Reionization',0),(305,80,'Change color',0),(306,80,'Bend light',1),(307,80,'Increase rotation',0),(308,80,'Measure temperature',0),(309,81,'Star age',0),(310,81,'Distance measurement',1),(311,81,'Black holes',0),(312,81,'Solar flares',0),(313,82,'Steady state',0),(314,82,'Inflation',1),(315,82,'Relativity',0),(316,82,'String theory',0),(317,83,'Max mass white dwarf',1),(318,83,'Min star mass',0),(319,83,'Black hole size',0),(320,83,'Sun distance',0),(321,84,'G',0),(322,84,'M',0),(323,84,'O',1),(324,84,'K',0),(325,85,'Galaxy binding',0),(326,85,'First stars',0),(327,85,'Accelerating expansion',1),(328,85,'Neutrinos',0),(329,86,'4.5B',0),(330,86,'13.8B',1),(331,86,'100B',0),(332,86,'10K',0),(333,87,'Photons',0),(334,87,'Neutrinos',0),(335,87,'Protons & electrons',1),(336,87,'Neutrons',0);
/*!40000 ALTER TABLE `options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `progress`
--

DROP TABLE IF EXISTS `progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `progress` (
  `progress_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `lesson_id` int DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`progress_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progress`
--

LOCK TABLES `progress` WRITE;
/*!40000 ALTER TABLE `progress` DISABLE KEYS */;
/*!40000 ALTER TABLE `progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `quiz_id` int DEFAULT NULL,
  `question_text` text,
  PRIMARY KEY (`question_id`),
  KEY `quiz_id` (`quiz_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`quiz_id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (27,4,'What is the primary difference between astronomy and astrology?'),(28,4,'Which term describes the apparent shift of a nearby object?'),(29,4,'What causes phases of the Moon?'),(30,4,'Which planet has runaway greenhouse effect?'),(31,4,'What fuel powers stars?'),(32,5,'Which law relates galaxy distance and velocity?'),(33,5,'HR diagram plots what?'),(34,5,'Energy transport in Sun outer layer?'),(35,5,'Schwarzschild radius defines?'),(36,5,'CMB temperature today?'),(37,5,'What is Type Ia Supernova used for?'),(38,4,'What is the primary difference between astronomy and astrology?'),(39,4,'Which term describes apparent shift of nearby object?'),(40,4,'What causes phases of Moon?'),(41,4,'Which planet has runaway greenhouse effect?'),(42,4,'Fuel of stars?'),(43,4,'Total solar eclipse occurs when?'),(44,4,'Force keeping planets in orbit?'),(45,4,'Event horizon is?'),(46,4,'Reflecting telescope uses?'),(47,4,'Light year is unit of?'),(48,4,'Largest planet?'),(49,4,'Redshift shows?'),(50,4,'Supernova is?'),(51,4,'Exoplanet is?'),(52,4,'CMB is?'),(53,4,'Dirty snowball object?'),(54,4,'Neutron star is?'),(55,4,'Dark matter is?'),(56,4,'Final stage of Sun-like star?'),(57,4,'Spaghettification means?'),(58,4,'HR diagram shows?'),(59,4,'Why Venus hotter than Mercury?'),(60,4,'Pulsar defined by?'),(61,4,'Meteorite is?'),(62,4,'Dark energy causes?'),(63,5,'Which law relates galaxy distance and velocity?'),(64,5,'HR diagram plots?'),(65,5,'Energy transport in Sun outer layer?'),(66,5,'Schwarzschild radius defines?'),(67,5,'CMB temperature today?'),(68,5,'Fusion dominant in massive stars?'),(69,5,'High redshift means?'),(70,5,'Omega parameter represents?'),(71,5,'Star >20 solar mass ends as?'),(72,5,'Fusion stops at which element?'),(73,5,'White dwarf stability due to?'),(74,5,'Cosmological principle states?'),(75,5,'Flat galaxy rotation due to?'),(76,5,'Big Bang produced mainly?'),(77,5,'Habitable zone is?'),(78,5,'Sun luminosity source?'),(79,5,'First neutral atoms formed in?'),(80,5,'Gravitational lensing does?'),(81,5,'Type Ia supernova used for?'),(82,5,'Rapid early expansion called?'),(83,5,'Chandrasekhar limit is?'),(84,5,'Hottest stars type?'),(85,5,'Dark energy explains?'),(86,5,'Age of universe?'),(87,5,'Solar wind consists of?');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_attempts`
--

DROP TABLE IF EXISTS `quiz_attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz_attempts` (
  `attempt_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `quiz_id` int DEFAULT NULL,
  `score` int DEFAULT NULL,
  `total` int DEFAULT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`attempt_id`),
  KEY `user_id` (`user_id`),
  KEY `quiz_id` (`quiz_id`),
  CONSTRAINT `quiz_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `quiz_attempts_ibfk_2` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`quiz_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_attempts`
--

LOCK TABLES `quiz_attempts` WRITE;
/*!40000 ALTER TABLE `quiz_attempts` DISABLE KEYS */;
INSERT INTO `quiz_attempts` VALUES (11,2,4,16,30,'2026-04-10 04:55:00');
/*!40000 ALTER TABLE `quiz_attempts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quizzes`
--

DROP TABLE IF EXISTS `quizzes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quizzes` (
  `quiz_id` int NOT NULL AUTO_INCREMENT,
  `topic_id` int DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  PRIMARY KEY (`quiz_id`),
  KEY `topic_id` (`topic_id`),
  CONSTRAINT `fk_quiz_topic` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`topic_id`) ON DELETE SET NULL,
  CONSTRAINT `quizzes_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`topic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quizzes`
--

LOCK TABLES `quizzes` WRITE;
/*!40000 ALTER TABLE `quizzes` DISABLE KEYS */;
INSERT INTO `quizzes` VALUES (4,1,'Astronomy for Beginners Quiz',1),(5,3,'Astrophysics and Cosmology Quiz',2);
/*!40000 ALTER TABLE `quizzes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin'),(2,'student'),(3,'teacher');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topics` (
  `topic_id` int NOT NULL AUTO_INCREMENT,
  `topic_name` varchar(100) DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  PRIMARY KEY (`topic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topics`
--

LOCK TABLES `topics` WRITE;
/*!40000 ALTER TABLE `topics` DISABLE KEYS */;
INSERT INTO `topics` VALUES (1,'Introduction to Universe',1),(2,'Stars and Galaxies',1),(3,'Solar System Basics',2),(4,'Planets and Motion',2),(5,'Black Hole Theory',3),(6,'Event Horizon',3),(7,'Introduction to Universe',1),(8,'Stars and Galaxies',1),(9,'Solar System Basics',2),(10,'Planets and Motion',2),(11,'Black Hole Theory',3),(12,'Event Horizon',3);
/*!40000 ALTER TABLE `topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_answers`
--

DROP TABLE IF EXISTS `user_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_answers` (
  `answer_id` int NOT NULL AUTO_INCREMENT,
  `attempt_id` int DEFAULT NULL,
  `question_id` int DEFAULT NULL,
  `selected_option` int DEFAULT NULL,
  PRIMARY KEY (`answer_id`),
  KEY `attempt_id` (`attempt_id`),
  CONSTRAINT `user_answers_ibfk_1` FOREIGN KEY (`attempt_id`) REFERENCES `quiz_attempts` (`attempt_id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_answers`
--

LOCK TABLES `user_answers` WRITE;
/*!40000 ALTER TABLE `user_answers` DISABLE KEYS */;
INSERT INTO `user_answers` VALUES (25,11,27,94),(26,11,28,99),(27,11,29,101),(28,11,30,106),(29,11,31,110),(30,11,38,139),(31,11,39,142),(32,11,40,147),(33,11,41,152),(34,11,42,154),(35,11,43,160),(36,11,44,162),(37,11,45,168),(38,11,46,169),(39,11,47,174),(40,11,48,179),(41,11,49,182),(42,11,50,187),(43,11,51,190),(44,11,52,194),(45,11,53,198),(46,11,54,201),(47,11,55,206),(48,11,56,210),(49,11,57,216),(50,11,58,218),(51,11,59,223),(52,11,60,228),(53,11,61,230),(54,11,62,234);
/*!40000 ALTER TABLE `user_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profiles`
--

DROP TABLE IF EXISTS `user_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_profiles` (
  `profile_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `bio` text,
  PRIMARY KEY (`profile_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profiles`
--

LOCK TABLES `user_profiles` WRITE;
/*!40000 ALTER TABLE `user_profiles` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reset_token` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `email_2` (`email`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'ashish','ashish@gmail.com','scrypt:32768:8:1$FVrZQ4AWDUHgwUSJ$6456a4b2623f5672bc73343ca686688b27c26b2aa8e6473b3fed76e29d339374e1a92cb45baa0f57bb40acbe02dcbe039a066cd40a37d99180ca955a8989886c',NULL,'2026-04-01 19:08:31',NULL),(2,'Navya','navya@gmail.com','scrypt:32768:8:1$sqDNk9Gg5SQaPCtf$69e30cc8dcbbb2fdaa59b91777b38c21a12ef8d2169dc92e44718e2fb1b88a2701fb2ecd8e80861ee1719cae7525da6c860262e8803ef370beb3b756c424b873',2,'2026-04-01 19:10:40','721dafdb-dc9d-46e8-91b0-16aceff31268'),(5,'TripleH','tripleh@gmail.com','scrypt:32768:8:1$s5cUC8T96eBHnq9w$b302e562d530627b105bafa849d0c66341bb26f75c1a69b55c23d47f52f5d9c9b71aee8899837d5cfb84b63c3d1e22d22a897fd9a9a7b280f83a303113bddc02',2,'2026-04-04 21:49:48',NULL),(7,'vindiesel','vin@gmail.com','scrypt:32768:8:1$xgWfTdIjHSQTURs2$c6590877e34b9ff353c6fad1ddc0052abe51846fc24248a1b6a04602d6cc7f0fb230aaf74473d2b75ac39ca02440ee53d45932489637565bc6645f542d354b2b',2,'2026-04-06 07:57:46','753caca1-ad3d-45f0-8b9a-8e38178ce324'),(8,'Carl Sagan','carl@gmail.com','scrypt:32768:8:1$Z9Yrbxj07Mnvo3OI$699c283afd879173f1779faf7ab8f64d4d944e5f213de527dde8793a658890d2c22c2aa2023c3abedf8a55f260190aedccbff95b9407fddead02f89c979feba7',3,'2026-04-06 08:32:15','39e4dddd-b299-4af0-8b22-6b210817c316'),(9,'Neil deGrasse Tyson','neil@gmail.com','scrypt:32768:8:1$dkNCQh5Go0D3BTJ2$5612f1267264b91ff2f6b6c6bf1dbc5aeb804cb9d9c4c6f246326c45e2543cb7f838d9bd19871ccfbeed3d8ebcdc4fe44ccd3b3a0f4cfbbd7a9aa59037849715',3,'2026-04-06 08:32:15','0275850e-e125-4dfd-b940-7b540596a3de'),(10,'Isaac Newton','newton@gmail.com','scrypt:32768:8:1$DeFkwTj7yGt6Moiv$55a69c42ec87cc7105c8d857ea085119410f7f7647b0cd95539bceb35838ad0f743b289d976d540209d30fc0298dc6bddf390629b4336a57420c9664d5b85f11',3,'2026-04-06 08:32:15','b78936c6-a169-4d82-884b-9fcb51e9e71d'),(11,'freakin_vishal','jarvishalsinha789@gmail.com','scrypt:32768:8:1$niWV1gCjhFZitY6N$e068084db25cf5276b087b9369d58cbbc4038f0e41614905f6153c854621dbe3e044ce842b9fb0ec923cd72a57297463fcf2f66af7ac69f6bd107014429b4330',2,'2026-04-12 17:02:30',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `videos` (
  `video_id` int NOT NULL AUTO_INCREMENT,
  `lesson_id` int DEFAULT NULL,
  `video_url` text,
  PRIMARY KEY (`video_id`),
  KEY `lesson_id` (`lesson_id`),
  CONSTRAINT `videos_ibfk_1` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`lesson_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videos`
--

LOCK TABLES `videos` WRITE;
/*!40000 ALTER TABLE `videos` DISABLE KEYS */;
/*!40000 ALTER TABLE `videos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-13 12:32:08
