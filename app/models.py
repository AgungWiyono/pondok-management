import datetime
import pytz

from sqlalchemy import event

from app import db


def get_now_time():
    return datetime.datetime.now(pytz.timezone("Asia/Jakarta"))


class Angkatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True, unique=True, nullable=False)
    students = db.relationship("Student", lazy="dynamic", backref="angkatan")

    def __repr__(self):
        return self.name


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, index=True, unique=True)
    username = db.Column(db.String(16), nullable=False)
    angkatan_id = db.Column(db.Integer, db.ForeignKey("angkatan.id"))
    jadwals = db.relationship(
        "Jadwal", secondary="absensi_jadwal", backref="student", lazy="dynamic"
    )

    def __repr__(self):
        return self.username


class Hari(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True, nullable=False)
    iso_week_day = db.Column(db.Integer, unique=True)
    jadwals = db.relationship("Jadwal", lazy="dynamic", backref="hari")

    def __repr__(self):
        return self.name


class Kegiatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True, nullable=False)
    note = db.Column(db.Text)
    jadwals = db.relationship("Jadwal", lazy="dynamic", backref="kegiatan")

    def __repr__(self):
        return self.name


class Jadwal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kegiatan_id = db.Column(db.Integer, db.ForeignKey("kegiatan.id"))
    hari_id = db.Column(db.Integer, db.ForeignKey("hari.id"))
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    late_time = db.Column(db.Time, nullable=False)
    active = db.Column(db.Boolean, default=True)
    students = db.relationship(
        "Student", secondary="absensi_jadwal", backref="jadwal", lazy="dynamic"
    )
    pelaksanaan_list = db.relationship(
        "Pelaksanaan", backref="jadwal", lazy="dynamic"
    )

    def __repr__(self):
        return f"{self.kegiatan.name}:{self.hari.name}"


class Pelaksanaan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    jadwal_id = db.Column(db.Integer, db.ForeignKey("jadwal.id"))

    def __repr__(self):
        return f"{self.jadwal.kegiatan.name}:{self.date}"


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_time = db.Column(db.Time, default=get_now_time(), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    pelaksanaan_id = db.Column(db.Integer, db.ForeignKey("pelaksanaan.id"))
    status_hadir_id = db.Column(db.Integer, db.ForeignKey("status_hadir.id"))
    students = db.relationship("Student", backref="attendances")
    pelaksanaans = db.relationship("Pelaksanaan", backref="attendances")
    status = db.relationship("StatusHadir", backref="attendances")

    def __repr__(self):
        return f"{self.id}"


class StatusHadir(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)

    def __repr__(self):
        return self.name


absensi_jadwal = db.Table(
    "absensi_jadwal",
    db.Column(
        "jadwal_id", db.Integer, db.ForeignKey("jadwal.id"), primary_key=True
    ),
    db.Column(
        "student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True
    ),
    db.Column("status_hadir_id", db.Integer, db.ForeignKey("status_hadir.id")),
    db.Column("note", db.Text),
)


def check_day_iso(mapper, connection, target):
    if target.iso_week_day > 7:
        raise Exception("Week Day can't be greater than 7")


event.listen(Hari, "before_insert", check_day_iso)
