# Pure-Python MySQL driver so MySQL works without compiling anything (Windows friendly).
try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:  # only needed when the MySQL backend is used
    pass
