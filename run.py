from includes import mysql
import logging, datetime

class DatabaseClearer():

    def __init__(self, delete_before, table, host, database, user, password):
        # create logger
        self.logger = logging.getLogger('DATABASECLEARER')
        self.logger.setLevel(logging.DEBUG)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.log = logging.FileHandler('databaseclearer.log')
        self.log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.ch.setFormatter(formatter)
        self.log.setFormatter(formatter)
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.log) 

        self.con = mysql.Database(host, database, user, password, self.logger)
        curs = self.con.connect()

        if self.con != False and curs != False:
            self.con.delete(table, "DATEDIFF(NOW(), insertdatetime) > "+str(delete_before))
            self.logger.info("Successfuly deleted.")

        self.con.close()

# add jobs here, you can add as much as you want
to_delete = [
    {"host":"mysql.domain.de", "database":"dbname", "user":"username", "password":"your_password", "table": "tablename", "days_before_deletion":40}, 
    {"host":"domain.de", "database":"dbname", "user":"username", "password":"your_password", "table": "tablename", "days_before_deletion":40} 
 

]

for job in to_delete:
    run = DatabaseClearer(job['days_before_deletion'], job['table'], job['host'], job['database'], job['user'], job['password'])
