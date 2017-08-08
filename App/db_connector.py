from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy.dialects.postgresql import *

engine = create_engine('postgresql:///hosts')

Base = declarative_base(engine)


class Host(Base):
    __tablename__ = 'host'

    id = Column(Integer, primary_key=True)
    hostname = Column(VARCHAR(128))
    host_alias = Column(VARCHAR(128))
    hostgroup = Column(VARCHAR(128))
    ipv4 = Column(INET)
    ipv6 = Column(VARCHAR(128))
    os = Column(VARCHAR(128))
    os_type = Column(VARCHAR(128))
    os_release = Column(VARCHAR(128))
    ssh_port = Column(VARCHAR(128))
    ssh_user = Column(VARCHAR(128))
    active = Column(BOOLEAN)

    

    @property
    def serialize(self):
    # return object data in easily serializeable format
        return {
            'id':self.id,
            'hostname':self.hostname,
            'hostgroup':self.hostgroup,
            'ipv4':self.ipv4,
            'ssh_port':self.ssh_port,
            'ssh_user':self.ssh_user,
            'active':self.active,}

def loadSession():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == '__main__':
    session = loadSession()
    res = session.query(Host).all()
    print res[1].hostname

