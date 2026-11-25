-- Run this in MySQL Workbench (File > Open SQL Script, then click the lightning bolt).
-- Connect as root first. It creates the database and a dedicated user for the app.

CREATE DATABASE IF NOT EXISTS hms_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'hms_user'@'localhost' IDENTIFIED BY 'Hms@12345';
CREATE USER IF NOT EXISTS 'hms_user'@'127.0.0.1' IDENTIFIED BY 'Hms@12345';

GRANT ALL PRIVILEGES ON hms_db.* TO 'hms_user'@'localhost';
GRANT ALL PRIVILEGES ON hms_db.* TO 'hms_user'@'127.0.0.1';
-- needed only for `python manage.py test`
GRANT ALL PRIVILEGES ON `test\_hms\_db`.* TO 'hms_user'@'localhost';
GRANT ALL PRIVILEGES ON `test\_hms\_db`.* TO 'hms_user'@'127.0.0.1';
FLUSH PRIVILEGES;

-- Afterwards, from the project folder run:  python manage.py migrate
-- then refresh the SCHEMAS panel in Workbench to see the tables.
