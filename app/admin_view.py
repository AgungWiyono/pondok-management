from flask_admin.contrib.sqla import ModelView

from app import models, admin, db

admin.add_view(ModelView(models.Angkatan, db.session))
admin.add_view(ModelView(models.Student, db.session))
admin.add_view(ModelView(models.Hari, db.session))
admin.add_view(ModelView(models.Kegiatan, db.session))
admin.add_view(ModelView(models.Jadwal, db.session))
admin.add_view(ModelView(models.StatusHadir, db.session))
admin.add_view(ModelView(models.Pelaksanaan, db.session))
admin.add_view(ModelView(models.Attendance, db.session))
