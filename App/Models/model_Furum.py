
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

