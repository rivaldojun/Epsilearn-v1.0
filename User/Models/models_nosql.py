class PostModel:
    def __init__(self, data):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.content = data.get('content')
        self.replies = data.get('replies', [])
        self.username = data.get('username')
        self.file = data.get('file', [])
        self.profil = data.get('profil')
        self.role = data.get('role')
        self.likeuser = data.get('likeuser', [])
        self.likenumber = data.get('likenumber')
        self.date_added = data.get('date_added')
        self.tags = data.get('tags', [])
        self.top_topics = data.get('top_topics', 'none')


class Survey:
    def __init__(self, data):
        self.id = data.get('id')
        self.question = data.get('question')
        self.user_id = data.get('user_id')
        self.date = data.get('date')
        self.options = data.get('options', {})
        self.username = data.get('username')
        self.profil = data.get('profil')
        self.role = data.get('role')
        self.voteuser = data.get('voteuser', {})
        self.total = data.get('total', 0)


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

class NotifModel:
    def __init__(self, data):
        self.id = data.get('id')
        self.post_id = data.get('post_id')
        # self.createur_id = data.get('createur_id')
        # self.destinateur_id = data.get('destinateur_id')
        self.createur_name = data.get('createur_name')
        self.destinateur_name = data.get('destinateur_name')
        self.statut = data.get('statut')
        self.text= data.get('text')
        self.date_added= data.get('date_added')
       
class ActuModel:
    def __init__(self, data):
        self.id = data.get('id')
        self.post_id = data.get('post_id')
        self.user_vue = data.get('user_vue', [])


