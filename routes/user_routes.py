from routes.router import Router
from controllers.auth_controller import AuthController
from controllers.user.profile_controller import ProfileController
from middleware.auth_middleware import auth_middleware

user = Router('user', __name__)

auth_controller         = AuthController()
profile_controller      = ProfileController()

user.post('/login', auth_controller.login)
user.post('/register', auth_controller.register)
user.post('/verify', auth_controller.verify)
user.post('/retry-code', auth_controller.retry_code)
user.post('/reset-password', auth_controller.reset_password)

user.get('/check-auth', auth_middleware, profile_controller.get_profile)
user.post('/profile/action', auth_middleware, profile_controller.action)
