from db import db

class CarbonNewsModel(db.Model):
    __tablename__ = 'carbonnews'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), default=None)
    content = db.Column(db.String(80), default=None)
    sourceurl = db.Column(db.String(80), default=None)
    sourcedescription = db.Column(db.String(80), default=None)
    eventdate = db.Column(db.String(80), default=None)
    comment = db.Column(db.String(80), default=None)
    suggest = db.Column(db.String(80), default=None)
    speakingnote = db.Column(db.String(80), default=None)
    hashtag = db.Column(db.String(80), default=None)
    newsimage = db.Column(db.String(255), default=None)

    def __init__(self, title
                     , content
                     , sourceurl
                     , sourcedescription
                     , eventdate
                     , comment
                     , suggest
                     , speakingnote
                     , hashtag
                     , newsimage):

        self.title = title
        self.content = content
        self.sourceurl = sourceurl
        self.sourcedescription = sourcedescription
        self.eventdate = eventdate
        self.comment = comment
        self.suggest = suggest
        self.speakingnote = speakingnote
        self.hashtag = hashtag
        self.newsimage = newsimage

    def json(self):
        return {
                'title': self.title
                , 'content': self.content
                , 'sourceurl': self.sourceurl
                , 'sourcedescription': self.sourcedescription
                , 'eventdate': self.eventdate
                , 'comment': self.comment
                , 'suggest': self.suggest
                , 'speakingnote': self.speakingnote
                , 'hashtag': self.hashtag
                , 'newsimage': self.newsimage
                }

    @classmethod
    def find_by_hash_tag(cls, hashtag):
        return cls.query.filter_by(hashtag=hashtag).all()

    @classmethod
    def find_by_name(cls, title):
        return cls.query.filter_by(title=title).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
