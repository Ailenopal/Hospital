-- Hospital Management System database for MySQL Workbench (MySQL 8)
-- Import: Workbench > Server > Data Import > "Import from Self-Contained File" > choose this file > Start Import.
-- Demo logins (sample-data file): superadmin and admin1, password Admin@12345

-- Run this in MySQL Workbench (File > Open SQL Script, then click the lightning bolt).
-- Connect as root first. It creates the database and a dedicated user for the app.

CREATE DATABASE IF NOT EXISTS hms_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'hms_user'@'localhost' IDENTIFIED BY 'Hms@12345';
CREATE USER IF NOT EXISTS 'hms_user'@'127.0.0.1' IDENTIFIED BY 'Hms@12345';

GRANT ALL PRIVILEGES ON hms_db.* TO 'hms_user'@'localhost';
GRANT ALL PRIVILEGES ON hms_db.* TO 'hms_user'@'127.0.0.1';
FLUSH PRIVILEGES;

-- Afterwards, from the project folder run:  python manage.py migrate
-- then refresh the SCHEMAS panel in Workbench to see the tables.

-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: hms_db
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.5

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
-- Current Database: `hms_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `hms_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `hms_db`;

--
-- Table structure for table `accounts_customuser`
--

DROP TABLE IF EXISTS `accounts_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `can_archive_patients` tinyint(1) NOT NULL,
  `can_manage_admissions` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `accounts_customuser_created_by_id_81e9c932_fk_accounts_` (`created_by_id`),
  CONSTRAINT `accounts_customuser_created_by_id_81e9c932_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser`
--

LOCK TABLES `accounts_customuser` WRITE;
/*!40000 ALTER TABLE `accounts_customuser` DISABLE KEYS */;
INSERT INTO `accounts_customuser` VALUES (1,'pbkdf2_sha256$1000000$WrivXLRXU8WK7PEWb8Q0YH$K0Q6Y37hFoaeyk2j4hXTXCY+wJnwd6O5Vi5oX19Ydig=',NULL,1,'superadmin','Sam','Reyes','superadmin@hms.example',1,1,'2026-11-17 04:46:11.925476','super_admin','',1,1,'2026-11-17 04:46:11.925689',NULL),(2,'pbkdf2_sha256$1000000$5Pwc82V8Oi3ooICioMvQ6j$+Z4ScpFfuAY3L4uTqKWD8eATzqTrKwANewvXVcAScD4=',NULL,0,'admin1','Nina','Cortez','admin1@hms.example',0,1,'2026-11-17 04:46:12.185644','admin','',1,1,'2026-11-17 04:46:12.185887',1),(3,'pbkdf2_sha256$1000000$3PjTAYrU8Jk9fTF4k5uYgg$jRMgpsfIFgajKjC1oHAT/RwopTZQEdT6mXWFAUmTo94=',NULL,0,'admin2','Marco','Dizon','admin2@hms.example',0,1,'2026-11-17 04:46:12.457085','admin','',1,1,'2026-11-17 04:46:12.457284',1);
/*!40000 ALTER TABLE `accounts_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_groups`
--

DROP TABLE IF EXISTS `accounts_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq` (`customuser_id`,`group_id`),
  KEY `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_customuser__customuser_id_bc55088e_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_groups`
--

LOCK TABLES `accounts_customuser_groups` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_user_permissions`
--

DROP TABLE IF EXISTS `accounts_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_user_customuser_id_permission_9632a709_uniq` (`customuser_id`,`permission_id`),
  KEY `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_customuser__customuser_id_0deaefae_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_user_permissions`
--

LOCK TABLES `accounts_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admissions_admission`
--

DROP TABLE IF EXISTS `admissions_admission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admissions_admission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `admission_date` datetime(6) NOT NULL,
  `ward` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `room_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `attending_physician` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reason` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `discharge_date` datetime(6) DEFAULT NULL,
  `discharge_notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `admitted_by_id` bigint DEFAULT NULL,
  `discharged_by_id` bigint DEFAULT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `admissions_admission_admitted_by_id_f569c1af_fk_accounts_` (`admitted_by_id`),
  KEY `admissions_admission_discharged_by_id_8d0d4e08_fk_accounts_` (`discharged_by_id`),
  KEY `admissions_admission_patient_id_6e0ce5b6_fk_patients_patient_id` (`patient_id`),
  CONSTRAINT `admissions_admission_admitted_by_id_f569c1af_fk_accounts_` FOREIGN KEY (`admitted_by_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `admissions_admission_discharged_by_id_8d0d4e08_fk_accounts_` FOREIGN KEY (`discharged_by_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `admissions_admission_patient_id_6e0ce5b6_fk_patients_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admissions_admission`
--

LOCK TABLES `admissions_admission` WRITE;
/*!40000 ALTER TABLE `admissions_admission` DISABLE KEYS */;
INSERT INTO `admissions_admission` VALUES (1,'2026-11-17 01:46:12.715404','Surgical Ward','109','Dr. C. Tan','Appendicitis',NULL,'',3,NULL,1),(2,'2026-11-14 01:46:12.715404','General Ward','296','Dr. C. Tan','Appendicitis',NULL,'',3,NULL,2),(3,'2026-11-13 01:46:12.715404','General Ward','157','Dr. B. Ramirez','Pneumonia',NULL,'',2,NULL,3),(4,'2026-11-15 01:46:12.715404','Surgical Ward','120','Dr. B. Ramirez','Post-operative care',NULL,'',2,NULL,4),(5,'2026-11-11 01:46:12.715404','ICU','232','Dr. D. Gonzales','Dengue fever',NULL,'',3,NULL,5),(6,'2026-09-24 04:46:12.715404','Surgical Ward','145','Dr. C. Tan','Pneumonia','2026-09-29 04:46:12.715404','Recovered well. Follow-up in two weeks.',2,2,6),(7,'2026-10-21 04:46:12.715404','General Ward','145','Dr. C. Tan','Pneumonia','2026-10-23 04:46:12.715404','Recovered well. Follow-up in two weeks.',2,3,7),(8,'2026-10-31 04:46:12.715404','ICU','105','Dr. C. Tan','Appendicitis','2026-11-04 04:46:12.715404','Recovered well. Follow-up in two weeks.',3,2,8),(9,'2026-11-05 04:46:12.715404','Maternity','222','Dr. A. Lopez','Dengue fever','2026-11-07 04:46:12.715404','Recovered well. Follow-up in two weeks.',3,2,9),(10,'2026-10-26 04:46:12.715404','Surgical Ward','256','Dr. B. Ramirez','Post-operative care','2026-11-01 04:46:12.715404','Recovered well. Follow-up in two weeks.',3,2,10),(11,'2026-10-21 04:46:12.715404','Surgical Ward','109','Dr. C. Tan','Pneumonia','2026-10-23 04:46:12.715404','Recovered well. Follow-up in two weeks.',2,2,11);
/*!40000 ALTER TABLE `admissions_admission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add System setting',6,'add_systemsetting'),(22,'Can change System setting',6,'change_systemsetting'),(23,'Can delete System setting',6,'delete_systemsetting'),(24,'Can view System setting',6,'view_systemsetting'),(25,'Can add activity log',7,'add_activitylog'),(26,'Can change activity log',7,'change_activitylog'),(27,'Can delete activity log',7,'delete_activitylog'),(28,'Can view activity log',7,'view_activitylog'),(29,'Can add custom user',8,'add_customuser'),(30,'Can change custom user',8,'change_customuser'),(31,'Can delete custom user',8,'delete_customuser'),(32,'Can view custom user',8,'view_customuser'),(33,'Can add patient',9,'add_patient'),(34,'Can change patient',9,'change_patient'),(35,'Can delete patient',9,'delete_patient'),(36,'Can view patient',9,'view_patient'),(37,'Can add medical information',10,'add_medicalinformation'),(38,'Can change medical information',10,'change_medicalinformation'),(39,'Can delete medical information',10,'delete_medicalinformation'),(40,'Can view medical information',10,'view_medicalinformation'),(41,'Can add emergency contact',11,'add_emergencycontact'),(42,'Can change emergency contact',11,'change_emergencycontact'),(43,'Can delete emergency contact',11,'delete_emergencycontact'),(44,'Can view emergency contact',11,'view_emergencycontact'),(45,'Can add admission',12,'add_admission'),(46,'Can change admission',12,'change_admission'),(47,'Can delete admission',12,'delete_admission'),(48,'Can view admission',12,'view_admission');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_activitylog`
--

DROP TABLE IF EXISTS `core_activitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_activitylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` char(39) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_activitylog_user_id_8705e516_fk_accounts_customuser_id` (`user_id`),
  KEY `core_activitylog_created_at_0dcde50a` (`created_at`),
  CONSTRAINT `core_activitylog_user_id_8705e516_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_activitylog`
--

LOCK TABLES `core_activitylog` WRITE;
/*!40000 ALTER TABLE `core_activitylog` DISABLE KEYS */;
INSERT INTO `core_activitylog` VALUES (1,'CREATE','Registered patient PAT-2026-00001 (Juan Santos Dela Cruz)',NULL,'2026-11-17 04:46:12.826593',2),(2,'CREATE','Registered patient PAT-2026-00002 (Maria Santos)',NULL,'2026-11-17 04:46:12.827167',2),(3,'CREATE','Registered patient PAT-2026-00003 (Jose M. Reyes)',NULL,'2026-11-17 04:46:12.827556',2),(4,'CREATE','Registered patient PAT-2026-00004 (Ana Santos Garcia)',NULL,'2026-11-17 04:46:12.827893',3),(5,'CREATE','Registered patient PAT-2026-00005 (Carlo M. Mendoza)',NULL,'2026-11-17 04:46:12.828275',2),(6,'CREATE','Registered patient PAT-2026-00006 (Liza Lopez Torres)',NULL,'2026-11-17 04:46:12.828611',3),(7,'CREATE','Registered patient PAT-2026-00007 (Miguel Lopez Ramos)',NULL,'2026-11-17 04:46:12.829049',3),(8,'CREATE','Registered patient PAT-2026-00008 (Rosa Santos Flores)',NULL,'2026-11-17 04:46:12.829374',2),(9,'CREATE','Registered patient PAT-2026-00009 (Paolo M. Aquino)',NULL,'2026-11-17 04:46:12.829640',2),(10,'CREATE','Registered patient PAT-2026-00010 (Grace Santos Bautista)',NULL,'2026-11-17 04:46:12.830137',2),(11,'ACCOUNT','Created Admin account \'admin1\'',NULL,'2026-11-17 04:46:12.830512',1),(12,'ACCOUNT','Created Admin account \'admin2\'',NULL,'2026-11-17 04:46:12.831060',1);
/*!40000 ALTER TABLE `core_activitylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_systemsetting`
--

DROP TABLE IF EXISTS `core_systemsetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_systemsetting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `hospital_name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tagline` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `registration_prefix` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  `records_per_page` smallint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `core_systemsetting_chk_1` CHECK ((`records_per_page` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_systemsetting`
--

LOCK TABLES `core_systemsetting` WRITE;
/*!40000 ALTER TABLE `core_systemsetting` DISABLE KEYS */;
INSERT INTO `core_systemsetting` VALUES (1,'City General Hospital','Compassionate care, trusted records','123 Health Avenue, Quezon City','(02) 8123-4567','info@citygeneral.example','PAT',10);
/*!40000 ALTER TABLE `core_systemsetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'accounts','customuser'),(1,'admin','logentry'),(12,'admissions','admission'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(7,'core','activitylog'),(6,'core','systemsetting'),(11,'patients','emergencycontact'),(10,'patients','medicalinformation'),(9,'patients','patient'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-11-17 04:46:11.029309'),(2,'contenttypes','0002_remove_content_type_name','2026-11-17 04:46:11.050402'),(3,'auth','0001_initial','2026-11-17 04:46:11.119343'),(4,'auth','0002_alter_permission_name_max_length','2026-11-17 04:46:11.138175'),(5,'auth','0003_alter_user_email_max_length','2026-11-17 04:46:11.142343'),(6,'auth','0004_alter_user_username_opts','2026-11-17 04:46:11.146164'),(7,'auth','0005_alter_user_last_login_null','2026-11-17 04:46:11.150266'),(8,'auth','0006_require_contenttypes_0002','2026-11-17 04:46:11.151060'),(9,'auth','0007_alter_validators_add_error_messages','2026-11-17 04:46:11.154283'),(10,'auth','0008_alter_user_username_max_length','2026-11-17 04:46:11.157564'),(11,'auth','0009_alter_user_last_name_max_length','2026-11-17 04:46:11.160856'),(12,'auth','0010_alter_group_name_max_length','2026-11-17 04:46:11.167547'),(13,'auth','0011_update_proxy_permissions','2026-11-17 04:46:11.171222'),(14,'auth','0012_alter_user_first_name_max_length','2026-11-17 04:46:11.174434'),(15,'accounts','0001_initial','2026-11-17 04:46:11.270982'),(16,'admin','0001_initial','2026-11-17 04:46:11.316203'),(17,'admin','0002_logentry_remove_auto_add','2026-11-17 04:46:11.321552'),(18,'admin','0003_logentry_add_action_flag_choices','2026-11-17 04:46:11.327552'),(19,'patients','0001_initial','2026-11-17 04:46:11.436141'),(20,'admissions','0001_initial','2026-11-17 04:46:11.495274'),(21,'core','0001_initial','2026-11-17 04:46:11.533877'),(22,'sessions','0001_initial','2026-11-17 04:46:11.544641');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_emergencycontact`
--

DROP TABLE IF EXISTS `patients_emergencycontact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients_emergencycontact` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `relationship` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patient_id` (`patient_id`),
  CONSTRAINT `patients_emergencyco_patient_id_5506bb56_fk_patients_` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_emergencycontact`
--

LOCK TABLES `patients_emergencycontact` WRITE;
/*!40000 ALTER TABLE `patients_emergencycontact` DISABLE KEYS */;
INSERT INTO `patients_emergencycontact` VALUES (1,'Isabel Dela Cruz','Spouse','09644854973','275 Rizal Street',1),(2,'Rosa Santos','Spouse','09719659571','290 Rizal Street',2),(3,'Ana Reyes','Parent','09499858816','287 Rizal Street',3),(4,'Isabel Garcia','Sibling','09366746013','300 Rizal Street',4),(5,'Daniel Mendoza','Child','09277126709','38 Rizal Street',5),(6,'Jose Torres','Spouse','09389845088','297 Rizal Street',6),(7,'Juan Ramos','Child','09481676682','198 Rizal Street',7),(8,'Liza Flores','Child','09531262237','255 Rizal Street',8),(9,'Carlo Aquino','Parent','09807076898','43 Rizal Street',9),(10,'Mateo Bautista','Spouse','09590317463','164 Rizal Street',10),(11,'Ana Villanueva','Sibling','09745025986','226 Rizal Street',11),(12,'Isabel Castillo','Sibling','09609116260','77 Rizal Street',12),(13,'Mateo Navarro','Parent','09654409968','136 Rizal Street',13),(14,'Liza Domingo','Sibling','09928862021','134 Rizal Street',14),(15,'Isabel Aguilar','Spouse','09129997207','266 Rizal Street',15),(16,'Miguel Pascual','Sibling','09319444228','117 Rizal Street',16),(17,'Liza Soriano','Child','09947327719','103 Rizal Street',17),(18,'Rafael Fernandez','Child','09965974909','15 Rizal Street',18),(19,'Miguel Salazar','Parent','09130058036','72 Rizal Street',19),(20,'Lourdes Valdez','Child','09988134464','182 Rizal Street',20),(21,'Carlo Rivera','Child','09764754893','77 Rizal Street',21),(22,'Paolo Tolentino','Spouse','09929209046','128 Rizal Street',22),(23,'Daniel Manalo','Parent','09850779486','274 Rizal Street',23),(24,'Jose Cruz','Parent','09818840243','124 Rizal Street',24),(25,'Liza Lim','Child','09653626718','84 Rizal Street',25);
/*!40000 ALTER TABLE `patients_emergencycontact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_medicalinformation`
--

DROP TABLE IF EXISTS `patients_medicalinformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients_medicalinformation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blood_type` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `allergies` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `existing_conditions` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `medical_history` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `current_medications` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patient_id` (`patient_id`),
  CONSTRAINT `patients_medicalinfo_patient_id_3c2d041f_fk_patients_` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_medicalinformation`
--

LOCK TABLES `patients_medicalinformation` WRITE;
/*!40000 ALTER TABLE `patients_medicalinformation` DISABLE KEYS */;
INSERT INTO `patients_medicalinformation` VALUES (1,'B-','','','Appendectomy (2015).','',1),(2,'O+','','Hypertension','No significant surgical history.','',2),(3,'A-','Shellfish','Hyperlipidemia','No significant surgical history.','',3),(4,'B+','Sulfa drugs','Hypertension','Appendectomy (2015).','',4),(5,'AB-','','Asthma','No significant surgical history.','',5),(6,'O-','Sulfa drugs','Hyperlipidemia','No significant surgical history.','',6),(7,'B+','Shellfish','','Appendectomy (2015).','',7),(8,'unknown','Penicillin','Hypertension','No significant surgical history.','',8),(9,'B-','','Asthma','No significant surgical history.','Metformin 500mg',9),(10,'unknown','Peanuts','Asthma','Appendectomy (2015).','',10),(11,'A+','','','No significant surgical history.','Metformin 500mg',11),(12,'A-','','Asthma','No significant surgical history.','',12),(13,'A+','','','Appendectomy (2015).','Amlodipine 5mg',13),(14,'B-','Shellfish','','No significant surgical history.','Amlodipine 5mg',14),(15,'AB+','Peanuts','Type 2 diabetes','No significant surgical history.','Metformin 500mg',15),(16,'O-','Shellfish','','Appendectomy (2015).','',16),(17,'AB-','','Hyperlipidemia','No significant surgical history.','',17),(18,'B+','Shellfish','','No significant surgical history.','',18),(19,'AB+','','Type 2 diabetes','Appendectomy (2015).','Metformin 500mg',19),(20,'unknown','','','No significant surgical history.','Metformin 500mg',20),(21,'A-','Shellfish','','No significant surgical history.','Amlodipine 5mg',21),(22,'A-','Shellfish','Asthma','Appendectomy (2015).','',22),(23,'unknown','Penicillin','','No significant surgical history.','Metformin 500mg',23),(24,'AB+','','Hypertension','No significant surgical history.','Amlodipine 5mg',24),(25,'O+','Penicillin','Asthma','Appendectomy (2015).','Metformin 500mg',25);
/*!40000 ALTER TABLE `patients_medicalinformation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_patient`
--

DROP TABLE IF EXISTS `patients_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients_patient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `middle_name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `civil_status` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nationality` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `profile_picture` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `province` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `zip_code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_archived` tinyint(1) NOT NULL,
  `registered_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `registered_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patient_id` (`patient_id`),
  KEY `patients_patient_registered_by_id_5e584461_fk_accounts_` (`registered_by_id`),
  KEY `patients_patient_status_0047d831` (`status`),
  KEY `patients_patient_is_archived_58e98552` (`is_archived`),
  KEY `patients_patient_registered_at_fb5fa4ed` (`registered_at`),
  CONSTRAINT `patients_patient_registered_by_id_5e584461_fk_accounts_` FOREIGN KEY (`registered_by_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_patient`
--

LOCK TABLES `patients_patient` WRITE;
/*!40000 ALTER TABLE `patients_patient` DISABLE KEYS */;
INSERT INTO `patients_patient` VALUES (1,'PAT-2026-00001','Juan','Santos','Dela Cruz','1990-06-17','M','single','Filipino','','09981836553','juan.delacruz@example.com','275 Rizal Street','Cebu City','Cebu','6000','admitted',0,'2026-08-02 03:46:12.715404','2026-11-17 04:46:12.719075',2),(2,'PAT-2026-00002','Maria','','Santos','1976-06-11','F','single','Filipino','','09987825707','maria.santos@example.com','290 Rizal Street','Manila','Metro Manila','1000','admitted',0,'2026-06-28 02:46:12.715404','2026-11-17 04:46:12.724023',2),(3,'PAT-2026-00003','Jose','M.','Reyes','2012-12-09','M','divorced','Filipino','','09431229838','jose.reyes@example.com','287 Rizal Street','Cebu City','Cebu','6000','admitted',0,'2026-06-26 04:46:12.715404','2026-11-17 04:46:12.728023',2),(4,'PAT-2026-00004','Ana','Santos','Garcia','1981-05-06','F','widowed','Filipino','','09599936196','ana.garcia@example.com','300 Rizal Street','Baguio','Benguet','2600','admitted',0,'2026-06-23 00:46:12.715404','2026-11-17 04:46:12.731717',3),(5,'PAT-2026-00005','Carlo','M.','Mendoza','1947-05-15','F','separated','Filipino','','09409170818','carlo.mendoza@example.com','38 Rizal Street','Baguio','Benguet','2600','admitted',0,'2026-11-06 18:46:12.715404','2026-11-17 04:46:12.735614',2),(6,'PAT-2026-00006','Liza','Lopez','Torres','1995-05-14','F','divorced','Filipino','','09633300498','liza.torres@example.com','297 Rizal Street','Quezon City','Metro Manila','1100','discharged',0,'2026-11-01 17:46:12.715404','2026-11-17 04:46:12.739976',3),(7,'PAT-2026-00007','Miguel','Lopez','Ramos','1967-10-28','F','widowed','Filipino','','09869473236','miguel.ramos@example.com','198 Rizal Street','Iloilo City','Iloilo','5000','discharged',0,'2026-11-02 01:46:12.715404','2026-11-17 04:46:12.744067',3),(8,'PAT-2026-00008','Rosa','Santos','Flores','1959-08-22','M','separated','Filipino','','09519779047','rosa.flores@example.com','255 Rizal Street','Cebu City','Cebu','6000','discharged',0,'2026-06-30 00:46:12.715404','2026-11-17 04:46:12.748175',2),(9,'PAT-2026-00009','Paolo','M.','Aquino','1993-09-10','F','married','Filipino','','09262050095','paolo.aquino@example.com','43 Rizal Street','Iloilo City','Iloilo','5000','discharged',0,'2026-09-11 00:46:12.715404','2026-11-17 04:46:12.752215',2),(10,'PAT-2026-00010','Grace','Santos','Bautista','1988-04-17','F','divorced','Filipino','','09708104260','grace.bautista@example.com','164 Rizal Street','Quezon City','Metro Manila','1100','discharged',0,'2026-08-09 03:46:12.715404','2026-11-17 04:46:12.755919',2),(11,'PAT-2026-00011','Ramon','M.','Villanueva','2020-04-18','M','single','Filipino','','09324157762','ramon.villanueva@example.com','226 Rizal Street','Davao City','Davao del Sur','8000','discharged',0,'2026-07-03 03:46:12.715404','2026-11-17 04:46:12.759957',2),(12,'PAT-2026-00012','Isabel','','Castillo','2019-07-28','M','divorced','Filipino','','09503973202','isabel.castillo@example.com','77 Rizal Street','Cebu City','Cebu','6000','active',0,'2026-07-17 21:46:12.715404','2026-11-17 04:46:12.764091',3),(13,'PAT-2026-00013','Andres','','Navarro','2012-12-13','M','widowed','Filipino','','09894946073','andres.navarro@example.com','136 Rizal Street','Cebu City','Cebu','6000','active',0,'2026-10-10 17:46:12.715404','2026-11-17 04:46:12.767845',3),(14,'PAT-2026-00014','Teresa','','Domingo','1957-11-12','F','single','Filipino','','09847535601','teresa.domingo@example.com','134 Rizal Street','Baguio','Benguet','2600','active',0,'2026-09-20 19:46:12.715404','2026-11-17 04:46:12.771420',3),(15,'PAT-2026-00015','Luis','Santos','Aguilar','1952-06-18','F','married','Filipino','','09314660300','luis.aguilar@example.com','266 Rizal Street','Manila','Metro Manila','1000','active',0,'2026-08-20 21:46:12.715404','2026-11-17 04:46:12.775030',3),(16,'PAT-2026-00016','Carmen','Lopez','Pascual','1993-03-02','M','married','Filipino','','09209690402','carmen.pascual@example.com','117 Rizal Street','Iloilo City','Iloilo','5000','active',0,'2026-07-17 18:46:12.715404','2026-11-17 04:46:12.778864',3),(17,'PAT-2026-00017','Daniel','','Soriano','1951-01-01','M','separated','Filipino','','09939991324','daniel.soriano@example.com','103 Rizal Street','Cebu City','Cebu','6000','active',0,'2026-07-21 22:46:12.715404','2026-11-17 04:46:12.782563',3),(18,'PAT-2026-00018','Elena','','Fernandez','1960-11-08','M','married','Filipino','','09236406413','elena.fernandez@example.com','15 Rizal Street','Iloilo City','Iloilo','5000','active',0,'2026-08-20 02:46:12.715404','2026-11-17 04:46:12.786235',2),(19,'PAT-2026-00019','Rafael','Santos','Salazar','2023-12-17','M','single','Filipino','','09665412094','rafael.salazar@example.com','72 Rizal Street','Baguio','Benguet','2600','active',0,'2026-06-19 23:46:12.715404','2026-11-17 04:46:12.790096',3),(20,'PAT-2026-00020','Sofia','M.','Valdez','1951-01-16','M','single','Filipino','','09894485254','sofia.valdez@example.com','182 Rizal Street','Cebu City','Cebu','6000','active',0,'2026-07-05 20:46:12.715404','2026-11-17 04:46:12.794039',3),(21,'PAT-2026-00021','Gabriel','M.','Rivera','1956-03-20','M','divorced','Filipino','','09104222468','gabriel.rivera@example.com','77 Rizal Street','Quezon City','Metro Manila','1100','active',0,'2026-07-07 20:46:12.715404','2026-11-17 04:46:12.797968',2),(22,'PAT-2026-00022','Lourdes','M.','Tolentino','1955-07-09','M','divorced','Filipino','','09161012773','lourdes.tolentino@example.com','128 Rizal Street','Baguio','Benguet','2600','active',0,'2026-10-31 21:46:12.715404','2026-11-17 04:46:12.801688',2),(23,'PAT-2026-00023','Mateo','Santos','Manalo','1963-09-25','F','separated','Filipino','','09645628515','mateo.manalo@example.com','274 Rizal Street','Cebu City','Cebu','6000','active',0,'2026-07-26 02:46:12.715404','2026-11-17 04:46:12.805356',3),(24,'PAT-2026-00024','Angela','','Cruz','1990-09-06','F','widowed','Filipino','','09177895777','angela.cruz@example.com','124 Rizal Street','Davao City','Davao del Sur','8000','active',0,'2026-10-12 00:46:12.715404','2026-11-17 04:46:12.809009',3),(25,'PAT-2026-00025','Victor','M.','Lim','2006-03-07','M','separated','Filipino','','09623192278','victor.lim@example.com','84 Rizal Street','Manila','Metro Manila','1000','active',0,'2026-08-17 23:46:12.715404','2026-11-17 04:46:12.812926',2);
/*!40000 ALTER TABLE `patients_patient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-17  4:46:46
