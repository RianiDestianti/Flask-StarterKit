from routes.router import Router
from middleware.auth_middleware import admin_only, auth_middleware
from controllers.admin.user_controller import UserController
from controllers.admin.role_controller import RoleController

admin = Router('admin', __name__)

user_controller         = UserController()
role_controller         = RoleController()

admin.get('/roles' , auth_middleware , admin_only , role_controller.get_data)

admin.get('/users' , auth_middleware , admin_only , user_controller.get_data)
admin.post('/user/action' , auth_middleware , admin_only , user_controller.action_data)
admin.get('/user/:id' , auth_middleware , admin_only , user_controller.get_detail)
admin.get('/user/delete/:id' , auth_middleware , admin_only , user_controller.delete_data)
