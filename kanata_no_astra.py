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
    porosidad: Optional[float] = Field(default=None, primary_key=True)
    temperatura: Optional[float] = Field(default=None, index=True)
    espesor: Optional[float] = Field(default=None, index=True)
    relajamiento: Optional[float] = Field(default=None, index=True)

    maderas: List["Madera"] = Relationship(back_populates="muestras", link_model=Enlace)

sqlite_file_name = "astra.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

def crear_madera():
        pedir_nombre=input("Ingrese el nombre de la madera:\n")
        dato=Madera(nombre=pedir_nombre)
        with Session(engine) as session:
            session.add(dato)
            session.commit()
        

def crear_muestra():
        pedir_porosidad=float(input("Ingrese la proporción de porosidad de la muestra:\n"))
        pedir_temperatura=float(input("Ingrese la temperatura inicial de la muestra:\n"))
        pedir_espesor=float(input("Ingrese el espesor de la muestra:\n"))
        pedir_relajamiento=float(input("Ingrese el tiempo de relajamientod e la muestra:\n"))
        dato=Muestra(porosidad=pedir_porosidad,temperatura=pedir_temperatura,espesor=pedir_espesor,relajamiento=pedir_relajamiento)

        with Session(engine) as session:
            session.add(dato)
            session.commit()

def menu():
    booleano=True
    while booleano:
        entrada=input("Seleccione una opcion:\n 1. Madera y muestra\n 2. Mostrar datos\n"\
                    " 3. Filtrar datos\n 4. Actualizar archivos\n 5. Eliminar datos\n 6. Salir\n Opción: ")
        if entrada == "1":
            crear_madera()
            crear_muestra()
        elif entrada == "2":
            booleano_2=True
            while booleano_2:
                entrada_2=input("¿Que tabla quiere mostrar?:\n 1. Mostrar tabla Madera\n 2. Mostrar tabla Muestra\n 3. Salir\n Opción: ")
                if entrada_2 == "1":
                    leer_datos_madera()
                elif entrada_2 == "2":
                    leer_datos_muestra()
                elif entrada_2 == "3":
                    booleano_2=False
                    break
                else:
                    print("Opcion invalida")
        elif entrada == "3":
            booleano_3=True
            while booleano_3:
                try:
                    entrada_3=float(input("Se va a filtrar la tabla Muestra por temperatura (K) menor a la que ingrese a continuación:\n"))
                    
                    filtrar_datos(entrada_3)
                    
                    booleano_3=False
                    break
                except:
                    print("Solo se permiten datos numericos")
        elif entrada == "4":
            booleano_4=True
            while booleano_4:
                try:
                    entrada_4=float(input("En la tabla Muestra se va a actualizar dato con espesor (mm) igual al que ingrese a continuacion:\n"))
                    entrada_5=float(input("Ingrese el nuevo valor de espesor (mm):\n"))
                    actualizar_datos(entrada_4, entrada_5)
                    
                    booleano_4=False
                    break
                except:
                    print("Solo se permiten datos numericos")
        elif entrada == "5":
            booleano_5=True
            while booleano_5:
                try:
                    entrada_6=float(input("En la tabla Muestra se va a borrar en valor de proporcion de porosidad igual al que ingrese a continuacion:\n"))
                    
                    borrar_datos(entrada_6)
                    
                    booleano_5=False
                    break
                except:
                    print("Solo se permiten datos numericos")

        elif entrada == "6":
            booleano=False
            break
        else:
            print("Opción invalida")

def leer_datos_muestra():
    with Session(engine) as session:
        statement = select(Muestra)
        results = session.exec(statement)
        muestras = results.all()
        print(muestras)

def leer_datos_madera():
    with Session(engine) as session:
        statement = select(Madera)
        results = session.exec(statement)
        maderas = results.all()
        print(maderas)

def filtrar_datos(x):
    with Session(engine) as session:
        statement = select(Muestra).where(Muestra.temperatura < x)
        results = session.exec(statement)
        for muestra in results:
            print(muestra)

def actualizar_datos(x,y):
    with Session(engine) as session:
        statement = select(Muestra).where(Muestra.espesor == x)
        results = session.exec(statement)
        muestras = results.one()
        print("Muestra:", muestras)

        muestras.espesor = y
        session.add(muestras)
        session.commit()
        session.refresh(muestras)
        print("Muestra actualizada:",muestras)

def borrar_datos(x):
    with Session(engine) as session:
        statement = select(Muestra).where(Muestra.porosidad == x)
        results = session.exec(statement)
        muestras = results.one()
        print("Muestra:", muestras)

        session.delete(muestras)
        session.commit()
        
        print("Muestra eliminada:", muestras)

        statement = select(Muestra).where(Muestra.porosidad == x)
        results = session.exec(statement)
        muestra = results.first()

        if muestra is None:
            print("No hay ninguna muestra con esa característica")

def crear_astra_y_tablas():
    SQLModel.metadata.create_all(engine)

def main():
    crear_astra_y_tablas()  
    menu()

if __name__ == "__main__":
    main()