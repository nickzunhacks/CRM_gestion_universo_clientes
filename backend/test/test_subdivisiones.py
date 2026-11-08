from backend.models.Subdivisiones import SubdivisionesId
from backend.models.Paises import PaisesId

class TestSubdivisiones:

    def test_pais_no_existente(self, client):

        #agregamos subdivision sin antes crear un pais en la tabla paisesid
        subdivision = {"nombre_subdivision":"Cundinamarca", "pais":1}
        r = client.post("/subdivisiones", json=subdivision)

        # el manejo de error debe arrojar un codigo 422 de Unprocessable Entity ya que la clave foranea no existe
        assert r.status_code == 422
        assert r.json()["detail"] == "Alguno de los datos enviados no esta registrado"

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
