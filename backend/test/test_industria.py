from sqlalchemy import null

from backend.models import IndustriaId


class TestIndustria:

    """
    1. que se cree con los datos correctos (listo)
    2. que se muestre la excepcion si se encuentra borrado y se quiere borrar
    3. que se muestre la excepcion si se busca un registro borrado
    4. que muestre vacio si no existe en la db
    5. que muestre las borrados
    6. que lance lista vacia si no hay borrados
    7. crear registros y que mostrar_todos si los muestre
    8. que al restaurar un registro su estado "activo" sea true
    9. que al tratar de introducir una industria con el mismo nombre, salga una excecpcion diceindo que ya existe este registro
    """

    # 1
    def test_crear_industria(self, client):

        datos = {"nombre_industria":"Alimenticia y de bebidas"}

        r = client.post('/industrias', json=datos)
        res = r.json()

        assert r.status_code == 200
        assert res["nombre_industria"] == "Alimenticia y de bebidas"
        assert res["id_industria"] == 1
        assert res["activo"] == True

    # 2

    def test_borrar_borrado(self, client, session):
        industria = IndustriaId(nombre_industria="Alimenticia y de bebida",activo=False)
        session.add(industria)
        session.commit()
        r = client.post('/industria-borrar', params={"id":1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 3
    def test_buscar_borrado(self, client, session):
        industria = IndustriaId(nombre_industria="Alimenticia y de bebida", activo=False)
        session.add(industria)
        session.commit()
        r = client.get('/industria', params={"id":1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 4
    def test_buscar_vacio(self, client, session):
        r = client.get('/industria', params={"id": 1})
        res = r.json()
        assert r.status_code == 200
        assert res == None

    # 5
    def test_mostrar_borrados(self, client, session):
        industria1 = IndustriaId(nombre_industria="Alimenticia y de bebida", activo=False)
        industria2 = IndustriaId(nombre_industria="Automotriz y de movilidad", activo=False)
        session.add(industria1)
        session.add(industria2)
        session.commit()
        r = client.get('/industrias-borradas')
        res = r.json()
        assert r.status_code == 200
        assert res[0]["nombre_industria"] == "Alimenticia y de bebida"
        assert res[0]["activo"] == False
        assert res[1]["nombre_industria"] == "Automotriz y de movilidad"
        assert res[0]["activo"] == False


    # 6
    def test_ningun_borrado(self, client, session):
        industria1 = IndustriaId(nombre_industria="Alimenticia y de bebida")
        industria2 = IndustriaId(nombre_industria="Automotriz y de movilidad")
        session.add(industria1)
        session.add(industria2)
        session.commit()
        r = client.get('/industrias-borradas')
        res = r.json()
        assert r.status_code == 200
        assert res == []

    # 7
    def test_mostrar_registros(self, client, session):
        industria1 = IndustriaId(nombre_industria="Alimenticia y de bebida")
        industria2 = IndustriaId(nombre_industria="Automotriz y de movilidad")
        session.add(industria1)
        session.add(industria2)
        session.commit()
        r = client.get('/industrias')
        res = r.json()
        assert r.status_code == 200
        assert res[0]["nombre_industria"] == "Alimenticia y de bebida"
        assert res[0]["id_industria"] == 1
        assert res[1]["nombre_industria"] == "Automotriz y de movilidad"
        assert res[1]["id_industria"] == 2

    # 8
    def test_restaurar_registro(self, client, session):
        industria1 = IndustriaId(nombre_industria="Alimenticia y de bebida", activo=False)
        session.add(industria1)
        session.commit()
        r = client.post('/industria-restaurar', params={"id":1})
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_industria"] == "Alimenticia y de bebida"
        assert res["id_industria"] == 1
        assert res["activo"] == True
        r = client.get('/industrias')
        res = r.json()
        assert r.status_code == 200
        assert res[0]["nombre_industria"] == "Alimenticia y de bebida"
        assert res[0]["id_industria"] == 1
        assert res[0]["activo"] == True

    # 9
    def test_dato_repetido(self, client, session):
        industria = IndustriaId(nombre_industria="Alimenticia y de bebida", activo=True)
        session.add(industria)
        session.commit()
        industria1 = {"nombre_industria":"Alimenticia y de bebida"}

        r = client.post('/industrias', json=industria1)
        res = r.json()
        assert r.status_code == 409
        assert res["detail"] == "los valores ['Alimenticia y de bebida'] ya se encuentran registrados"
