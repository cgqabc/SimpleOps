
--
-- 数据库: `OManager`
--

-- --------------------------------------------------------

--
-- 表的结构 `upgrade`
--
use OManager;
CREATE TABLE IF NOT EXISTS `upgrade` (
  `version` char(5) NOT NULL DEFAULT '' COMMENT '最新版本号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统升级表';

--
-- 转存表中的数据 `upgrade`
--

INSERT INTO `upgrade` (`version`) VALUES
('10026');

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `admin` char(20) NOT NULL DEFAULT '' COMMENT '管理员帐号',
  `passwd` char(32) NOT NULL DEFAULT '' COMMENT '管理员密码',
  `Privatekey` char(32) NOT NULL DEFAULT '' COMMENT '私钥MD5',
  `privileges` char(62) NOT NULL COMMENT '权限角色',
  PRIMARY KEY (`admin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表';

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`admin`, `passwd`, `Privatekey`, `privileges`) VALUES
('demo', 'e10adc3949ba59abbe56e057f20f883e', 'dced4ca98819e25a3ebcc939d5c21378', '1,2,3,5,6'),
('root', 'e10adc3949ba59abbe56e057f20f883e', '8115082536da7863426017e0248bf3a8', 'root');

-- --------------------------------------------------------

--
-- 表的结构 `user_logs`
--

CREATE TABLE IF NOT EXISTS `user_logs` (
  `id` int(5) NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user` char(10) NOT NULL COMMENT '管理员帐号',
  `event` char(255) NOT NULL COMMENT '操作事件',
  `Datatime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '操作日期',
  PRIMARY KEY (`id`),
  KEY `Datatime` (`Datatime`),
  KEY `USER_NID` (`user`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='操作日志表' AUTO_INCREMENT=261 ;

--
-- 转存表中的数据 `user_logs`
--

INSERT INTO `user_logs` (`id`, `user`, `event`, `Datatime`) VALUES
(1, 'root', '登录系统    IP:192.168.56.1', '2014-07-03 16:25:10'),
(2, 'root', '操作对象：192.168.1.21,192.168.1.22-操作MID:1002', '2014-07-03 16:25:26'),
(3, 'root', '退出系统    IP:192.168.56.1', '2014-07-03 16:25:32'),
(4, 'root', '登录系统    IP:192.168.56.1', '2014-07-03 23:29:10'),
(5, 'root', '退出系统    IP:192.168.56.1', '2014-07-03 23:29:13'),
(6, 'root', '登录系统    IP:192.168.56.1', '2014-07-03 23:29:26'),
(7, 'root', '退出系统    IP:192.168.56.1', '2014-07-03 23:29:33'),
(8, 'root', '登录系统    IP:192.168.56.1', '2014-07-03 23:29:52'),
(9, 'root', '操作对象：192.168.1.21-操作MID:1006', '2014-07-03 23:30:42'),
(10, 'root', '退出系统    IP:192.168.56.1', '2014-07-03 23:31:49'),
(11, 'root', '登录系统    IP:192.168.56.1', '2014-07-03 23:32:05'),
(12, 'root', '操作对象：192.168.1.21,192.168.1.22-操作MID:3400', '2014-07-03 23:32:20'),
(13, 'root', '退出系统    IP:192.168.56.1', '2014-07-03 23:32:46'),
(14, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 12:50:53'),
(15, 'root', '操作对象：192.168.1.21,192.168.1.22-操作MID:1001', '2014-07-04 12:51:29'),
(16, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:05:58'),
(17, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:06:10'),
(18, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:06:41'),
(19, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:06:50'),
(20, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:08:35'),
(21, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:08:43'),
(22, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:09:03'),
(23, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:09:47'),
(24, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:10:51'),
(25, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:10:59'),
(26, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:13:28'),
(27, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:13:36'),
(28, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:21:49'),
(29, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:21:59'),
(30, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:22:07'),
(31, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:27:11'),
(32, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:27:40'),
(33, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:28:50'),
(34, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:28:59'),
(35, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:33:19'),
(36, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:34:56'),
(37, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:35:04'),
(38, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:35:14'),
(39, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:37:21'),
(40, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:37:47'),
(41, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:40:27'),
(42, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:42:41'),
(43, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:42:48'),
(44, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:43:02'),
(45, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:45:25'),
(46, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:45:55'),
(47, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:47:47'),
(48, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:48:03'),
(49, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:49:37'),
(50, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:51:10'),
(51, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:51:20'),
(52, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:51:29'),
(53, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:52:30'),
(54, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:52:47'),
(55, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:54:01'),
(56, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 13:54:23'),
(57, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 13:57:37'),
(58, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 14:04:27'),
(59, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 14:04:40'),
(60, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 14:05:20'),
(61, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 14:07:37'),
(62, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 14:09:02'),
(63, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 14:18:26'),
(64, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 14:18:59'),
(65, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 14:24:12'),
(66, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 14:24:32'),
(67, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 14:25:47'),
(68, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 14:26:03'),
(69, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 14:26:34'),
(70, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 14:26:39'),
(71, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 14:27:59'),
(72, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 14:30:55'),
(73, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 14:31:04'),
(74, 'root', '操作对象：192.168.1.21-操作MID:1001', '2014-07-04 14:31:32'),
(75, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 14:31:50'),
(76, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 15:10:53'),
(77, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 15:12:45'),
(78, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 15:14:38'),
(79, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 15:17:33'),
(80, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 15:18:38'),
(81, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 15:19:15'),
(82, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 15:29:06'),
(83, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 15:30:18'),
(84, 'root', '登录系统    IP:192.168.56.1', '2014-07-04 15:36:51'),
(85, 'root', '操作对象：192.168.1.21,192.168.1.22-操作MID:1003', '2014-07-04 15:37:26'),
(86, 'root', '退出系统    IP:192.168.56.1', '2014-07-04 15:38:07'),
(87, 'root', '登录系统    IP:192.168.56.1', '2014-07-05 02:29:49'),
(88, 'root', '操作对象：192.168.1.21,192.168.1.22-操作MID:1003', '2014-07-05 02:31:53'),
(89, 'root', '退出系统    IP:192.168.56.1', '2014-07-05 02:37:51'),
(90, 'root', '登录系统    IP:192.168.56.1', '2014-07-05 07:16:29'),
(91, 'root', '操作对象：192.168.1.21,192.168.1.22-操作MID:1006', '2014-07-05 07:17:06'),
(92, 'root', '操作对象：192.168.1.21,192.168.1.22-操作MID:1003', '2014-07-05 07:17:23'),
(93, 'root', '退出系统    IP:192.168.56.1', '2014-07-05 07:20:08');

--
-- 限制导出的表
--

--
-- 限制表 `user_logs`
--
ALTER TABLE `user_logs`
  ADD CONSTRAINT `user_logs_ibfk_1` FOREIGN KEY (`user`) REFERENCES `users` (`admin`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
