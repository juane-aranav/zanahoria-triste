from typing import List, Optional
from unittest import result
from sqlmodel import Field, Session, Relationship, SQLModel, create_engine, select, col
from math import *

sigma=5.67*(10**(-8))

epsilon=1

#rhoc=(8*relajamiento*(temperatura**3)*sigma*1)/(espesor)

class Enlace(SQLModel, table=True):
    madera_id: Optional[int] = Field(
        default=None, foreign_key="madera.id", primary_key=True)
    muestra_porosidad:Optional[int] = Field(
        default=None, foreign_key="muestra.porosidad", primary_key=True)

class Madera(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    rhoc: Optional[int] = Field(default=None, index=True)

    muestras: List["Muestra"] = Relationship(back_populates="maderas", link_model=Enlace)

class Muestra(SQLModel, table=True):
    porosidad: Optional[int] = Field(default=None, primary_key=True)
    temperatura: Optional[int] = Field(default=None, index=True)
    espesor: Optional[int] = Field(default=None, index=True)
    relajamiento: Optional[float] = Field(default=None, index=True)

    maderas: List["Madera"] = Relationship(back_populates="muestras", link_model=Enlace)

sqlite_file_name = "astra.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

def crear_archivos():
    madera_sande = Madera(nombre="Sandé")
    madera_sajo = Madera(nombre="Sajo")
    madera_cedro = Madera(nombre="Cedro")
    madera_nogal = Madera(nombre="Nogal")

    muestra_1 = Muestra(temperatura=300, espesor=500, relajamiento=19.697, maderas=[madera_cedro,madera_nogal])
    muestra_2 = Muestra(porosidad=30, temperatura=290, relajamiento=16.684, espesor=400)
    muestra_3 = Muestra(porosidad=20, temperatura=280, relajamiento=21.879, espesor=300)
    muestra_4 = Muestra(porosidad=10, temperatura=270, relajamiento=19.689, espesor=200)

    with Session(engine) as session:
        session.add(muestra_1)
        session.add(muestra_2)
        session.add(muestra_3)
        session.add(muestra_4)

        session.add(madera_sande)
        session.add(madera_sajo)
        session.add(madera_cedro)
        session.add(madera_nogal)

        session.commit()
        
def leer_datos():
    with Session(engine) as session:
        statement = select(Muestra)
        results = session.exec(statement)
        muestras = results.all()
        print(muestras)

def filtrar_datos():
    with Session(engine) as session:
        statement = select(Muestra).where(Muestra.temperatura < 280)
        results = session.exec(statement)
        for muestra in results:
            print(muestra)

def actualizar_datos():
    with Session(engine) as session:
        statement = select(Muestra).where(Muestra.temperatura == 290)
        results = session.exec(statement)
        muestras = results.one()
        print("Muestra:", muestras)

        muestras.temperatura = 300
        session.add(muestras)
        session.commit()
        session.refresh(muestras)
        print("Muestra actualizada:",muestras)

def borrar_datos():
    with Session(engine) as session:
        statement = select(Muestra).where(Muestra.porosidad == 20)
        results = session.exec(statement)
        muestras = results.one()
        print("Muestra:", muestras)

        session.delete(muestras)
        session.commit()
        
        print("Muestra eliminada:", muestras)

        statement = select(Muestra).where(Muestra.porosidad == 20)
        results = session.exec(statement)
        muestra = results.first()

        if muestra is None:
            print("No hay ninguna muestra con esa característica")

def crear_astra_y_tablas():
    SQLModel.metadata.create_all(engine)

def main():
    crear_astra_y_tablas()
    crear_archivos()
    leer_datos()
    filtrar_datos()
    actualizar_datos()
    borrar_datos()

if __name__ == "__main__":
    main()