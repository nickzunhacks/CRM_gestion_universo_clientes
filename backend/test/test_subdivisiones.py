from backend.models.Subdivisiones import SubdivisionesId
from backend.models.Paises import PaisesId

"""
pruebas subdivisiones
1. que al crear una subdivision por un país que no existe, se maneje el error (listo)
2. que se cree con los datos correctos (post /subdivisiones) (listo)
3. que al intentar crear un pais con registro borrado, salga un exepcion
4. que se muestre la excepcion si se encuentra borrado y se quiere borrar (post /subdivision-borrar) (listo)
5. que se muestre la excepcion si se busca un registro borrado (get /subdivision) (listo)
6. que muestre vacio si no existe en la db (get /subdivision) (listo)
7. que muestre las borrados (get /subdivisiones-borradas) (listo)
8. que lance lista vacia si no hay borrados (get /subdivisiones-borradas) (listo)
9. crear registros y que mostrar_todos si los muestre (get /subdivisiones) (listo)
10. que al restaurar un registro su estado "activo" sea true (post /subdivisiones-restaurar get /subdivision)
11. que al intentar meter un registro con el mismo nombre de subdivision y pais, no se pueda y salga una excepción (post /subdivisiones)
12. que al buscar subdivisiones por país si salgan por país (get /subdivisiones-país) (listo)
13. que si se busca divisiones por un país que no existe, retorne una excepcion (get /subdivisiones-país)
14. que si se busca divisiones por un país borrado, retorne exception (get /subdivisiones-país)
"""

class TestSubdivisiones:

    # 1
    def test_subdivision_pais_no_existente(self, client):

        #agregamos subdivision sin antes crear un pais en la tabla paisesid
        subdivision = {"nombre_subdivision":"Cundinamarca", "id_pais":1}
        r = client.post("/subdivisiones", json=subdivision)

        # el manejo de error debe arrojar un codigo 422 de Unprocessable Entity ya que la clave foranea no existe
        assert r.status_code == 422
        assert r.json()["detail"] == f"la clave foranea id_pais no tiene registro con el valor 1"

    # 2
    def test_subdivision_pais_existente(self, client, session):

        # Ahora si agregamos un pais antes de agregar una subdivision
        subdivision = {"nombre_subdivision": "Cundinamarca", "id_pais": 1}
        pais = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        session.add(pais)
        session.commit()

        # Debe arrojar un 200 ya que el pais ahora si existe. En este sentido el id debe ser 1 al ser el primer pais registrado.
        # Los datos de respuesta debe corresponder a los enviados
        r = client.post("/subdivisiones", json=subdivision)
        res = r.json()
        assert r.status_code == 200
        assert res["id_pais"] == 1
        assert res["nombre_subdivision"] == "Cundinamarca"

    # 3
    def test_subdivision_pais_borrado(self, client, session):
        pais = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento", activo=False)
        session.add(pais)
        session.commit()
        arauca = {"nombre_subdivision": "Arauca", "id_pais": 1}
        r = client.post("/subdivisiones", json=arauca)
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 4
    def test_borrar_subdivision_borrada(self, client, session):
        pais = PaisesId(nombre_pais="Argentina", nombre_subdivisiones="Pronvincia")
        session.add(pais)
        session.commit()
        subdivion = SubdivisionesId(nombre_subdivision="Fomosa", id_pais=1, activo=False)
        session.add(subdivion)
        session.commit()
        r = client.post("/subdivision-borrar", params={"id":1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 5
    def test_buscar_subdivision_borrada(self, client, session):

        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        cundinamarca = SubdivisionesId(nombre_subdivision="Cundinamarca", id_pais=1, activo=False)
        session.add(colombia)
        session.add(cundinamarca)
        session.commit()

        r = client.get("/subdivision", params={"id":1})
        res = r.json()

        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 6
    def test_buscar_subdivision_inexistente(self, client, session):
        r = client.get("/subdivision", params={"id":1})
        res = r.json()
        assert r.status_code == 200
        assert not res

    # 7
    def test_subdivisiones_borradas(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        bogota = SubdivisionesId(nombre_subdivision="Distrito Capital", id_pais=1, activo=False)
        antioquia = SubdivisionesId(nombre_subdivision="Antioquia", id_pais=1, activo=False)
        session.add_all([colombia, bogota, antioquia])
        session.commit()
        r = client.get("/subdivisiones-borradas")
        res = r.json()
        assert r.status_code == 200
        assert res[0]["nombre_subdivision"] == "Distrito Capital"
        assert res[1]["nombre_subdivision"] == "Antioquia"

    # 8
    def test_sin_borrados(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        bogota = SubdivisionesId(nombre_subdivision="Distrito Capital", id_pais=1)
        antioquia = SubdivisionesId(nombre_subdivision="Antioquia", id_pais=1)
        session.add_all([colombia, bogota, antioquia])
        session.commit()
        r = client.get("/subdivisiones-borradas")
        res = r.json()
        assert r.status_code == 200
        assert res == []

    # 9
    def test_mostrar_subdivisiones(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        bogota = SubdivisionesId(nombre_subdivision="Distrito Capital", id_pais=1)
        antioquia = SubdivisionesId(nombre_subdivision="Antioquia", id_pais=1)
        session.add_all([colombia, bogota, antioquia])
        session.commit()
        r = client.get("/subdivisiones")
        res = r.json()
        assert r.status_code == 200
        assert res[0]["nombre_subdivision"] == "Distrito Capital"
        assert res[1]["nombre_subdivision"] == "Antioquia"

    # 10
    def test_restuarar_subdivisiones(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        bogota = SubdivisionesId(nombre_subdivision="Distrito Capital", id_pais=1, activo=False)
        session.add_all([colombia, bogota])
        session.commit()
        r = client.post("/subdivisiones-restaurar", params={"id":1})
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_subdivision"] == "Distrito Capital"
        r = client.get("/subdivision", params={"id":1})
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_subdivision"] == "Distrito Capital"

    # 11
    def test_subdivision_repetida(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        bogota = SubdivisionesId(nombre_subdivision="Distrito Capital", id_pais=1, activo=False)
        session.add_all([colombia, bogota])
        session.commit()
        bogota_repetido = {"nombre_subdivision":"Distrito Capital", "id_pais":1}
        r = client.post("/subdivisiones", json=bogota_repetido)
        res = r.json()
        assert r.status_code == 409
        assert res["detail"] == "los valores ['Distrito Capital', 1] ya se encuentran registrados"

    # 12
    def test_buscar_subdivisiones_por_pais(self, client, session):

        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        ecuador = PaisesId(nombre_pais="Ecuador", nombre_subdivisiones="Provincia")
        cundinamarca = SubdivisionesId(nombre_subdivision="Cundinamarca", id_pais=1)
        antioquia = SubdivisionesId(nombre_subdivision="Antioquia", id_pais=1)
        azuay = SubdivisionesId(nombre_subdivision="Azuay", id_pais=2)
        bolivar = SubdivisionesId(nombre_subdivision="Bolivar", id_pais=2)

        session.add_all([colombia, ecuador, cundinamarca, antioquia, azuay, bolivar])
        session.commit()

        subdivisiones_colombia = {"pais":1}
        subdivisiones_ecuador = {"pais":2}

        r = client.get("/subdivisiones-pais", params=subdivisiones_colombia)

        res = r.json()

        assert r.status_code == 200
        assert res[0]["nombre_subdivision"] == "Cundinamarca"
        assert res[1]["nombre_subdivision"] == "Antioquia"

        r = client.get("/subdivisiones-pais", params=subdivisiones_ecuador)

        res = r.json()

        assert r.status_code == 200
        assert res[0]["nombre_subdivision"] == "Azuay"
        assert res[1]["nombre_subdivision"] == "Bolivar"

    # 13
    def test_buscar_divisiones_por_pais_inexistente(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        ecuador = PaisesId(nombre_pais="Ecuador", nombre_subdivisiones="Provincia")
        cundinamarca = SubdivisionesId(nombre_subdivision="Cundinamarca", id_pais=1)
        antioquia = SubdivisionesId(nombre_subdivision="Antioquia", id_pais=1)
        azuay = SubdivisionesId(nombre_subdivision="Azuay", id_pais=2)
        bolivar = SubdivisionesId(nombre_subdivision="Bolivar", id_pais=2)

        session.add_all([colombia, ecuador, cundinamarca, antioquia, azuay, bolivar])
        session.commit()

        r = client.get("/subdivisiones-pais", params={"pais":3})
        res = r.json()
        assert r.status_code == 404
        assert res["detail"] == "3 no existe"

    # 14
    def test_buscar_subdivisiones_por_pais_borrado(self, client, session):
        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento", activo=False)
        cundinamarca = SubdivisionesId(nombre_subdivision="Cundinamarca", id_pais=1)
        antioquia = SubdivisionesId(nombre_subdivision="Antioquia", id_pais=1)
        session.add_all([colombia, cundinamarca, antioquia])
        session.commit()
        r = client.get("/subdivisiones-pais", params={"pais":1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"