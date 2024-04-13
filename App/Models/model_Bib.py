

class CoursModel:
    def __init__(self, data):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.titre = data.get('titre')
        self.image = data.get('image')
        self.description = data.get('description')
        self.repo = data.get('repo', [])
        self.repo_realname = data.get('repo_realname', [])
        self.username = data.get('username')
        self.user_star = data.get('user_star', [])
        self.user_save = data.get('user_save', [])
        self.profil = data.get('profil')
        self.role = data.get('role')
        self.downloadnumber = data.get('downloadnumber')
        self.starnumber = data.get('starnumber')
        self.date_added = data.get('date_added')
        self.discipline = data.get('discipline')
        self.type = data.get('type')
        self.prix = data.get('prix')
        self.stat = data.get('stat')


class RequestModel:
    def __init__(self, data):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.id_answer = data.get('id_answer', [])
        self.titre = data.get('titre')
        self.description = data.get('description')
        self.username = data.get('username')
        self.user_answer = data.get('user_answer', [])
        self.profil = data.get('profil')
        self.role = data.get('role')
        self.answernumber = data.get('starnumber')
        self.date_added = data.get('date_added')
        self.discipline = data.get('discipline')
        self.type = data.get('type')
        self.prix = data.get('prix')
        self.stat = data.get('stat')
        self.statut = data.get('statut')


