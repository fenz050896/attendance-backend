from app.seeds import Seeder

from app.models.user_role_model import UserRoleModel

class UserRoleSeeder(Seeder):
  def __init__(self):
    super().__init__(1)

  def run(self):
    print('=============== Running UserRoleSeeder ===============')

    UserRoleModel.create_many([
      { 'role_id': 1, 'role_name': 'Administrator' },
      { 'role_id': 2, 'role_name': 'User' },
    ], commit=True)

    print('=============== Finish UserRoleSeeder ===============')
