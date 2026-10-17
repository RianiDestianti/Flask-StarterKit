from models.role_model import RoleModel


class RoleController:
    def get_data(self):

        data = [{
            'id'      : item.id,
            'name'    : item.name,
        } for item in RoleModel.query.all()]

        return {
            'status'  : 200,
            'message' : 'Success return data',
            'data'    : data
        }
