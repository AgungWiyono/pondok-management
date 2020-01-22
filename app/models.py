from app import db


class Angkatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True, unique=True, nullable=False)
    students = db.relationship("Student", lazy="dynamic")


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, index=True, unique=True)
    username = db.Column(db.String(16), nullable=False)
    angkatan_id = db.Column(db.Integer, db.ForeignKey("angkatan.id"))


class Hari(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True, nullable=False)


class Kegiatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True, nullable=False)
    note = db.Column(db.Text)
    jadwals = db.relationship("Jadwal", lazy="dynamic")


class Jadwal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kegiatan_id = db.Column(db.Integer, db.ForeignKey("kegiatan.id"))
    hari_id = db.Column(db.Integer, db.ForeignKey("hari.id"))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    late_time = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)
