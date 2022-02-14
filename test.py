from random import choice
import unittest
from unittest.mock import patch
import questionnaire
import questionnaire_import
import os
import json

class QuestionTest(unittest.TestCase):
    def test_question_good_or_bad_answere(self):
        choices = ('choice_one', 'choice_two', 'choice_tree')
        q = questionnaire.Question('Question_title', choices, 'choice_two')
        with patch('builtins.input', return_value='1'):
            self.assertFalse(q.poser())
        with patch('builtins.input', return_value='2'):
            self.assertTrue(q.poser())

class SurveyTest(unittest.TestCase):
    def test_harry_potter_survey_confirme(self):
        filename = 'cinema_harrypotter_confirme.json'
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)
        self.assertEqual(len(q.questions), 20)
        self.assertEqual(q.title, 'Harry Potter')
        self.assertEqual(q.category, 'Cinéma')
        self.assertEqual(q.level, 'confirmé')

        with patch('builtins.input', return_value='1'):
            self.assertEqual(q.lancer(), 7)

    def test_invalid_survey(self):
        filename = 'blabla.json'
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)
        self.assertEqual(q.category, 'inconnu')
        self.assertEqual(q.level, 'inconnu')
        self.assertIsNotNone(q.questions)
        
        filename = 'blabla2.json'
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)

class ImportTest(unittest.TestCase):
    def test_import_json_format(self):
        questionnaire_import.generate_json_file("Cinéma", "Harry Potter", "https://www.kiwime.com/oqdb/files/1003995292/OpenQuizzDB_003/openquizzdb_3.json")
        filenames = (
            'cinema_harrypotter_debutant.json',
            'cinema_harrypotter_confirme.json',
            'cinema_harrypotter_expert.json',
        )

        for filename in filenames:
            self.assertTrue(os.path.isfile(filename))

            file = open(filename, 'r')
            json_data = file.read()
            file.close
            try:
                data = json.loads(json_data)
            except:
                self.fail(f'Deserialize issue on file {filename}')

            self.assertIsNotNone(data.get('titre'))
            self.assertIsNotNone(data.get('questions'))
            self.assertIsNotNone(data.get('categorie'))
            self.assertIsNotNone(data.get('difficulte'))

            for question in data.get('questions'):
                self.assertIsNotNone(question.get('titre'))
                self.assertIsNotNone(question.get('choix'))
                for choix in question.get('choix'):
                    self.assertGreater(len(choix[0]), 0)
                    self.assertTrue(isinstance(choix[1], bool))
                    good_answere = [i for i in question.get('choix') if i[1]]
                    self.assertEqual(len(good_answere), 1)
unittest.main()

