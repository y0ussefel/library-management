-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: planning_universite
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `etudiants`
--

DROP TABLE IF EXISTS `etudiants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etudiants` (
  `id_etudiant` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `telephone` varchar(15) DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `genre` varchar(45) DEFAULT NULL,
  `id_filiere` int DEFAULT NULL,
  PRIMARY KEY (`id_etudiant`),
  KEY `id_filiere` (`id_filiere`),
  CONSTRAINT `etudiants_ibfk_1` FOREIGN KEY (`id_filiere`) REFERENCES `filieres` (`id_filiere`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `etudiants`
--

LOCK TABLES `etudiants` WRITE;
/*!40000 ALTER TABLE `etudiants` DISABLE KEYS */;
INSERT INTO `etudiants` VALUES (2,'grgrg','fefef','grg@gmail.com','0105050512','2003-06-12','Masculin',11),(3,'grgrg','fefef','grg@gmail.com','0105050512','2003-06-12','Masculin',11);
/*!40000 ALTER TABLE `etudiants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filieres`
--

DROP TABLE IF EXISTS `filieres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filieres` (
  `id_filiere` int NOT NULL AUTO_INCREMENT,
  `nom_filiere` varchar(255) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id_filiere`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filieres`
--

LOCK TABLES `filieres` WRITE;
/*!40000 ALTER TABLE `filieres` DISABLE KEYS */;
INSERT INTO `filieres` VALUES (11,NULL,NULL);
/*!40000 ALTER TABLE `filieres` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-14  1:41:05
-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: library
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL,
  `username` varchar(45) DEFAULT NULL,
  `pass` varchar(45) DEFAULT NULL,
  `emp_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_empt` (`emp_id`),
  CONSTRAINT `fk_empt` FOREIGN KEY (`emp_id`) REFERENCES `employers` (`cin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'admin','123456',NULL),(2,'users','1234',NULL);
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clients` (
  `cin` decimal(10,0) NOT NULL,
  `nom` varchar(45) DEFAULT NULL,
  `prenom` varchar(45) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` int DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`cin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (12341,'sqihla','9alo','gg@gmail.com',789321456,'2024-06-13 16:08:21'),(12345,'sali','souu','sss@gmail.com',789456123,'2024-06-13 15:57:37'),(12346,'grgrg','grgrgrg','you@gmail.com',123456789,NULL),(12745,'el fe','yossef','gegege@gmail.xom',1234567890,NULL),(22551,'jamal','monik','jamal@gmail.com',639466393,'2024-06-13 15:54:51'),(25648,'dfefefe','fefefef','yoxu@mail.com',123456701,NULL),(43434,'ddgegeg','egegege','gegeg',123456789,NULL),(234232,'omar','lhmar','kdfkdfjdkfj@kfdekfj',12122121,NULL),(2323232,'ranya','misony','kfkdfj#kdfjkfj',5545454,NULL);
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employers`
--

DROP TABLE IF EXISTS `employers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employers` (
  `cin` int NOT NULL,
  `nom` varchar(45) DEFAULT NULL,
  `prenom` varchar(45) DEFAULT NULL,
  `login` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  PRIMARY KEY (`cin`),
  KEY `fk_department` (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employers`
--

LOCK TABLES `employers` WRITE;
/*!40000 ALTER TABLE `employers` DISABLE KEYS */;
INSERT INTO `employers` VALUES (11112,'youss','lalal','user123','qwert12345',NULL),(14523,'youssef','fenary','youx','1234567890',NULL),(123458,'fefef','fefef','efef','051545',NULL);
/*!40000 ALTER TABLE `employers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emprunter`
--

DROP TABLE IF EXISTS `emprunter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emprunter` (
  `id_emp` int NOT NULL AUTO_INCREMENT,
  `titre_book` varchar(45) DEFAULT NULL,
  `cin_client` int DEFAULT NULL,
  `date_emp` varchar(45) DEFAULT NULL,
  `date_ret` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_emp`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emprunter`
--

LOCK TABLES `emprunter` WRITE;
/*!40000 ALTER TABLE `emprunter` DISABLE KEYS */;
INSERT INTO `emprunter` VALUES (6,'aloooooo',12745,'fefafadf','fafdfa'),(7,'livreq',12341,'12-04-2024','15-04-2024'),(12,'aloooooo',12341,'21-08-2021','21-09-2021'),(13,'alo',12341,'12-05-2023','15-05-2023'),(14,'alo',12745,'12-12-2024','13-12-2024'),(16,'livreq',12745,'12-12-2015','18-12-2015'),(17,'alo',43434,'12-12-2014','12-02-2015'),(18,'livreq',43434,'12-05-2021','14-05-2021'),(19,'aloooooo',22551,'23-04-2014','30-04-2014'),(20,'alo',22551,'23-01-2023','27-01-2023'),(21,'alo',12341,'23-03-2023','27-03-2023'),(22,'saw',43434,'12-12-2022','25-12-2022'),(23,'saw',12341,'12-11-2022','22-11-2022');
/*!40000 ALTER TABLE `emprunter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `livres`
--

DROP TABLE IF EXISTS `livres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `livres` (
  `code` int NOT NULL,
  `titre` varchar(45) DEFAULT NULL,
  `auteur` varchar(45) DEFAULT NULL,
  `categorie` varchar(45) DEFAULT NULL,
  `prix` int DEFAULT NULL,
  `statut` varchar(45) DEFAULT NULL,
  `publicite` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `nb_emp` int DEFAULT '0',
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `livres`
--

LOCK TABLES `livres` WRITE;
/*!40000 ALTER TABLE `livres` DISABLE KEYS */;
INSERT INTO `livres` VALUES (13,'alo','rgrgr','dffdff',13,'Neuf ','nhar tlat','grhrhrh\n',13,2),(111,'aloooooo','ahmad wi','crwasa',2,'Neuf ','sff','\n',12,0),(444,'fkkefh','ffefe','efefefe',323,' Utilisé','12-01-2024','fefe\n',23,0),(1212,'livreq','ahmad wissal','crwasa',12,' Utilisé','wewew','\n',12,1),(1234,'saw','youssef el fenary','horror',40,'Neuf ','12-05-2023','none\n',12,2),(222222,'efefefe','dwdwdw','efefef',245,'Neuf ','23-07-2023','efefe\n',12,0);
/*!40000 ALTER TABLE `livres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retourner`
--

DROP TABLE IF EXISTS `retourner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `retourner` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titreBook` varchar(45) DEFAULT NULL,
  `cinClient` varchar(45) DEFAULT NULL,
  `date_ret` varchar(45) DEFAULT NULL,
  `date_emp` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retourner`
--

LOCK TABLES `retourner` WRITE;
/*!40000 ALTER TABLE `retourner` DISABLE KEYS */;
INSERT INTO `retourner` VALUES (2,'alo','22551','15-04-2024','12-04-2024'),(3,'alo','12346','rgrg','fggrg'),(4,'alo',' 12341','23-07-2024','16-07-2024'),(5,'alo','12341','25-05-2014','12-05-2014'),(6,'alo','12745','12-06-2024','12-05-2024'),(7,'livreq','12745','15-12-2017','12-12-2017');
/*!40000 ALTER TABLE `retourner` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-14  1:41:05
