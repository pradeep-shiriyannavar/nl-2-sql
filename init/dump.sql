/*
SQLyog - Free MySQL GUI v5.19
Host - 5.5.29 : Database - db_food_management
*********************************************************************
Server version : 5.5.29
*/

SET NAMES utf8;

SET SQL_MODE='';

create database if not exists `db_food_management`;

USE `db_food_management`;

SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO';

/*Table structure for table `m_admin` */

DROP TABLE IF EXISTS `m_admin`;

CREATE TABLE `m_admin` (
  `s_no` int(6) NOT NULL AUTO_INCREMENT,
  `admin_id` varchar(40) NOT NULL,
  `admin_password` varchar(40) NOT NULL,
  `admin_name` varchar(50) NOT NULL,
  `admin_phone` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`s_no`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `m_admin` */

insert into `m_admin` (`s_no`,`admin_id`,`admin_password`,`admin_name`,`admin_phone`) values (1,'admin','admin','namana','9886692401');

/*Table structure for table `m_donor` */

DROP TABLE IF EXISTS `m_donor`;

CREATE TABLE `m_donor` (
  `d_id` int(5) NOT NULL AUTO_INCREMENT,
  `d_username` varchar(20) DEFAULT NULL,
  `d_password` varchar(20) DEFAULT NULL,
  `d_phone_number` varchar(20) DEFAULT NULL,
  `d_email` varchar(30) DEFAULT NULL,
  `d_address` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `m_donor` */

insert into `m_donor` (`d_id`,`d_username`,`d_password`,`d_phone_number`,`d_email`,`d_address`) values (8,'ram','1234','7760433598','namanabl13@gmail.com','jayanagar'),(9,'Kiran ','1234','7338345250','namanabl13@gmail.com','Jayanagar ');

/*Table structure for table `m_food_category` */

DROP TABLE IF EXISTS `m_food_category`;

CREATE TABLE `m_food_category` (
  `c_id` int(10) NOT NULL AUTO_INCREMENT,
  `c_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `m_food_category` */

insert into `m_food_category` (`c_id`,`c_name`) values (1,'Veg Food'),(2,'Non Veg Food'),(3,'Jain Food');

/*Table structure for table `m_food_trans` */

DROP TABLE IF EXISTS `m_food_trans`;

CREATE TABLE `m_food_trans` (
  `ft_trans` int(10) NOT NULL AUTO_INCREMENT,
  `ft_date` varchar(20) NOT NULL,
  `d_id` int(10) NOT NULL,
  `c_id` int(10) DEFAULT NULL,
  `ft_details` varchar(60) NOT NULL,
  `ft_remark` varchar(50) NOT NULL,
  `ft_longitude` varchar(30) NOT NULL,
  `ft_latitude` varchar(30) NOT NULL,
  `ft_status` char(10) NOT NULL DEFAULT 'open',
  `s_id` int(10) DEFAULT NULL,
  `v_code` int(10) NOT NULL,
  `ft_delivery` char(20) NOT NULL DEFAULT 'in process',
  `dist` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ft_trans`),
  KEY `v_code` (`v_code`),
  KEY `d_id` (`d_id`),
  KEY `c_id` (`c_id`),
  KEY `s_id` (`s_id`),
  CONSTRAINT `m_food_trans_ibfk_1` FOREIGN KEY (`v_code`) REFERENCES `m_volunteer` (`v_code`),
  CONSTRAINT `m_food_trans_ibfk_2` FOREIGN KEY (`d_id`) REFERENCES `m_donor` (`d_id`),
  CONSTRAINT `m_food_trans_ibfk_3` FOREIGN KEY (`c_id`) REFERENCES `m_food_category` (`c_id`),
  CONSTRAINT `m_food_trans_ibfk_4` FOREIGN KEY (`s_id`) REFERENCES `m_seeker` (`s_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;

/*Data for the table `m_food_trans` */

insert into `m_food_trans` (`ft_trans`,`ft_date`,`d_id`,`c_id`,`ft_details`,`ft_remark`,`ft_longitude`,`ft_latitude`,`ft_status`,`s_id`,`v_code`,`ft_delivery`,`dist`) values (15,'15/06/2022',9,2,'Biryani','20','12.9321963','77.583828','Closed',8,25,'Delivered','0.0391'),(16,'15/06/2022',9,2,'Biryani','20','12.9321963','77.583828','open',NULL,26,'in process','0.03604'),(17,'15/06/2022',9,2,'Biryani','20','12.9321963','77.583828','open',NULL,27,'in process','0.03604'),(18,'15/06/2022',9,2,'Biryani','20','12.9321963','77.583828','open',NULL,28,'in process','0.03882'),(19,'20/10/2024',8,1,'Rice','2','12.931859','77.5835287','Closed',8,25,'in process','0.01325'),(20,'20/10/2024',8,1,'Rice','2','12.931859','77.5835287','open',NULL,26,'in process','0.01384'),(21,'20/10/2024',8,1,'Rice','2','12.931859','77.5835287','open',NULL,27,'in process','0.01384'),(22,'20/10/2024',8,1,'Rice','2','12.931859','77.5835287','open',NULL,28,'in process','0.01077'),(23,'20/10/2024',8,1,'Rice','2','12.931859','77.5835287','open',NULL,32,'in process','0.01077'),(24,'20/10/2024',8,3,'Rice','2','12.931859','77.5835287','open',NULL,25,'in process','0.01325'),(25,'20/10/2024',8,3,'Rice','2','12.931859','77.5835287','open',NULL,26,'in process','0.01384'),(26,'20/10/2024',8,3,'Rice','2','12.931859','77.5835287','open',NULL,27,'in process','0.01384'),(27,'20/10/2024',8,3,'Rice','2','12.931859','77.5835287','open',NULL,28,'in process','0.01077'),(28,'20/10/2024',8,3,'Rice','2','12.931859','77.5835287','open',NULL,32,'Delivered','0.01077');

/*Table structure for table `m_seeker` */

DROP TABLE IF EXISTS `m_seeker`;

CREATE TABLE `m_seeker` (
  `s_id` int(5) NOT NULL AUTO_INCREMENT,
  `s_username` varchar(20) DEFAULT NULL,
  `s_password` varchar(20) DEFAULT NULL,
  `s_phone_number` varchar(20) DEFAULT NULL,
  `s_email` varchar(30) DEFAULT NULL,
  `s_locality` varchar(20) DEFAULT NULL,
  `s_address` varchar(200) DEFAULT NULL,
  `s_longitude` varchar(30) DEFAULT NULL,
  `s_latitude` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `m_seeker` */

insert into `m_seeker` (`s_id`,`s_username`,`s_password`,`s_phone_number`,`s_email`,`s_locality`,`s_address`,`s_longitude`,`s_latitude`) values (7,'kumar','1234','7760433598','namanabl13@gmail.com','blr','jayanagar','1122.9318545','77.5835128'),(8,'Raju','1234','7760433598','namanabl13@gmail.com','Blr','jayanagar ','12.9318723','77.583525');

/*Table structure for table `m_volunteer` */

DROP TABLE IF EXISTS `m_volunteer`;

CREATE TABLE `m_volunteer` (
  `v_code` int(10) NOT NULL AUTO_INCREMENT,
  `v_id` varchar(50) NOT NULL,
  `v_pass` varchar(50) DEFAULT NULL,
  `v_contact_person` varchar(50) DEFAULT NULL,
  `v_orgname` varchar(80) DEFAULT NULL,
  `v_addr` varchar(70) DEFAULT NULL,
  `v_city` varchar(50) DEFAULT NULL,
  `v_area` varchar(60) DEFAULT NULL,
  `v_pincode` decimal(20,0) DEFAULT NULL,
  `v_phone` decimal(20,0) DEFAULT NULL,
  `v_email` varchar(50) DEFAULT NULL,
  `v_longitude` varchar(30) DEFAULT NULL,
  `v_latitude` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`v_code`,`v_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;

/*Data for the table `m_volunteer` */

insert into `m_volunteer` (`v_code`,`v_id`,`v_pass`,`v_contact_person`,`v_orgname`,`v_addr`,`v_city`,`v_area`,`v_pincode`,`v_phone`,`v_email`,`v_longitude`,`v_latitude`) values (25,'neha','1234','neha','ashraya','jaynagar','blr','jayanagar','560010','7760433598','namanabl13@gmail.com','12.931977','77.583546'),(26,'nita','1234','nita','Ashraya','Jayanagar','Bengaluru','Bengaluru South','560010','7760433598','namanabl13@gmail.com','12.931966','77.583594'),(27,'nita','1234','nita','Ashraya','Jayanagar','Bengaluru','Bengaluru South','560010','7760433598','namanabl13@gmail.com','12.931966','77.583594'),(28,'2003','1234','Shiva','Ashraya','Jayanagar','Blr','Jayanagar','560010','7760433598','namanabl13@gmail.com','12.931932','77.583594'),(32,'pradee','pradee','pradee','DDDDD','Bengaluru','Bengaluru','Jayangar','560022','8545464544','pradeepshiriyannavar@gmail.com','12.931932','77.583594');

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
