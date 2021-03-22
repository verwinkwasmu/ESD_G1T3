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
-- Database: `facility`
--
CREATE DATABASE IF NOT EXISTS `facility` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `facility`;


-- --------------------------------------------------------

--
-- Table structure for table `facility`
--

DROP TABLE IF EXISTS `facility`;
CREATE TABLE IF NOT EXISTS `facility` (
  `item_id` varchar(10) NOT NULL,
  `item_name` varchar(10) NOT NULL,
  `item_price` double(10,2) NOT NULL,
  `max_capacity` int(10) NOT NULL,
  `item_desc` varchar(10) NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `facility`
--

INSERT INTO `facility` (`item_id`, `item_name`, `item_price`, `max_capacity`, `item_desc`) VALUES
('fb_1', "Gym", 5, 5, "A fully-equipped Gym for hotel guests"),
('fb_2', "Balcony", 3.00, 5, "Enjoy"),

--
-- Indexes for dumped tables
--

--
-- Indexes for table `facility`
--
ALTER TABLE `facility`
  ADD PRIMARY KEY (`item_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
