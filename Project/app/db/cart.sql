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

DROP TABLE IF EXISTS `cart`;
CREATE TABLE IF NOT EXISTS `cart` (
  `order_id` int(10) NOT NULL,
  `booking_id` int(10) NOT NULL,
  `item_id` varchar(10) NOT NULL,
  `order_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `rs_quantity` int(5) NULL DEFAULT NULL,
  `price` double(10,2) NULL DEFAULT NULL,
  `rs_delivered_status` boolean NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`order_id`, `booking_id`, `item_id`, `order_datetime`, `rs_quantity`, `price`, `rs_delivered_status`) VALUES
(1, 1, 'fb_1', CURRENT_TIMESTAMP, null, null, null),
(2, 2, 'rs_1', CURRENT_TIMESTAMP, 2, 3.00, FALSE),
(3, 1, 'fb_2', CURRENT_TIMESTAMP, null, null, null);

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
