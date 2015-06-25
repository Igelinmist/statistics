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
                    self.node_list.append(nums)
                    job_node(*nums)

        self.cur.execute('DELETE FROM catalog_unit;')
        self.conn.commit()
        self.node_list = []
        job_node()


if __name__ == '__main__':
    receiver = Receiver('192.168.20.104')
    archiver = Archiver('127.0.0.1')
    archiver.store_equipment_set(receiver.get_equipment())
    receiver.close()
    archiver.close()
