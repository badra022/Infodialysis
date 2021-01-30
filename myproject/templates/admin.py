from myproject import db
from myproject.models import User


admin1 = User('admin@admin.com' , 'admin', 'admin', 'admin', 'admin' , '123')
db.session.add(admin1)
db.session.commit()
