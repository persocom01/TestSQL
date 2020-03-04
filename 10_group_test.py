# Demonstrates the group keyword.
import json
import mariadb as mdb
import pandas as pd

dbname = 'testDB'
cfg_path = './server.cfg'

with open(cfg_path, 'r') as f:
    server_config = json.load(f)
db = mdb.connect(**server_config)
cursor = db.cursor()

command = f'USE {dbname};'
try:
    cursor.execute(command)
except mdb.ProgrammingError:
    print('database does not exist')

# One reason to use GROUP BY is to apply an aggregate function to the group.
# Note also that although you may select non aggregate columns, SELECT * will
# only return the first row in the group.
# The aggregate functions available are:
# COUNT = len()
# SUM
# AVG
# MIN
# MAX
command = '''
SELECT *,count(*),SUM(age),AVG(age),MIN(age),MAX(age)
FROM konosuba
WHERE isekai = false
GROUP BY race
ORDER BY count(*) DESC
LIMIT 10;
'''
cursor.execute(command)
df = pd.DataFrame(cursor.fetchall())
print('group by:')
print(df)
print()

# The second reason to use GROUP BY is to use the HAVING keyword, which is
# basically WHERE but applied to aggregate group functions.
command = '''
SELECT count(*),SUM(age),AVG(age),MIN(age),MAX(age)
FROM konosuba
WHERE isekai = false
GROUP BY race
HAVING count(*) > 1
ORDER BY count(*) DESC
LIMIT 10;
'''
cursor.execute(command)
df = pd.DataFrame(cursor.fetchall())
print('having count > 1:')
print(df)
print()

cursor.close()
db.commit()
db.close()
print('commands executed.')
