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
-- Database: `cart`
--
CREATE DATABASE IF NOT EXISTS `cart` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `cart`;


-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `order_id` int(10) NOT NULL,
  `booking_id` int(10) NOT NULL,
  `item_id` varchar(10) NOT NULL,
  `fb_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `rs_quantity` int(5) NOT NULL,
  `price` double(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`order_id`, `booking_id`, `item_id`, `fb_datetime`, `rs_quantity`, `price`) VALUES
(1, 1, 'item1', '2021-03-20 05:10:19', 1, 100.20),
(2, 2, 'item1', '2021-03-20 05:29:22', 2, 3.00);
(3, 1, 'item2', '2021-03-20 05:51:00', 1, 200.49),

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`order_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `order_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
