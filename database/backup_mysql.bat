@echo off
REM Backs up hms_db to a dated .sql file. Needs mysqldump (installed with MySQL / Workbench).
REM If mysqldump is not found, add "C:\Program Files\MySQL\MySQL Server 8.0\bin" to PATH.
set STAMP=%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%
set STAMP=%STAMP: =0%
if not exist backups mkdir backups
mysqldump -u hms_user -p --no-tablespaces --single-transaction hms_db > backups\hms_db_%STAMP%.sql
echo Backup saved in the backups folder.
