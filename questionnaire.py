import json

class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def FromJsonData(data):
        choix = [i[0] for i in data['choix']]
        bonne_reponse = [i[0] for i in data['choix'] if i[1] == True]
        if len(bonne_reponse) != 1:
            return None
        q = Question(data['titre'], choix, bonne_reponse[0])
        return q

    def poser(self):
        print("QUESTION")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
class Questionnaire:
    def __init__(self, questions, category, title, level):
        self.questions = questions
        self.category = category
        self.title = title
        self.level = level

    def lancer(self):
        score = 0
        question_num = 1

        print('--------------------------------------------')
        print(f'QUESTIONNAIRE: {self.title}')
        print(f'Catégorie: {self.category}')
        print(f'Difficulté: {self.level}')
        print(f'Nombre de questions: {len(self.questions)}')
        print('--------------------------------------------')

        for question in self.questions:
            print(f'Question {question_num}/{len(self.questions)}')
            if question.poser():
                score += 1
            question_num += 1
        print("Score final :", score, "sur", len(self.questions))
        return score

    def from_json_data(data):
        questionary_data_question = data['questions']
        questions = [Question.FromJsonData(i) for i in questionary_data_question]
        return Questionnaire(questions, data['categorie'], data['titre'], data['difficulte'])


json_file = open('cinema_harrypotter_confirme.json', 'r')
json_data = json_file.read()
json_file.close()
questionary_data = json.loads(json_data)


Questionnaire.from_json_data(questionary_data).lancer()