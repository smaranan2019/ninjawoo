SET time_zone = "+08:00";

CREATE DATABASE IF NOT EXISTS nv_jolibeee DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE nv_jolibeee;


DROP TABLE IF EXISTS driver;
CREATE TABLE IF NOT EXISTS driver (
  `driver_id` int(11) NOT NULL AUTO_INCREMENT,
  `driver_hp` int(11) NOT NULL,
  `driver_tele_handle` varchar(100),
  `driver_date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `driver_date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`driver_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO driver (`driver_id`, `driver_hp`, `driver_tele_handle`, `driver_date_created`, `driver_date_modified`) VALUES
(1, 98292466, 'jumpingjujubee', '2020-06-12 02:14:55', '2020-06-12 02:14:55'),
(3, 92732335, 'frances_s', '2020-06-12 02:14:55', '2020-06-12 02:14:55'),
(5, 83056389, null, '2020-06-12 02:14:55', '2020-06-12 02:14:55');


DROP TABLE IF EXISTS package;
CREATE TABLE IF NOT EXISTS package (
  `tracking_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) NOT NULL,
  `cusomter_address` varchar(100) NOT NULL,
  `shipper_name` varchar(100) NOT NULL,
  `shipper_address` varchar(100) NOT NULL,
  `package_status` varchar(100) NOT NULL DEFAULT 'PENDING PICKUP',
  `package_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `package_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`tracking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO package (`tracking_id`, `customer_name`, `cusomter_address`, `shipper_name`, `shipper_address`, 
					`package_status`) VALUES
(1, 'Angelica Skyler', '32 Smith Road, #04-23, S112233', 'Alexander Hamilton', '65 Applebee, #23-52, S734483', 
'PENDING PICKUP'),
(3, 'Angelica Skyler', '32 Smith Road, #04-23, S112233', 'Alexander Hamilton', '65 Applebee, #23-52, S734483', 
'PENDING PICKUP');

DROP TABLE IF EXISTS driver_package;
CREATE TABLE IF NOT EXISTS driver_package (
  `driver_package_id` int(11) AUTO_INCREMENT,
  `tracking_id` int(11) NOT NULL,
  `driver_id` int(11) NOT NULL,
  `package_pickup_date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `package_pickup_date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`driver_package_id`),
  CONSTRAINT driver_package_fk1 FOREIGN KEY (driver_id) references driver(driver_id),
  CONSTRAINT driver_package_fk2 FOREIGN KEY (tracking_id) references package(tracking_id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO driver_package (`driver_package_id`, `tracking_id`, `driver_id`) VALUES
(1, 1, 1),
(3, 3, 1);

UPDATE package SET `package_status` = 'PENDING DELIVERY' WHERE `tracking_id` = 1;
UPDATE package SET `package_status` = 'PENDING DELIVERY' WHERE `tracking_id` = 3;

DROP TABLE IF EXISTS remarks;
CREATE TABLE IF NOT EXISTS remarks (
  `remark_id` int(11) NOT NULL AUTO_INCREMENT,
  `driver_id` int(11) NOT NULL,
  `remark_problem_description` text NOT NULL,
  `estimated_delay_day` int(10),
  `estimated_delay_hour` int(10),
  `estimated_delay_minute` int(10),
  `remark_date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `remark_date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`remark_id`),
  CONSTRAINT remark_fk FOREIGN KEY (driver_id) references driver(driver_id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO remarks (`remark_id`, `driver_id`, `remark_problem_description`, `estimated_delay_day`, `estimated_delay_hour`,
						`estimated_delay_minute`) VALUES
(1, 1, 'Leaving early, Im picking up my daughter', 1, 0, 0),
(3, 1, 'Still stuck in the jam soz', 0, 1, 0);

select * from remarks;