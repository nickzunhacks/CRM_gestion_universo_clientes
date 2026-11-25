from backend.models.Ciudades import CiudadesId
from backend.models.Subdivisiones import SubdivisionesId
from backend.models.Paises import PaisesId
"""
1. que se cree con los datos correctos
2. que al crear una ciudad por una subdivision que no existe, se lance una excepcion
3. que al intentar crear una ciudad con subdivision borrada, salga un exepcion
4. que se muestre la excepcion si se encuentra borrado y se quiere borrar
5. que se muestre la excepcion si se busca un registro borrado 
6. que al buscar una ciudad muestre vacio si no existe en la db 
7. que muestre las borrados 
8. que lance lista vacia si no hay borrados 
9. crear registros y que mostrar_todos si los muestre 
10. que al restaurar un registro su estado "activo" sea true 
11. que al intentar meter un registro con el mismo nombre de ciudad, no se pueda y salga una excepción 
12. que al buscar ciudades por subdivisiones si salgan por subdivisiones
13. que si se busca ciudades por una subdivision que no existe, retorne vacio
14. que si se busca ciudades por una subdivision borrada, retorne exception
15. que al intentar restaurar un registro que esta activo, salga exepcion
16. que al buscar ciudades por pais si salgan por pais
17. que al buscar ciudades por paises que no existen, salga la exepcion
18. que al buscar ciudades por paises que estan borrados, salga la excepcion

"""
class TestCiudades:
    def iniciaciones(self):
        self.colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamentos")
        self.ecuador = PaisesId(nombre_pais="Ecuador", nombre_subdivisiones="Provincias")
        self.cundinamarca = SubdivisionesId(nombre_subdivision="cundinamarca", id_pais=1)
        self.antioquia = SubdivisionesId(nombre_subdivision="Antioquia", id_pais=1)
        self.eloro = SubdivisionesId(nombre_subdivision="El Oro", id_pais=2)
        self.azuay = SubdivisionesId(nombre_subdivision="Azuay", id_pais=2)
        self.bogota = CiudadesId(nombre_ciudad="Bogota", id_subdivision=1)
        self.girardot = CiudadesId(nombre_ciudad="Girardot", id_subdivision=1)
        self.medellin = CiudadesId(nombre_ciudad="Medellin", id_subdivision=2)
        self.envigado = CiudadesId(nombre_ciudad="Envigado", id_subdivision=2)
        self.machala = CiudadesId(nombre_ciudad="Machala", id_subdivision=3)
        self.zaruma = CiudadesId(nombre_ciudad="Zaruma", id_subdivision=3)
        self.cuenca = CiudadesId(nombre_ciudad="Cuenca", id_subdivision=4)
        self.gualaceo = CiudadesId(nombre_ciudad="Gualaceo", id_subdivision=4)

    def iniciaciones_json(self):
        self.bogota_json = {"nombre_ciudad": "Bogota", "id_subdivision": 1}
        self.girardot_json = {"nombre_ciudad": "Girardot", "id_subdivision": 1}
        self.medellin_json = {"nombre_ciudad": "Medellin", "id_subdivision": 2}
        self.envigado_json = {"nombre_ciudad": "Envigado", "id_subdivision": 2}
        self.machala_json = {"nombre_ciudad": "Machala", "id_subdivision": 3}
        self.zaruma_json = {"nombre_ciudad": "Zaruma", "id_subdivision": 3}
        self.cuenca_json = {"nombre_ciudad": "Cuenca", "id_subdivision": 4}
        self.gualaceo_json = {"nombre_ciudad": "Gualaceo", "id_subdivision": 4}


    # 1
    def test_crear_ciudad(self, client, session):
        self.iniciaciones()
        self.iniciaciones_json()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        bogota_json = self.bogota_json
        session.add_all([colombia, cundinamarca])
        r = client.post("/ciudades", json=bogota_json)
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_ciudad"] == "Bogota"
        assert res["id_subdivision"] == 1

    # 2
    def test_ciudad_subdivision_inexistente(self, client):
        self.iniciaciones_json()
        envigado = self.envigado_json
        r = client.post("/ciudades", json=envigado)
        res = r.json()
        assert r.status_code == 422
        assert res["detail"] == "la clave foranea id_subdivision no tiene registro con el valor 2"

    # 3
    def test_ciudad_subdivision_borrada(self, client, session):
        self.iniciaciones()
        self.iniciaciones_json()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        bogota_json = self.bogota_json
        cundinamarca.activo = False
        session.add_all([colombia, cundinamarca])
        session.commit()
        r = client.post("/ciudades", json=bogota_json)
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 4
    def test_ciudad_borrar_borrado(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        antioquia = self.antioquia
        medellin = self.medellin
        medellin.activo = False
        session.add_all([colombia, antioquia, medellin])
        r = client.post("/ciudades-borrar", params={'id': 1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 5
    def test_ciudad_buscar_borrado(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        antioquia = self.antioquia
        medellin = self.medellin
        medellin.activo = False
        session.add_all([colombia, antioquia, medellin])
        r = client.get("/ciudad", params={'id': 1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 6
    def test_ciudad_inexistente(self, session, client):
        self.iniciaciones()
        ecuador = self.ecuador
        eloro = self.eloro
        machala = self.machala
        session.add_all([ecuador, eloro, machala])
        r = client.get("/ciudad", params={'id': 2})
        res = r.json()
        assert r.status_code == 200
        assert not res
    # 7
    def test_ciudades_mostrar_borrados(self, session, client):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        antioquia = self.antioquia
        bogota = self.bogota
        girardot = self.girardot
        medellin = self.medellin
        envigado = self.envigado
        bogota.activo = False
        envigado.activo = False
        session.add_all([colombia, cundinamarca, antioquia, bogota, medellin, girardot, envigado])
        session.commit()
        r = client.get("/ciudades-borradas")
        res = r.json()
        assert r.status_code == 200
        assert len(res) == 2
        assert res[0]["nombre_ciudad"] == "Bogota"
        assert res[1]["nombre_ciudad"] == "Envigado"

    # 8
    def test_ciudades_no_borradas(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        antioquia = self.antioquia
        bogota = self.bogota
        girardot = self.girardot
        medellin = self.medellin
        envigado = self.envigado
        session.add_all([colombia, cundinamarca, antioquia, bogota, medellin, girardot, envigado])
        session.commit()
        r = client.get("/ciudades-borradas")
        res = r.json()
        assert r.status_code == 200
        assert res == []

    # 9
    def test_ciudades_mostrar(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        antioquia = self.antioquia
        bogota = self.bogota
        girardot = self.girardot
        medellin = self.medellin
        envigado = self.envigado
        session.add_all([colombia, cundinamarca, antioquia, bogota, medellin, girardot, envigado])
        session.commit()
        r = client.get("/ciudades")
        res = r.json()
        assert r.status_code == 200
        assert len(res) == 4
        assert res[0]["nombre_ciudad"] == "Bogota"
        assert res[1]["nombre_ciudad"] == "Medellin"
        assert res[2]["nombre_ciudad"] == "Girardot"
        assert res[3]["nombre_ciudad"] == "Envigado"

    # 10
    def test_ciudades_restaurar(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        antioquia = self.antioquia
        medellin = self.medellin
        medellin.activo = False
        medellin.id_subdivision = 1
        session.add_all([colombia, antioquia, medellin])
        r = client.post("/ciudad-restaurar", params={'id':1})
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_ciudad"] == "Medellin"
        assert res["id_subdivision"] == 1
        r = client.get("/ciudad", params={'id':1})
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_ciudad"] == "Medellin"
        assert res["id_subdivision"] == 1

    # 11
    def test_ciudades_repetidas(self, client, session):
        self.iniciaciones()
        self.iniciaciones_json()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        bogota = self.bogota
        bogota_json = self.bogota_json
        session.add_all([colombia, cundinamarca, bogota])
        session.commit()
        r = client.post("/ciudades", json=bogota_json)
        res = r.json()
        assert r.status_code == 409
        assert res["detail"] == "los valores ['Bogota'] ya se encuentran registrados"

    # 12
    def test_ciudades_subdivision(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        antioquia = self.antioquia
        bogota = self.bogota
        girardot = self.girardot
        medellin = self.medellin
        envigado = self.envigado
        session.add_all([colombia, cundinamarca, antioquia, bogota, girardot, medellin, envigado])
        session.commit()
        r = client.get("/ciudades-subdivision", params={'id':1})
        res = r.json()
        assert r.status_code == 200
        assert len(res) == 2
        assert res[0]["nombre_ciudad"] == "Bogota"
        assert res[1]["nombre_ciudad"] == "Girardot"
        r = client.get("/ciudades-subdivision", params={'id': 2})
        res = r.json()
        assert r.status_code == 200
        assert len(res) == 2
        assert res[0]["nombre_ciudad"] == "Medellin"
        assert res[1]["nombre_ciudad"] == "Envigado"

    # 13
    def test_ciudades_subdivsion_inexistente(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        antioquia = self.antioquia
        bogota = self.bogota
        girardot = self.girardot
        medellin = self.medellin
        envigado = self.envigado
        session.add_all([colombia, cundinamarca, antioquia, bogota, girardot, medellin, envigado])
        session.commit()
        r = client.get("/ciudades-subdivision", params={'id': 3})
        res = r.json()
        assert r.status_code == 404
        assert res["detail"] == "3 no existe"

    # 14
    def test_ciudades_subdivsion_borrada(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        antioquia = self.antioquia
        bogota = self.bogota
        girardot = self.girardot
        medellin = self.medellin
        envigado = self.envigado
        antioquia.activo = False
        session.add_all([colombia, cundinamarca, antioquia, bogota, girardot, medellin, envigado])
        session.commit()
        r = client.get("/ciudades-subdivision", params={'id': 2})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 2 se encuentra borrado"

    # 15
    def test_ciudades_restaurar_no_borrado(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        bogota = self.bogota
        session.add_all([colombia, cundinamarca, bogota])
        session.commit()
        r = client.post("/ciudad-restaurar", params={'id': 1})
        res = r.json()
        assert r.status_code == 409
        assert res["detail"] == "El registro 1 no se encuentra borrado"

    # 16
    def test_ciudades_por_pais(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        antioquia = self.antioquia
        bogota = self.bogota
        medellin = self.medellin
        girardot = self.girardot
        envigado = self.envigado

        session.add_all([colombia, cundinamarca, antioquia, bogota, medellin, girardot, envigado])
        session.commit()

        r = client.get("/ciudades-pais", params={"id": 1})
        res = r.json()
        assert r.status_code == 200
        assert len(res) == 4
        assert res[0]["nombre_ciudad"] == "Bogota"
        assert res[1]["nombre_ciudad"] == "Medellin"
        assert res[2]["nombre_ciudad"] == "Girardot"
        assert res[3]["nombre_ciudad"] == "Envigado"
        print(res)

        session.add_all([colombia, cundinamarca, antioquia, bogota, medellin, girardot, envigado])
        session.commit()

        ecuador = self.ecuador
        eloro = self.eloro
        azuay = self.azuay
        machala = self.machala
        zaruma = self.zaruma
        cuenca = self.cuenca
        gualaceo = self.gualaceo

        session.add_all([ecuador, eloro, azuay, machala, zaruma, cuenca, gualaceo])
        session.commit()

        r = client.get("/ciudades-pais", params={"id": 2})
        res = r.json()
        assert r.status_code == 200
        assert len(res) == 4
        assert res[0]["nombre_ciudad"] == "Machala"
        assert res[1]["nombre_ciudad"] == "Zaruma"
        assert res[2]["nombre_ciudad"] == "Cuenca"
        assert res[3]["nombre_ciudad"] == "Gualaceo"
        print(res)

    # 17
    def test_ciudades_por_pais_inexistente(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        antioquia = self.antioquia
        bogota = self.bogota
        medellin = self.medellin
        girardot = self.girardot
        envigado = self.envigado

        session.add_all([colombia, cundinamarca, antioquia, bogota, medellin, girardot, envigado])
        session.commit()

        r = client.get("/ciudades-pais", params={'id': 2})
        res = r.json()
        assert r.status_code == 404
        assert res["detail"] == "2 no existe"

    # 18
    def test_ciudades_por_pais_borrado(self, client, session):
        self.iniciaciones()
        colombia = self.colombia
        cundinamarca = self.cundinamarca
        antioquia = self.antioquia
        bogota = self.bogota
        medellin = self.medellin
        girardot = self.girardot
        envigado = self.envigado
        colombia.activo = False

        session.add_all([colombia, cundinamarca, antioquia, bogota, medellin, girardot, envigado])
        session.commit()

        r = client.get("/ciudades-pais", params={'id': 1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"