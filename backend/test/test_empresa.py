from backend.models.Empresa import EmpresaId
from datetime import date

empresa1 = EmpresaId(pais_empresa=1, tipo_identificacion_empresa=1, numero_identificacion_empresa="0989432789432",
                     razon_social="NICKZUN S.A.S", fecha_inicio_operaciones= date(2020, 9, 12)
                     )

empresa1_json = {
    "pais_empresa": 1,
    "tipo_identificacion_empresa": 1,
    "numero_identificacion_empresa": "0989432789432",
    "razon_social": "NICKZUN S.A.S",
    "fecha_inicio_operaciones": "2020-09-12",
}

class TestEmpresa:

    def test_lista_vacia(self, client):
        r = client.get("/empresas")

        # observamos si responde con una lista vacia la base de datos

        assert r.status_code == 200
        assert r.json() == []

    def test_insersion_empresa(self, client, session):
        session.add(empresa1)
        session.commit()

        r = client.get("/empresas")

        # agregamos a empresa 1 y observamos si los datos retornados en la lista si coinciden
        assert r.status_code == 200
        assert len(r.json()) == 1
        assert r.json()[0]["pais_empresa"] == 1
        assert r.json()[0]["tipo_identificacion_empresa"] == 1
        assert r.json()[0]["numero_identificacion_empresa"] == "0989432789432"
        assert r.json()[0]["razon_social"] == "NICKZUN S.A.S"
        assert r.json()[0]["fecha_inicio_operaciones"] == '2020-09-12'

    def test_error_integridad(self, client, session):

        r = client.post("/empresa", json=empresa1_json)
        assert r.status_code == 200
        res = r.json()

        #verificamos que el post pone los datos correctamente
        assert res["pais_empresa"] == 1
        assert res["tipo_identificacion_empresa"] == 1
        assert res["numero_identificacion_empresa"] == "0989432789432"
        assert res["razon_social"] == "NICKZUN S.A.S"
        assert res["fecha_inicio_operaciones"] == '2020-09-12'

        #observamos que si al intentar poner una empresa exactamente igual, deja o no (no deberia dejar)
        r = client.post("/empresa", json=empresa1_json)
        assert r.status_code == 409
        res = r.json()
        assert res['detail'] == "No se puede registrar una empresa con el mismo pais, numero y tipo de identificacion"