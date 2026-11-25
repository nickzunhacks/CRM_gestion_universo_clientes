from backend.models import TipoIdentificacion, TipoIdentificacionId

"""
pruebas tipos de id
1. que se cree con los datos correctos 	post /tipos-id
2. que se muestre la excepcion si se encuentra borrado y se quiere borrar 	post /tipo-id-borrar
3. que se muestre la excepcion si se busca un registro borrado 	get /tipo-id
4. que muestre vacio si no existe en la db 	get /tipo-id
5. que muestre las borrados 	get /tipo-id-borrados
6. que lance lista vacia si no hay borrados 	get /tipo-id-borrados
7. crear registros y que mostrar_todos si los muestre 	post /tipos-id y /tipos-id
8. que al restaurar un registro su estado "activo" sea true 	post /tipo-id-restaurar
9. que al intentar meter un registro con el mismo nombre de id, no se pueda y salga una excepcion	post /tipos-id

"""

class TestTipoIdentificacion:

    def iniciar_tipo_id(self, session):
        NIT = TipoIdentificacionId(nombre_tipo_identificacion="NIT")
        RUC = TipoIdentificacionId(nombre_tipo_identificacion="RUC")
        RUT = TipoIdentificacionId(nombre_tipo_identificacion="RUT")
        LEI = TipoIdentificacionId(nombre_tipo_identificacion="LEI")
        FOLIO_MERCANTIL = TipoIdentificacionId(nombre_tipo_identificacion="FOLIO_MERCANTIL")
        lista = [NIT, RUC, RUT, LEI, FOLIO_MERCANTIL]
        session.add_all([NIT, RUC, RUT, LEI, FOLIO_MERCANTIL])
        session.commit()
        for id in lista:
            session.refresh(id)
        return lista

    def iniciar_tipo_id_json(self):
        tipos_de_id = \
        [
            {"nombre_tipo_identificacion":"NIT"}, {"nombre_tipo_identificacion":"RUC"}, {"nombre_tipo_identificacion":"RUT"},
            {"nombre_tipo_identificacion":"LEI"}, {"nombre_tipo_identificacion":"FOLIO MERCANTIL"}
        ]
        return tipos_de_id

    # 1. que se cree con los datos correctos 	post /tipos-id
    def test_crear_tipo_identificacion(self, client):
        lista_tipos_de_id = self.iniciar_tipo_id_json()
        r = client.post("/tipos-id", json=lista_tipos_de_id[0])
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_tipo_identificacion"] == "NIT"
        assert res["id_tipo_identificacion"] == 1

    # 2. que se muestre la excepcion si se encuentra borrado y se quiere borrar 	post /tipo-id-borrar
    def test_borrar_borrado(self, client, session):
        lista_tipos_de_id = self.iniciar_tipo_id(session)
        lista_tipos_de_id[0].activo = False
        r = client.post('/tipo-id-borrar', params={"id":1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    # 3. que se muestre la excepcion si se busca un registro borrado 	get /tipo-id
    def test_buscar_borrado(self, client, session):
        lista_tipos_de_id = self.iniciar_tipo_id(session)
        lista_tipos_de_id[0].activo = False
        r = client.get('/tipo-id', params={"id":1})
        res = r.json()
        assert r.status_code == 410
        assert res["detail"] == "El registro 1 se encuentra borrado"

    #4. que muestre vacio si no existe en la db 	get /tipo-id
    def test_buscar_vacio(self, client, session):
        r = client.get('/tipo-id', params={"id": 1})
        res = r.json()
        assert r.status_code == 200
        assert res == None

    # 5. que muestre las borrados 	get /tipo-id-borrados
    def test_mostrar_borrados(self, client, session):
        lista_tipos_de_id = self.iniciar_tipo_id(session)
        lista_tipos_de_id[0].activo = False
        lista_tipos_de_id[1].activo = False
        session.commit()
        r = client.get('/tipo-id-borrados')
        res = r.json()
        assert r.status_code == 200
        assert res[0]["nombre_tipo_identificacion"] == "NIT"
        assert res[0]["activo"] == False
        assert res[1]["nombre_tipo_identificacion"] == "RUC"
        assert res[1]["activo"] == False

    # 6. que lance lista vacia si no hay borrados 	get /tipo-id-borrados
    def test_ningun_borrado(self, client, session):
        self.iniciar_tipo_id(session)
        r = client.get('/tipo-id-borrados')
        res = r.json()
        assert r.status_code == 200
        assert res == []

    # 7. crear registros y que mostrar_todos si los muestre 	post /tipos-id y /tipos-id
    def test_mostrar_registros(self, client, session):
        self.iniciar_tipo_id(session)
        r = client.get('/tipos-id')
        res = r.json()
        assert r.status_code == 200
        assert res[0]["nombre_tipo_identificacion"] == "NIT"
        assert res[0]["id_tipo_identificacion"] == 1
        assert res[1]["nombre_tipo_identificacion"] == "RUC"
        assert res[1]["id_tipo_identificacion"] == 2
        assert res[2]["nombre_tipo_identificacion"] == "RUT"
        assert res[2]["id_tipo_identificacion"] == 3
        assert res[3]["nombre_tipo_identificacion"] == "LEI"
        assert res[3]["id_tipo_identificacion"] == 4
        assert res[4]["nombre_tipo_identificacion"] == "FOLIO_MERCANTIL"
        assert res[4]["id_tipo_identificacion"] == 5

    # 8. que al restaurar un registro su estado "activo" sea true 	post /tipo-id-restaurar

    def test_restaurar_registro(self, client, session):
        lista = self.iniciar_tipo_id(session)
        lista[0].activo = False
        session.commit()
        r = client.post('/tipo-id-restaurar', params={"id":1})
        res = r.json()
        assert r.status_code == 200
        assert res["nombre_tipo_identificacion"] == "NIT"
        assert res["id_tipo_identificacion"] == 1
        assert res["activo"] == True
        r = client.get('/tipos-id')
        res = r.json()
        assert r.status_code == 200
        assert res[0]["nombre_tipo_identificacion"] == "NIT"
        assert res[0]["id_tipo_identificacion"] == 1
        assert res[0]["activo"] == True

    # 9. que al intentar meter un registro con el mismo nombre de id, no se pueda y salga una excepcion	post /tipo-id-borrado
    def test_dato_repetido(self, client, session):
        self.iniciar_tipo_id(session)
        jsons = self.iniciar_tipo_id_json()
        r = client.post('/tipos-id', json=jsons[0])
        res = r.json()
        assert r.status_code == 409
        assert res["detail"] == "los valores ['NIT'] ya se encuentran registrados"