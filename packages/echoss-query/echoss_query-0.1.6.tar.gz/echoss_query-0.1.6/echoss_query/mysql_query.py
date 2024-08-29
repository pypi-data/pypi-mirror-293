import pymysql
import pymysql.cursors
import pandas as pd

from echoss_fileformat import FileUtil, get_logger, set_logger_level

logger = get_logger("echoss_query")


class MysqlQuery:
    conn = None

    def __init__(self, conn_info: str or dict):
        """
        Args:
            conn_info : configration dictionary
            ex) conn_info = {
                                'mysql':
                                    {
                                        'user'  : str(user),
                                        'passwd': str(pw),
                                        'host'  : int(ip),
                                        'db'    : str(db_name),
                                        'charset': str(utf8)
                                    }
                            }
        """
        if isinstance(conn_info, str):
            conn_info = FileUtil.dict_load(conn_info)
        elif not isinstance(conn_info, dict):
            raise TypeError("MysqlQuery support type 'str' and 'dict'")
        required_keys = ['user', 'passwd', 'host', 'db', 'charset']
        if (len(conn_info) > 0) and ('mysql' in conn_info) and all(key in conn_info['mysql'] for key in required_keys):
            self.user = conn_info['mysql']['user']
            self.passwd = conn_info['mysql']['passwd']
            self.host = conn_info['mysql']['host']
            self.db = conn_info['mysql']['db']
            self.charset = conn_info['mysql']['charset']
        else:
            logger.debug(f'[MySQL] config info not exist or any required keys are missing {required_keys}')

    def __str__(self):
        return f"Mysql(host={self.conn.host}, db={self.conn.db}, charset={self.conn.charset})"

    @staticmethod
    def _parsing(query: str) -> str:
        if ';' not in query:
            return query + ';'
        return query

    def _connect_db(self):
        try:
            self.conn = pymysql.connect(
                user=self.user,
                passwd=self.passwd,
                host=self.host,
                db=self.db,
                charset=self.charset
            )
            return self.conn
        except Exception as e:
            logger.debug(f"[MySQL] DB Connection Exception : {e}")

    def ping(self):
        """
        Args:
            Any

        Returns:
            str : DB Status
        """
        if self._connect_db().open:
            logger.debug(f'[MySQL] database {self.__str__()} connection success')
        else:
            raise ConnectionError(f'database {self.__str__()} connection fail')

    def databases(self):
        """
        Args:
            Any

        Returns:
            pd.DataFrame() : database dataframe
        """
        with self._connect_db() as conn:
            with conn.cursor(pymysql.cursors.SSCursor) as cur:
                cur.execute('SHOW DATABASES;')
                result = cur.fetchall()

                if result != ():
                    return pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
                else:
                    logger.debug("[MySQL] can't find database")

    def tables(self, database: str):
        """
        Args:
            database(str) : name of database

        Returns:
            pd.DataFrame() : table dataframe
        """
        if database is not None:
            db = pymysql.connect(
                user=self.user,
                passwd=self.passwd,
                host=self.host,
                db=database,
                charset=self.charset
            )
            with db as conn:
                with conn.cursor(pymysql.cursors.SSCursor) as cur:
                    cur.execute('SHOW TABLES;')
                    result = cur.fetchall()

                    if result != ():
                        return pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
                    else:
                        logger.debug("[MySQL] can't find tables")
        else:
            logger.debug("[MySQL] can't find database")

    def conn_info(self):
        """
        Args:
            Any

        Returns:
            tuple : connection information(host_info, db_info, charset_info)
        """
        return self.conn.host, self.conn.db, self.conn.charset

    ###################################3###
    #  Table method
    #######################################

    def create(self, query_str: str) -> None:
        """
        Args:
            query_str(str) : MySQL create query string
        """
        query = self._parsing(query_str)
        keyword = 'CREATE'
        if keyword in query or keyword.lower() in query:
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.DictCursor) as cur:
                        cur.execute(query)
                    conn.commit()
            except Exception as e:
                logger.debug(f"[MySQL] Create Exception : {e}")
        else:
            raise ValueError('input is not include "create"')

    def drop(self, query_str: str) -> None:
        """
        Args:
            query_str(str) : MySQL drop query string
        """
        query = self._parsing(query_str)
        keyword = 'DROP'
        if keyword in query or keyword.lower() in query:
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.DictCursor) as cur:
                        cur.execute(query)
                    conn.commit()
            except Exception as e:
                logger.debug(f"[MySQL] Drop Exception : {e}")
        else:
            raise ValueError('input is not include "drop"')

    def truncate(self, query_str: str) -> None:
        """
        Args:
            query_str(str) : MySQL truncate query string
        """
        query = self._parsing(query_str)
        keyword = 'TRUNCATE'
        if keyword in query or keyword.lower() in query:
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.DictCursor) as cur:
                        cur.execute(query)
                    conn.commit()
            except Exception as e:
                logger.debug(f"[MySQL] Truncate Exception : {e}")
        else:
            raise ValueError('input is not include "truncate"')

    def alter(self, query_str: str) -> None:
        """
        Args:
            query_str(str) : MySQL alter query string
        """
        query = self._parsing(query_str)
        keyword = 'ALTER'
        if keyword in query or keyword.lower() in query:
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.DictCursor) as cur:
                        cur.execute(query)
                    conn.commit()
            except Exception as e:
                logger.debug(f"[MySQL] Alter Exception : {e}")
        else:
            raise ValueError('input is not include "alter"')

    ###################################3###
    #  Quqery method
    #######################################

    def select_one(self, query_str: str, params=None) -> dict:
        """
        Args:
            query_str(str): MySQL select query string that returns a single row
            params: query string format parameters like % style
        Returns:
            dict: A single dictionary result from the query
        """
        query = self._parsing(query_str)
        keyword = 'SELECT'

        if keyword in query or keyword.lower() in query:
            result = {}
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.DictCursor) as cur:
                        cur.execute(query, params)
                        result = cur.fetchone()
                        if result:
                            return result
                        else:
                            logger.debug("[MySQL] No data found")
                            return {}
            except Exception as e:
                logger.debug(f"[MySQL] SELECT Exception: {e}")
                return {}
        else:
            raise ValueError('Input does not include "SELECT"')

    def select_list(self, query_str: str, params=None) -> list:
        """
        Args:
            query_str(str) : MySQL select query string
            params: query string format parameters like % style
        Returns:
            list() : List of query result
        """
        query = self._parsing(query_str)
        keyword = 'SELECT'

        if keyword in query or keyword.lower() in query:
            try:
                with self._connect_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute(query, params)
                        result = cur.fetchall()

                        if result != ():
                            return [x for tuple_ in result for x in tuple_]
                        else:
                            logger.debug("[MySQL] data not exist")
            except Exception as e:
                logger.debug(f"[MySQL] SELECT_LIST Exception : {e}")
        else:
            raise ValueError('input is not include "select"')

    def select(self, query_str: str, params=None) -> pd.DataFrame:
        """
        Args:
            query_str(str) : MySQL select query string
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str)
        keyword = 'SELECT'

        if keyword in query or keyword.lower() in query:
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.DictCursor) as cur:
                        cur.execute(query, params)
                        result = cur.fetchall()

                        if result != ():
                            return pd.DataFrame(result)
                        else:
                            logger.debug(f"[MySQL] data not exist")
            except Exception as e:
                logger.debug(f"[MySQL] SELECT Exception : {e}")
        else:
            raise ValueError('input is not include "select"')

    def faster_select(self, query_str: str, params=None, fetch_size=1000) -> pd.DataFrame:
        """
        Args:
            query_str(str) : MySQL select query string better than normal select
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str)
        keyword = 'SELECT'
        if keyword in query or keyword.lower() in query:
            results = []
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.SSCursor) as cur:
                        cur.execute(query, params)
                        while True:
                            rows = cur.fetchmany(fetch_size)
                            if not rows:
                                break
                            results.extend(rows)

                        if len(results) > 0:
                            return pd.DataFrame(results, columns=[desc[0] for desc in cur.description])
                        else:
                            logger.debug(f"[MySQL] data not exist")
            except Exception as e:
                logger.debug(f"[MySQL] FASTER_SELECT Exception : {e}")
            self.close()
        else:
            raise ValueError('input is not include "select"')

    def insert(self, query_str: str, params=None) -> int:
        """
        Args:
            query_str(str) : MySQL insert query string
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str)
        keyword = 'INSERT'
        if keyword in query or keyword.lower() in query:
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.DictCursor) as cur:
                        cur.execute(query, params)
                    conn.commit()
                    return cur.rowcount
            except Exception as e:
                logger.debug(f"[MySQL] INSERT Exception : {e}")
                return 0
        else:
            raise ValueError('input is not include "insert"')

    def update(self, query_str: str, params=None) -> int:
        """
        Args:
            query_str(str) : MySQL update query string
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str)
        keyword = 'UPDATE'
        if keyword in query or keyword.lower() in query:
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.DictCursor) as cur:
                        cur.execute(query, params)
                        logger.debug(f"[MySQL] UPDATE {cur.rowcount} rows")
                    conn.commit()
                    return cur.rowcount
            except Exception as e:
                logger.debug(f"[MySQL] UPDATE Exception : {e}")
                return 0
        else:
            raise ValueError('input is not include "update"')

    def delete(self, query_str: str, params=None) -> int:
        """
        Args:
            query_str(str) : MySQL delete query string

        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str)
        keyword = 'DELETE'
        if keyword in query or keyword.lower() in query:
            try:
                with self._connect_db() as conn:
                    with conn.cursor(pymysql.cursors.DictCursor) as cur:
                        cur.execute(query, params)
                        logger.debug(f"[MySQL] DELETE {cur.rowcount} rows")
                    conn.commit()
                    return cur.rowcount
            except Exception as e:
                logger.debug(f"[MySQL] DELETE Exception : {e}")
                return 0
        else:
            raise ValueError('input is not include "delete"')

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

