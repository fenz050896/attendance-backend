import json
from app.models.app_config_model import AppConfigModel

from app.seeds import Seeder

class AppConfigSeeder(Seeder):
  def __init__(self):
    super().__init__(0)

  def run(self):
    print('=============== Running AppConfigSeeder ===============')

    days = [
      { 'label': 'Senin', 'value': 0 },
      { 'label': 'Selasa', 'value': 1 },
      { 'label': 'Rabu', 'value': 2 },
      { 'label': 'Kamis', 'value': 3 },
      { 'label': 'Jum\'at', 'value': 4 },
    ]
    AppConfigModel.create_many([
      { 'field': 'clock_in', 'label': 'Jam Masuk', 'type': 'single', 'value': '09:00' },
      { 'field': 'clock_out', 'label': 'Jam Keluar', 'type': 'single', 'value': '17:00' },
      { 'field': 'work_days', 'label': 'Hari Kerja', 'type': 'multiple', 'value': json.dumps(days) },
    ], commit=True)

    print('=============== Finish AppConfigSeeder ===============')
