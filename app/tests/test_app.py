from app.app import app, redis_store
from app.models import db, Term, Similar
import unittest



class AAFoodTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aafood-test.db'
        app.config['REDIS_URL'] = 'redis://localhost:6379/30'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.init_app(app)
            db.create_all()
            redis_store.init_app(app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        scan = redis_store.scan_iter()
        redis_store.flushdb()


class AppTestCase(AAFoodTestCase):

    def test_db_create(self):
        term_a = Term(english='test', chinese='測試')
        term_b = Term(english='bamboo', chinese='竹子')
        db.session.add(term_a)
        db.session.add(term_b)
        similar = Similar(x=term_a, y=term_b, score=0.8)
        term_a.similars.append(similar)
        print(len(Term.query.all()))

    def test_assertion(self):
        assert 10 + 10 == 20


    def test_pattern_match(self):
        from app.bot.intention_detector_utils import fetching_target_and_intention_jieba
        #target, bot = fetching_target_and_intention_jieba('幫我翻譯 avocado 的中文')
        target, bot = fetching_target_and_intention_jieba('冷笑話')


