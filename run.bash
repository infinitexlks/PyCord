flask shell
from app.extensions import db
db.create_all()
exit()
