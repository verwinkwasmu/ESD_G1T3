-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Mar 20, 2021 at 05:29 AM
-- Server version: 5.7.32
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `booking`
--
CREATE DATABASE IF NOT EXISTS `booking` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `booking`;


-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
CREATE TABLE IF NOT EXISTS `booking` (
  `booking_id` int(10) NOT NULL,
  `guest_name` varchar(40) NOT NULL,
  `nric_passportno` varchar(40) NOT NULL,
  `email` varchar(40) NOT NULL,
  -- to keep stay_duration or not...
  `stay_duration` varchar(40) NOT NULL,
  `room_number` varchar(10) NOT NULL,
  `room_price` double(10,2) NOT NULL,
  `checkin_status` BOOLEAN NOT NULL,
  `checkout_status` BOOLEAN NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`booking_id`, `guest_name`, `nric_passportno`, `email`, `stay_duration`, `room_number`, `room_price`, `checkin_status`,`checkout_status`) VALUES
(1, "Jessie", "S9920937I", "jessie@gmail.com", "14 March-18 March 2021", "A800", 299.99, TRUE, TRUE), 
(1, "James", "S9920347I", "james@gmail.com", "21 March- 23 March 2021", "A801", 299.99, TRUE, FALSE), 


--
-- Indexes for dumped tables
--

--
-- Indexes for table booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`booking_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
