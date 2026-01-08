#!/bin/bash
set -e

# Crée l'utilisateur et donne les permissions avec les variables d'environnement pour la prod
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';
FLUSH PRIVILEGES;
EOSQL