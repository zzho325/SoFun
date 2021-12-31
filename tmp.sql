2021-06-22 TABLE MyGuests (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
firstname VARCHAR(30) NOT NULL,
lastname VARCHAR(30) NOT NULL,
email VARCHAR(50),
reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP


create table book_info
(
	ds varchar(10) default '',
	book_id bigint primary key default 0,
	book_name varchar(20) default '',
	book_author varchar(20) default '',
	book_intro varchar(200) default '',
	book_length int default 0,
	book_view_num int default 0, 
	book_comment_num int default 0, 
	book_fav_num int default 0,
	book_tags varchar(50) default '',
	update_time varchar(20) default '',
	create_time varchar(20) default '',
);