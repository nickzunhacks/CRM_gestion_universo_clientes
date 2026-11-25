from backend.models.Paises import Paises, PaisesId

class TestPaises:

    """
        1. que se cree con los datos correctos (post /paises)
        2. que se muestre la excepcion si se encuentra borrado y se quiere borrar (post /paises-borrar)
        3. que se muestre la excepcion si se busca un registro borrado (get /pais)
        4. que muestre vacio si no existe en la db (get /pais)
        5. que muestre las borrados (get /paises-borrados)
        6. que lance lista vacia si no hay borrados (get /paises-borrados)
        7. crear registros y que mostrar_todos si los muestre (get /paises)
        8. que al restaurar un registro su estado "activo" sea true (post /pais-restaurar get /pais)
        9) que al intentar meter un registro con el mismo nombre de pais, no se pueda y salga una excepcion
    """

    # 1
    def test_crear_paises(self, client, session):
        colombia = {"nombre_pais":"Colombia", "nombre_subdivisiones":"Departamento"}
        r = client.post("/paises", json=colombia)
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_pais"] == "Colombia"
        assert res["nombre_subdivisiones"] == "Departamento"
        pais_creado = session.get(PaisesId, 1)
        assert pais_creado.nombre_pais == "Colombia"
        assert pais_creado.nombre_subdivisiones == "Departamento"

    # 2
    def test_borrar_pais(self, client, session):
        ecuador = PaisesId(nombre_pais="Ecuador", nombre_subdivisiones="provincia", activo=False)
        session.add(ecuador)
        session.commit()
        r = client.post("/paises-borrar", params={"id":1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 3
    def test_buscar_borrado(self, client, session):
        panama = PaisesId(nombre_pais="Panama", nombre_subdivisiones="estado", activo=False)
        session.add(panama)
        session.commit()
        r = client.get("/pais", params={"id":1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 4
    def test_vacio(self, client, session):
        r = client.get("/pais", params={"id":1})
        res = r.json()
        assert r.status_code == 200
        assert not res

    # 5
    def test_paises_borrados(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="departamento", activo=False)
        ecuador = PaisesId(nombre_pais="Ecuador", nombre_subdivisiones="provincia", activo=False)
        panama = PaisesId(nombre_pais="Panama", nombre_subdivisiones="estado", activo=False)
        peru = PaisesId(nombre_pais="Peru", nombre_subdivisiones="departamento", activo=False)

        session.add(colombia)
        session.add(ecuador)
        session.add(panama)
        session.add(peru)
        session.commit()

        r = client.get("/paises-borrados")
        res = r.json()
        assert len(res) == 4
        assert res[0]["nombre_pais"] == "Colombia"
        assert res[1]["nombre_pais"] == "Ecuador"
        assert res[2]["nombre_pais"] == "Panama"
        assert res[3]["nombre_pais"] == "Peru"

    # 6
    def test_no_borrados(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="departamento")
        ecuador = PaisesId(nombre_pais="Ecuador", nombre_subdivisiones="provincia")
        panama = PaisesId(nombre_pais="Panama", nombre_subdivisiones="estado")
        peru = PaisesId(nombre_pais="Peru", nombre_subdivisiones="departamento")
        session.add(colombia)
        session.add(ecuador)
        session.add(panama)
        session.add(peru)

        r = client.get("/paises-borrados")
        res = r.json()
        assert r.status_code == 200
        assert res == []

    # 7
    def test_mostrar_todos_paises(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="departamento")
        ecuador = PaisesId(nombre_pais="Ecuador", nombre_subdivisiones="provincia")
        panama = PaisesId(nombre_pais="Panama", nombre_subdivisiones="estado")
        peru = PaisesId(nombre_pais="Peru", nombre_subdivisiones="departamento")
        session.add(colombia)
        session.add(ecuador)
        session.add(panama)
        session.add(peru)

        r = client.get("/paises")
        res = r.json()
        assert r.status_code == 200
        assert len(res) == 4
        assert res[0]["nombre_pais"] == "Colombia"
        assert res[1]["nombre_pais"] == "Ecuador"
        assert res[2]["nombre_pais"] == "Panama"
        assert res[3]["nombre_pais"] == "Peru"

    # 8
    def test_restaurar_pais(self, client, session):
        noruega = PaisesId(nombre_pais="Noruega",  nombre_subdivisiones="Fylker",activo=False)
        session.add(noruega)
        session.commit()

        r = client.post("/pais-recuperar", params={"id":1})
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_pais"] == "Noruega"

        r = client.get("/pais", params={"id":1})
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_pais"] == "Noruega"

    # 9
    def test_pais_repetido(self, client, session):
        portugal = PaisesId(nombre_pais="Portugal", nombre_subdivisiones="Distrito")
        portugal_repetido = {"nombre_pais":"Portugal", "nombre_subdivisiones":"Distrito"}
        session.add(portugal)
        session.commit()
        r = client.post("/paises", json=portugal_repetido)
        res = r.json()
        assert r.status_code == 409
        assert res["detail"] == "los valores ['Portugal'] ya se encuentran registrados"