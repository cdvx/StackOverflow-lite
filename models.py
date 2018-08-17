
answersList = [
{'answerId': 1,
    'Qn_Id': 1,
    'body': '''Lorem ipsum dolor sit amet, consectetur adipiscing 
    elit.Vivamus nec tortor ac purus luctus lobortis id et magna.
    Pellentesque id odio volutpat, fermentum neque non, 
    vestibulum enim.Vivamus aliquet libero quis orci mattis 
    tincidunt.'''},
{'answerId': 2,
    'Qn_Id': 2,
    'body': '''What's programmingLorem ipsum dolor sit amet, 
    consectetur adipiscing elit.Vivamus nec tortor ac purus 
    luctus lobortis id et magna.Pellentesque id odio volutpat, 
    fermentum neque non, vestibulum enim.Vivamus aliquet libero 
    quis orci mattis tincidunt.'''},
{'answerId': 3,
    'Qn_Id': 3,
    'body': '''What are data structuresLorem ipsum dolor sit amet, 
    consectetur adipiscing elit.Vivamus nec tortor ac purus luctus 
    lobortis id et magna.Pellentesque id odio volutpat, fermentum neque non, 
    vestibulum enim.Vivamus aliquet libero quis orci mattis tincidunt.'''},
{'answerId': 4,
    'Qn_Id': 4,
    'body': '''Lorem ipsum dolor sit amet, consectetur adipiscing 
    elit.Vivamus nec tortor ac purus luctus lobortis id et magna.
    Pellentesque id odio volutpat, fermentum neque non, 
    vestibulum enim.Vivamus aliquet libero quis orci mattis 
    tincidunt.'''}
]



class Question:
    def __init__(self, questionId=0, topic='', body=''):
        self.id = questionId
        self.topic = topic
        self.body = body
        self.answers =[]

    def __repr__(self):
        return {
            'questionId': self.id,
            'topic': self.topic,
            'body': self.body
        }



def createQnsList():
    QnsList =[]
    body= '''Lorem ipsum dolor sit amet, consectetur adipiscing 
        elit.Vivamus nec tortor ac purus luctus lobortis id et magna.
        Pellentesque id odio volutpat, fermentum neque non, vestibulum 
        enim.Vivamus aliquet libero quis orci mattis tincidunt.'''

    topics = [0,'python','comp science','AI','blockchain','ethereum']

    for i in range(1,6):
        Qn = Question(i,topics[i],body)

        for answer in answersList:
            if answer['Qn_Id'] == Qn.id:
                Qn.answers.append(answer)

        QnsList.append(Qn.__repr__())
    return QnsList


questionsList = createQnsList()


qnIds = [id for id in [question['questionId'] for question in questionsList]]
class Answer:
    def __init__(self, answerId=0, body='', Qn_Id=0):
        self.answerId = answerId
        self.body = body
        self.Qn_Id = Qn_Id

    def __repr__(self):
        return {
            'answerId': self.answerId,
            'Qn_Id': self.Qn_Id,
            'body': self.body
        }
        

