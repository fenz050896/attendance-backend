from argon2 import PasswordHasher
from faker import Faker

from app.seeds import Seeder

from app.models.user_model import UserModel
from app.models.user_profile_model import UserProfileModel

class UserSeeder(Seeder):
  def __init__(self):
    super().__init__(2)

  def run(self):
    print('=============== Running UserSeeder ===============')

    ph = PasswordHasher()
    password = ph.hash('secret2023')

    fake = Faker()

    users = [
      { 'full_name': 'Ananda Fitra', 'email': 'michaelfitrahjackson@gmail.com', 'password': password, 'role_id': 1 },
    ]

    for _ in range(2):
      users.append({
        'full_name': fake.name(),
        'email': fake.safe_email(),
        'password': password,
      })
    
    for user in users:
      user_model = UserModel.create(user)
      UserProfileModel.create({ 'user_id': user_model.id })

    UserModel.commit()
    UserProfileModel.commit()

    print('=============== Finish UserSeeder ===============')
