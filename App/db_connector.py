from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine

engine = create_engine('postgresql:///hosts')

Base = declarative_base(engine)


class Host(Base):
    __tablename__ = 'host'

    id = Column(Integer, primary_key=True)
    hostname = Column(String)
    host_alias = Column(String)
    hostgroup = Column(String)
    ipv4 = Column(Integer)
    ipv6 = Column(Integer)
    os = Column(String)
    os_type = Column(String)
    os_release = Column(String)
    ssh_port = Column(Integer)
    ssh_user = Column(String)
    active = Column(String)


    def __init__(self, id, hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type,os_release,ssh_port, ssh_user, active):
       self.host_id ={'id':id,
                      'hostname':hostname,
                      'host_alias':host_alias,
                      'hostgroup':hostgroup,
                      'ipv4':ipv4,
                      'ipv6':ipv6,
                      'os':os,
                      'os_type':os_type,
                      'os_release':os_release,
                      'ssh_port':ssh_port,
                      'ssh_user':ssh_user,
                      'active':active,
                      }

    def __getitem__(self, item):
        return self.host_id[item]


def loadSession():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

@property
def serialize(self):
    # return object data in easily serializeable format
    return{
        'id':self.id,
        'hostname':self.hostname,
        'hostgroup':self.hostgroup,
        'ipv4':self.ipv4,
        'ssh_port':self.ssh_port,
        'ssh_user':self.ssh_user,
        'active':self.active
    }


if __name__ == '__main__':
    session = loadSession()
    res = session.query(Host).all()
    print res[1].hostname

