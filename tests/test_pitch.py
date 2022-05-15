import unittest
from app.models import Pitch

class PitchModelTest(unittest.TestCase):

    def setUp(self):
        self.new_pitch = Pitch(id = 1, pitch_title = 'dance', pitch_content = 'Dance is life', category = 'entertainment', upvote = 0, downvote = 0, username = 'Rachel')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)

    def test_get_pitch_by_id(self):
        self.new_pitch.save_pitch()
        got_pitch = Pitch.get_pitch(1)
        self.assertTrue(got_pitch is not None)
