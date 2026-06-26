# controllers/base_controller.py
from flask import jsonify, request

class BaseController:
    def __init__(self, service, model_class):
        self.service = service
        self.model_class = model_class

    def create(self):
        data = request.json
        try:
            entity = self.model_class(**data)
            entity_id = self.service.create(entity)
            return jsonify({"message": "Criado com sucesso", "id": entity_id}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def read(self, entity_id):
        entity = self.service.read(entity_id)
        if entity:
            return jsonify(entity.__dict__), 200
        return jsonify({"error": "Não encontrado"}), 404

    def update(self, entity_id):
        data = request.json
        try:
            entity = self.model_class(id=entity_id, **data)
            linhas = self.service.update(entity)
            if linhas:
                return jsonify({"message": "Atualizado com sucesso"}), 200
            return jsonify({"error": "Não encontrado"}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def delete(self, entity_id):
        linhas = self.service.delete(entity_id)
        if linhas:
            return jsonify({"message": "Excluído com sucesso"}), 200
        return jsonify({"error": "Não encontrado"}), 404
