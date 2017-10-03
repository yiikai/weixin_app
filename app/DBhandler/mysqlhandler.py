from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String,Integer,Text

base = declarative_base()

class Menu(base):
	__tablename__ = 'Caipu'
	id = Column(Integer,primary_key=True)
	title = Column(String(100))
	ingredient = Column(Text)
	steps = Column(Text)	

class mysqlhandler(object):
	DBSession = None
	session = None
	def __init__(self,dbname,ip,username):
		sqlconnect = "mysql+mysqldb://%s:myk1987091029!@%s:3306/%s?charset=utf8"%(username,ip,dbname)
		print "sqlconnect statement is ======",sqlconnect
		self.engine = create_engine(sqlconnect)
		self.DBSession = sessionmaker(bind=self.engine)
		self.session = self.DBSession()
	
	def add_item(self,item):
		self.session.add(item)
		self.session.commit()
	
	def disconnect(self):
		self.session.close()
				
	def execute(self,sql):
		return self.session.execute(sql)		
