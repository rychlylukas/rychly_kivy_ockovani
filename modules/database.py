from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.types import String, Integer, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()


class Vakcina(Base):
    __tablename__ = 'vakciny'

    id = Column(Integer, primary_key=True)
    nazev_firmy = Column(String(length=50))
    ucinnost_vakciny = Column(Integer)
    cena_vakciny = Column(Integer)
    typ_vakciny = Column(String(length=50))
    pocet_davek = Column(Integer)
    schvalena_v_EU = Column(Boolean)
    ockovani = relationship('Ockovani', backref='vakciny')


class Povolani(Base):
    __tablename__ = 'povolani'

    id = Column(Integer, primary_key=True)
    nazev_povolani = Column(String(length=50))
    ockovani = relationship('Ockovani', backref='povolani')


class Ockovani(Base):
    __tablename__ = 'ockovani'

    id = Column(Integer, primary_key=True)
    jmeno = Column(String(length=50))
    datum_narozeni = Column(Date)
    pocet_davek_aktualne = Column(Integer)
    vakciny_id = Column(Integer, ForeignKey('vakciny.id'))
    povolani_id = Column(Integer, ForeignKey('povolani.id'))

class Database:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='../ockovani.db'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def read_all(self, order = Ockovani.id):
        try:
            result = self.session.query(Ockovani).order_by(order).all()
            return result
        except:
            return False

    def create_vakcina(self, vakcina):
        try:
            self.session.add(vakcina)
            self.session.commit()
            return True
        except:
            return False

    def create_povolani(self, povolani):
        try:
            self.session.add(povolani)
            self.session.commit()
            return True
        except:
            return False

    def create_ockovani(self, ockovani):
        try:
            self.session.add(ockovani)
            self.session.commit()
            return True
        except:
            return False

    def read_vakciny(self, order = Vakcina.nazev_firmy):
        try:
            result = self.session.query(Vakcina).order_by(order).all()
            return result
        except:
            return False

    def read_vakciny_id(self, id):
        try:
            result = self.session.query(Vakcina).get(id)
            return result
        except:
            return False

    def read_povolani(self, order = Povolani.nazev_povolani):
        try:
            result = self.session.query(Povolani).order_by(order).all()
            return result
        except:
            return False

    def read_povolani_id(self, id):
        try:
            result = self.session.query(Povolani).get(id)
            return result
        except:
            return False

    def read_ockovani(self, order = Ockovani.datum_narozeni):
        try:
            result = self.session.query(Ockovani).order_by(order).all()
            return result
        except:
            return False

    def read_ockovani_id(self, id):
        try:
            result = self.session.query(Ockovani).get(id)
            return result
        except:
            return False

    def update(self):
        try:
            self.session.commit()
            return True
        except:
            return False

    def delete_vakciny(self, id):
        try:
            vakcina = self.read_vakciny_id(id)
            self.session.delete(vakcina)
            self.session.commit()
            return True
        except:
            return False

    def delete_povolani(self, id):
        try:
            povolani = self.read_povolani_id(id)
            self.session.delete(povolani)
            self.session.commit()
            return True
        except:
            return False

    def delete_ockovani(self, id):
        try:
            ockovani = self.read_ockovani_id(id)
            self.session.delete(ockovani)
            self.session.commit()
            return True
        except:
            return False

    def read_by_id(self, id):
        try:
            result = self.session.query(Ockovani).get(id)
            return result
        except:
            return False

    def create(self, person):
        try:
            self.session.add(person)
            self.session.commit()
            return True
        except:
            return False

    def delete(self, id):
        try:
            person = self.read_by_id(id)
            self.session.delete(person)
            self.session.commit()
            return True
        except:
            return False


