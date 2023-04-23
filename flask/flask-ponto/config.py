app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ponto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Definição dos modelos
class Student(db.Model):
    rfID = db.Column(db.String(100), primary_key=True)
    RAStudent = db.Column(db.Integer)
    nameStudent = db.Column(db.String(255))
    presenceStudent = db.Column(db.Integer)
    absenceStudent = db.Column(db.Integer)
    lateStudent = db.Column(db.Integer)
    isPresent = db.Column(db.Boolean, default=False)


class Entrance(db.Model):
    idEntrance = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timeEntrance = db.Column(db.DateTime, default=datetime.utcnow)
    rfID = db.Column(db.String(100), db.ForeignKey('student.rfID'))


class Exit(db.Model):
    idExit = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timeExit = db.Column(db.DateTime, default=datetime.utcnow)
    rfID = db.Column(db.String(100), db.ForeignKey('student.rfID'))
