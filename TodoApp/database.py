

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



#for connecting with sql
SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db'   
engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})



# for connection with postgresql DBMS
# SQLALCHEMY_DATABASE_URL='postgresql://postgres:Ab9819114*@localhost/TodoApplicationDatabase'    
# engine=create_engine(SQLALCHEMY_DATABASE_URL)


# for connection with MySql DBMS
# SQLALCHEMY_DATABASE_URL='mysql+pymysql://root:Ab9819114*@127.0.0.1:3306/TodoApplicationDatabase'    
# engine=create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal=sessionmaker(autoflush=False,bind=engine)

Base=declarative_base()