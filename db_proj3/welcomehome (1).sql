-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- 主机： localhost:3306
-- 生成日期： 2024-12-10 21:39:51
-- 服务器版本： 5.7.24
-- PHP 版本： 8.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `welcomehome`
--

-- --------------------------------------------------------

--
-- 表的结构 `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(2, 'bed'),
(1, 'chair'),
(5, 'closet'),
(3, 'desk'),
(4, 'lamp'),
(7, 'sofa'),
(6, 'TV');

-- --------------------------------------------------------

--
-- 表的结构 `customer_service`
--

CREATE TABLE `customer_service` (
  `cid` int(11) NOT NULL,
  `sLid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `datas`
--

CREATE TABLE `datas` (
  `dataid` int(11) NOT NULL,
  `deviceid` int(11) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  `eventLabel` varchar(20) NOT NULL,
  `value` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `device`
--

CREATE TABLE `device` (
  `deviceid` int(11) NOT NULL,
  `type` varchar(100) NOT NULL,
  `modelid` int(11) DEFAULT NULL,
  `SLid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `items`
--

CREATE TABLE `items` (
  `itemId` int(11) NOT NULL,
  `description` varchar(200) NOT NULL,
  `price` float NOT NULL,
  `stockQuantity` int(11) NOT NULL,
  `donator` varchar(100) DEFAULT NULL,
  `ordered` tinyint(1) NOT NULL DEFAULT '0',
  `categoryId` int(11) DEFAULT NULL,
  `location` varchar(50) NOT NULL DEFAULT 'stock'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `items`
--

INSERT INTO `items` (`itemId`, `description`, `price`, `stockQuantity`, `donator`, `ordered`, `categoryId`, `location`) VALUES
(1, 'chair', 100, 1, 'test', 1, 1, 'stock'),
(2, 'bed', 200, 1, 'test', 1, 2, 'stock'),
(3, 'bed', 200, 1, 'test', 1, 2, 'stock'),
(4, 'lamp', 20, 1, 'test', 0, 4, 'stock'),
(5, 'chair', 200, 2, 'test', 0, NULL, 'stock');

-- --------------------------------------------------------

--
-- 表的结构 `model`
--

CREATE TABLE `model` (
  `modelid` int(11) NOT NULL,
  `modeltype` varchar(50) NOT NULL,
  `modelname` varchar(50) NOT NULL,
  `properties` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `orderitems`
--

CREATE TABLE `orderitems` (
  `orderId` int(11) NOT NULL,
  `itemId` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `category` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `orderitems`
--

INSERT INTO `orderitems` (`orderId`, `itemId`, `quantity`, `category`) VALUES
(15, 1, 1, 'chair'),
(16, 2, 1, 'bed'),
(17, 3, 1, 'bed');

-- --------------------------------------------------------

--
-- 表的结构 `orders`
--

CREATE TABLE `orders` (
  `orderId` int(11) NOT NULL,
  `customerId` varchar(255) DEFAULT NULL,
  `orderDate` datetime NOT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `orders`
--

INSERT INTO `orders` (`orderId`, `customerId`, `orderDate`, `status`) VALUES
(2, '1', '2024-12-09 22:16:26', 'start'),
(3, '1', '2024-12-09 22:20:08', 'start'),
(4, '1', '2024-12-10 01:37:09', 'start'),
(5, '1', '2024-12-10 01:40:09', 'start'),
(6, '2', '2024-12-10 01:49:18', 'start'),
(7, '3', '2024-12-10 02:07:54', 'start'),
(8, '4', '2024-12-10 02:13:17', 'start'),
(9, '1', '2024-12-10 02:26:03', 'start'),
(10, '1', '2024-12-10 02:39:37', 'start'),
(11, '1', '2024-12-10 02:57:31', 'start'),
(12, '1', '2024-12-10 02:58:17', 'start'),
(13, '1', '2024-12-10 02:59:42', 'start'),
(14, '2', '2024-12-10 03:00:42', 'start'),
(15, '1', '2024-12-10 03:13:56', 'start'),
(16, '2', '2024-12-10 03:14:32', 'start'),
(17, 'Matty', '2024-12-10 16:17:54', 'start');

-- --------------------------------------------------------

--
-- 表的结构 `price`
--

CREATE TABLE `price` (
  `fromtime` time NOT NULL,
  `endtime` time NOT NULL,
  `zipcode` int(11) NOT NULL,
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `servicelocation`
--

CREATE TABLE `servicelocation` (
  `sLid` int(11) NOT NULL,
  `addr` varchar(50) NOT NULL,
  `zipcode` int(11) NOT NULL,
  `unitNumber` varchar(20) NOT NULL,
  `tookOverDate` date NOT NULL,
  `squareFootage` int(11) NOT NULL,
  `bedroomCnt` int(11) NOT NULL,
  `occupantsCnt` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `cid` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `billAddr` varchar(4000) NOT NULL,
  `role` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`cid`, `first_name`, `last_name`, `username`, `password`, `billAddr`, `role`) VALUES
(3, 'Han', 'Wen', 'Han Wen', 'scrypt:32768:8:1$Wli8Yf44JcGGWkwd$bd1a3fedf65e597e7ef6807b827936b41a6e06bc52afa0edf0d6ab2a7fcb5208529baaf327ac8988789e4c45589a572406c2f02a8df221fafca4d0baa630c7d0', 'Tandon', 'staff'),
(4, 'v', 'test', 'vtest', 'scrypt:32768:8:1$Nswfp6jx7ihpRm4Q$6e14fb8dc4e1dfa7a2184438c8b9ac118e86de987a4b74592699bdb3b397fc48749ebb190b809a72f5db4ec20c3cad4393bb7dabdcf2ee5b316ae2c71a92eb88', 'test', 'volunteer'),
(5, 't', 'est', 'test', 'scrypt:32768:8:1$EJbYWiMgh9HTH7Zt$4e2db1eb6e9c36b85a78d01f8d5c6f5227ee4a4036a1eeb3fa89733b3da724415fd408edbe242749119cace191730f934b534893590061ec04091007be8baa98', 'secret', 'volunteer');

--
-- 转储表的索引
--

--
-- 表的索引 `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- 表的索引 `customer_service`
--
ALTER TABLE `customer_service`
  ADD PRIMARY KEY (`cid`,`sLid`),
  ADD KEY `sLid` (`sLid`);

--
-- 表的索引 `datas`
--
ALTER TABLE `datas`
  ADD PRIMARY KEY (`dataid`),
  ADD KEY `deviceid` (`deviceid`);

--
-- 表的索引 `device`
--
ALTER TABLE `device`
  ADD PRIMARY KEY (`deviceid`),
  ADD KEY `modelid` (`modelid`),
  ADD KEY `SLid` (`SLid`);

--
-- 表的索引 `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`itemId`),
  ADD KEY `fk_category` (`categoryId`);

--
-- 表的索引 `model`
--
ALTER TABLE `model`
  ADD PRIMARY KEY (`modelid`);

--
-- 表的索引 `orderitems`
--
ALTER TABLE `orderitems`
  ADD PRIMARY KEY (`orderId`,`itemId`),
  ADD KEY `itemId` (`itemId`);

--
-- 表的索引 `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`orderId`),
  ADD KEY `customerId` (`customerId`);

--
-- 表的索引 `price`
--
ALTER TABLE `price`
  ADD PRIMARY KEY (`fromtime`,`endtime`,`zipcode`);

--
-- 表的索引 `servicelocation`
--
ALTER TABLE `servicelocation`
  ADD PRIMARY KEY (`sLid`);

--
-- 表的索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`cid`),
  ADD UNIQUE KEY `username` (`username`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 使用表AUTO_INCREMENT `datas`
--
ALTER TABLE `datas`
  MODIFY `dataid` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `device`
--
ALTER TABLE `device`
  MODIFY `deviceid` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `items`
--
ALTER TABLE `items`
  MODIFY `itemId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 使用表AUTO_INCREMENT `model`
--
ALTER TABLE `model`
  MODIFY `modelid` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `orders`
--
ALTER TABLE `orders`
  MODIFY `orderId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- 使用表AUTO_INCREMENT `servicelocation`
--
ALTER TABLE `servicelocation`
  MODIFY `sLid` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `cid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 限制导出的表
--

--
-- 限制表 `customer_service`
--
ALTER TABLE `customer_service`
  ADD CONSTRAINT `customer_service_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `user` (`cid`),
  ADD CONSTRAINT `customer_service_ibfk_2` FOREIGN KEY (`sLid`) REFERENCES `servicelocation` (`sLid`);

--
-- 限制表 `datas`
--
ALTER TABLE `datas`
  ADD CONSTRAINT `datas_ibfk_1` FOREIGN KEY (`deviceid`) REFERENCES `device` (`deviceid`);

--
-- 限制表 `device`
--
ALTER TABLE `device`
  ADD CONSTRAINT `device_ibfk_1` FOREIGN KEY (`modelid`) REFERENCES `model` (`modelid`),
  ADD CONSTRAINT `device_ibfk_2` FOREIGN KEY (`SLid`) REFERENCES `servicelocation` (`sLid`);

--
-- 限制表 `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `fk_category` FOREIGN KEY (`categoryId`) REFERENCES `categories` (`id`);

--
-- 限制表 `orderitems`
--
ALTER TABLE `orderitems`
  ADD CONSTRAINT `orderitems_ibfk_1` FOREIGN KEY (`orderId`) REFERENCES `orders` (`orderId`),
  ADD CONSTRAINT `orderitems_ibfk_2` FOREIGN KEY (`itemId`) REFERENCES `items` (`itemId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
