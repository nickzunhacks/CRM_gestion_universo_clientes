from backend.models.Subdivisiones import SubdivisionesId
from backend.models.Paises import PaisesId
from endpoints import subdivisiones

"""
Que se quiere probar:
    1) validar que el pais al que pertenece la subdivision, si exista
    2) que al crear una subdivision, se cree con los datos correctos
    3) que al buscar todas las subdivisiones filtrados por pais, lo haga correctamente
    4) que al buscar una solo subdivision que no exista, se maneje correctamente el error
"""

class TestSubdivisiones:

    # 1

    def test_pais_no_existente(self, client):

        #agregamos subdivision sin antes crear un pais en la tabla paisesid
        subdivision = {"nombre_subdivision":"Cundinamarca", "pais":1}
        r = client.post("/subdivisiones", json=subdivision)

        # el manejo de error debe arrojar un codigo 422 de Unprocessable Entity ya que la clave foranea no existe
        assert r.status_code == 422
        assert r.json()["detail"] == f"la clave foranea pais no tiene registro con el valor 1"

    # 2

    def test_pais_existente(self, client, session):

        # Ahora si agregamos un pais antes de agregar una subdivision
        subdivision = {"nombre_subdivision": "Cundinamarca", "pais": 1}
        pais = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        session.add(pais)
        session.commit()

        # Debe arrojar un 200 ya que el pais ahora si existe. En este sentido el id debe ser 1 al ser el primer pais registrado.
        # Los datos de respuesta debe corresponder a los enviados
        r = client.post("/subdivisiones", json=subdivision)
        res = r.json()
        assert r.status_code == 200
        assert res["pais"] == 1
        assert res["nombre_subdivision"] == "Cundinamarca"

    # 3

    def test_buscar_subdivisiones_por_pais(self, client, session):

        colombia = PaisesId(nombre_pais="Colombia", nombre_subdivisiones="Departamento")
        ecuador = PaisesId(nombre_pais="Ecuador", nombre_subdivisiones="Provincia")
        cundinamarca = SubdivisionesId(nombre_subdivision="Cundinamarca", pais=1)
        antioquia = SubdivisionesId(nombre_subdivision="Antioquia", pais=1)
        azuay = SubdivisionesId(nombre_subdivision="Azuay", pais=2)
        bolivar = SubdivisionesId(nombre_subdivision="Bolivar", pais=2)

        session.add(colombia)
        session.add(ecuador)
        session.add(cundinamarca)
        session.add(antioquia)
        session.add(azuay)
        session.add(bolivar)
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