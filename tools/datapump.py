import psycopg2


class Receiver():
    """Recive data from old statistics format"""
    def __init__(self, db_host, db_port=5432, db_user='puser', db_pwd='1234'):
        conn_str = 'host=%s port=%d user=%s password=%s dbname=statistics' % (
            db_host, db_port, db_user, db_pwd)
        self.conn = psycopg2.connect(conn_str)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def load_equipment(self):
        self.cur.execute('SELECT * FROM equipment;')
        result = self.cur.fetchall()
        self.plant_dict = self.build_node_dict(result)
        self.conn.commit()

    def build_node_dict(self, query_result):
        node_dict = {}
        for rec in query_result:
            if rec[1] in node_dict:
                node_dict[rec[1]].append(rec)
            else:
                node_dict[rec[1]] = [rec]
        return node_dict

    def get_equipment(self):
        self.load_equipment()
        return self.plant_dict

    def view_nodes(self):
        for node in self.plant_dict:
            print('%s > %s' % (node, self.plant_dict[node]))


class Journal:
    def __init__(self, old_eq_num, eq_num, ext_stat, stat_by_parent):
        self.old_eq_num = old_eq_num
        self.equipment_id = eq_num
        self.extended_stat = ext_stat
        self.stat_by_parent = stat_by_parent

    def set_id(self, oid):
        self.id = oid


class Archiver():
    """Store data in new statistics format"""
    def __init__(self, db_host, db_port=5432, db_user='puser', db_pwd='1234'):
        conn_str = 'host=%s port=%d user=%s password=%s dbname=iplant' % (
            db_host, db_port, db_user, db_pwd)
        self.conn = psycopg2.connect(conn_str)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def store_equipment(self, old_id, name, plant_id):
        self.cur.execute(
            """INSERT INTO catalog_unit (name, plant_id)
            VALUES (%s, %s);""",
            (name, plant_id))
        self.conn.commit()
        self.cur.execute(
            'SELECT id from catalog_unit ORDER BY id DESC LIMIT 1;')
        new_id = self.cur.fetchone()[0]
        self.conn.commit()
        return old_id, new_id

    def store_equipment_set(self, node_dict):
        def job_node(old_node=None, new_node=None):
            if old_node in node_dict:
                for branch in node_dict[old_node]:
                    nums = self.store_equipment(branch[0], branch[2], new_node)
                    if branch[6]:
                        self.journal_list.append(
                            Journal(nums[0], nums[1], branch[7], branch[8]))
                    job_node(*nums)

        self.cur.execute('DELETE FROM catalog_unit;')
        self.conn.commit()
        self.journal_list = []
        job_node()

    def create_journals(self):
        for journal in self.journal_list:
            self.cur.execute(
                """INSERT INTO statistics_journal
                (extended_stat, stat_by_parent, equipment_id,
                    description, last_stat)
                VALUES (%s, %s, %s, %s, %s)""",
                (journal.extended_stat,
                    journal.stat_by_parent,
                    journal.equipment_id,
                    '',
                    'wd=00:00,psk=0,ost=0'))
            self.conn.commit()
            self.cur.execute(
                'SELECT id from statistics_journal ORDER BY id DESC LIMIT 1;')
            journal.set_id(self.cur.fetchone()[0])
            self.conn.commit()

if __name__ == '__main__':
    receiver = Receiver('192.168.20.104')
    receiver.get_equipment()
    # receiver.view_nodes()
    archiver = Archiver('127.0.0.1')
    archiver.store_equipment_set(receiver.get_equipment())
    archiver.create_journals()
    receiver.close()
    archiver.close()
