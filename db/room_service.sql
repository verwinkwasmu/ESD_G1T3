-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 21, 2021 at 05:29 AM
-- Server version: 5.7.32
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `room_service`
--
CREATE DATABASE IF NOT EXISTS `room_service` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `room_service`;


-- --------------------------------------------------------

--
-- Table structure for table `room_service`
--

DROP TABLE IF EXISTS `room_service`;
CREATE TABLE IF NOT EXISTS `room_service` (
  `item_id` varchar(10) NOT NULL,
  `item_name` varchar(40) NOT NULL,
  `item_price` float(10,2) NOT NULL,
  `waiting_time` varchar(10) NOT NULL,
  `item_desc` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Dumping data for table `room_service`
--

INSERT INTO `room_service` (`item_id`, `item_name`, `item_price`, `waiting_time`, `item_desc`) VALUES
('rs_1', "Lunch Special", 15, 30, "Cheap and delicious lunch meal special"),
('rs_2', "6 Course Meal", 108, 60, "Exquisite 8 Course Meal prepared by the best chef in Singapore, Mr Verwin Kwa"),
('rs_3', 'Hokkien Mee', 7, 30, "Michellelin Speciality HKM, must try!"), 
('rs_4', 'Ice CreamING x Waffle', 18, 30, "Freshly made Belgium waffles that will make u go woah~!" ), 
('rs_5', 'Japanese Special', 67, 60, "Bringing Japanese Omakase to your doorstep!"), 
('rs_6', 'Afternoon Tea Party', 80, 30, "Tea time for ladies and gents picked by the Queen's righthand men"), 
('rs_7', "Laobu's Nasi Lemak", 20, 30, "Taste better than Punggol Nasi Alamak"), 
('rs_8', 'Spanish Delight', 80, 60, "Hola! Specially picked by Prof Raf J.Barros"), 
('rs_9', 'Italian Talent', 70, 30, "Don't be upsetti! Get spagetti!");

--
-- Indexes for dumped tables
--

--
-- Indexes for table `room_service`
--
ALTER TABLE `room_service`
  ADD PRIMARY KEY (`item_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
