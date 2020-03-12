# Demonstrates table constraints. There are 6 possible constraints:
# NOT NULL
# UNIQUE
# PRIMARY KEY
# FOREIGN KEY
# CHECK
# DEFAULT
import json
import mariadb as mdb
import pandas as pd
import pleiades as ple

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

cz = ple.CZ(cursor)

# FOREIGN KEY is a CONSTRAINT that enforces referential integrety between
# tables. The table with the FOREIGN KEY is the child and the reference is the
# parent. The FOREIGN KEY of the child typically references the PRIMARY KEY of
# the parent. Aside from referencing, two options, ON DELETE and ON UPDATE can
# be set to determine what happens to the FOREIGN KEY when the parent is
# deleted or updated. The options are CASCADE, SET NULL and RESTRICT.
# CASCADE sets the child equal to whatever the parent is set to. If the parent
# is deleted, the child is also deleted. This is true even in ON UPDATE
# cascade.
# SET NULL sets the child to NULL.
# RESTRICT makes it impossible for the parent to be deleted or updated as long
# as the child exists. RESTRICT is the default value for ON DELETE and ON
# UPDATE.
# FOREIGN KEY can be set at table creation or after using ALTER TABLE.
command = '''
ALTER TABLE quest_map
ADD CONSTRAINT fk_qm_qid
    FOREIGN KEY(quest_id)
        REFERENCES quest(id)
        ON DELETE cascade
        ON UPDATE cascade
,ADD CONSTRAINT fk_qm_cid
    FOREIGN KEY(char_id)
        REFERENCES konosuba(id)
        ON DELETE cascade
        ON UPDATE cascade
;
'''
cursor.execute(command)
df = pd.DataFrame(cz.show_columns('quest_map'))
print(df)
print()

command = '''
DELETE FROM quest WHERE id=1;
'''
cursor.execute(command)
df = pd.DataFrame(cz.select_from('quest_map').ex())
print(df)
print()

command = '''
INSERT INTO quest VALUES (1, 'giant toads', 50000);
'''
cursor.execute(command)
df = pd.DataFrame(cz.select_from('quest_map').ex())
print(df)
print()

command = '''
ALTER TABLE quest_map
DROP CONSTRAINT fk_qm_qid
,DROP CONSTRAINT fk_qm_cid
;
'''
cursor.execute(command)
df = pd.DataFrame(cz.show_columns('quest_map'))
print(df)
print()

cursor.close()
db.commit()
db.close()
print('commands executed.')
