import psycopg2
import subprocess
import sys
import os
import re
import datetime
import psycopg2 as pg
from psycopg2 import sql

def main():
  with pg.connect(
  host="10.24.11.107",
  port="12345", 
  dbname="postgres",
#  user="docker",
  user="postgres",
  password="password"
  ) as conn:
        with conn.cursor() as cursor:
          proc = subprocess.Popen(["python", "alps_sensor_test3.py"], 
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT
          )
          data = []
          start = False
          for line in iter(proc.stdout.readline, ''):
            pattern = "(.*):(.*)"
            d = re.search(pattern, line)
            if not (isinstance(d, type(None))):
              start = True
              t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
              data.append(t)
            
              if start == True:
                data.append(d.group(1))
                data.append(float(d.group(2)))
                print(data)
                cursor.execute(
                sql.SQL("INSERT INTO alps({},{},{})VALUES(%s,%s,%s)").format(sql.Identifier("time"),sql.Identifier("sensor"),sql.Identifier("value")),[data[0],data[1],data[2]])
                conn.commit()
                data = []
                start = False

if __name__ == '__main__':
  main()
