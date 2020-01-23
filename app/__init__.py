from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, name="absensi", template_mode="bootstrap3")

from app import models

admin.add_view(ModelView(models.Angkatan, db.session))
admin.add_view(ModelView(models.Student, db.session))
admin.add_view(ModelView(models.Hari, db.session))
admin.add_view(ModelView(models.Kegiatan, db.session))
admin.add_view(ModelView(models.Jadwal, db.session))
admin.add_view(ModelView(models.StatusHadir, db.session))
admin.add_view(ModelView(models.Pelaksanaan, db.session))
admin.add_view(ModelView(models.Attendance, db.session))
