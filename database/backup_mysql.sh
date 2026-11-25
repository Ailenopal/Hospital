#!/bin/sh
# Backs up hms_db to backups/hms_db_<date>.sql  (run from the project folder)
mkdir -p backups
mysqldump -u hms_user -p --no-tablespaces --single-transaction hms_db > "backups/hms_db_$(date +%Y%m%d_%H%M).sql"
echo "Backup saved in the backups folder."
