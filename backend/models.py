from config import db


class Manga(db.Model):
    __tablename__ = "manga"
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    latest_chapter = db.Column(db.Float, nullable=True)
    current_chapter = db.Column(db.Float, nullable=False)
    chapter_diff = db.Column(db.Float, nullable=True)
    link = db.Column(db.String(200), nullable=True)
    website = db.Column(db.String(100), nullable=False)

    def __init__(
        self,
        image_url,
        title,
        rating,
        latest_chapter,
        current_chapter,
        chapter_diff,
        link,
        website,
    ):
        self.image_url = image_url
        self.title = title
        self.rating = rating
        self.latest_chapter = latest_chapter
        self.current_chapter = current_chapter
        self.chapter_diff = chapter_diff
        self.link = link
        self.website = website

    def __repr__(self):
        return f"<Manga: {self.title}>"

    def to_json(self):
        return {
            "id": self.id,
            "imageURL": self.image_url,
            "title": self.title,
            "rating": self.rating,
            "latestChapter": self.latest_chapter,
            "currentChapter": self.current_chapter,
            "chapterDiff": self.chapter_diff,
            "link": self.link,
            "website": self.website,
        }
