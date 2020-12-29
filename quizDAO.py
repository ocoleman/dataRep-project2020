import mysql.connector
from mysql.connector import cursor
import dbconfig as cfg
class QuizDAO:

    db=""
    #connect function
    def connectToDB(self):
        self.db = mysql.connector.connect(
            host=       cfg.mysql['host'],
            user=       cfg.mysql['user'],
            password=   cfg.mysql['password'],
            database=   cfg.mysql['database']
        )
    #connects on launch
    def __init__(self): 
        self.connectToDB()

    #get cursor object
    def getCursor(self):
        if not self.db.is_connected():
            self.connectToDB()
        return self.db.cursor()
    
    #get dict cursor object
    def getDictCursor(self):
        if not self.db.is_connected():
            self.connectToDB()
        return self.db.cursor(dictionary=True)

    #Inserts new user details to database
    def createUser(self, username, password):
        cursor = self.getCursor()
        sql="INSERT INTO user (username, password) VALUES (%s,%s)"
        values=(username,password)
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()
        
    #Gets a user by name and password
    def getUser(self, username, password):
        cursor = self.getDictCursor()
        sql="select * from user where username=%s and password=%s"
        values=(username,password)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    #checks if a user already exists
    def checkForUser(self, username):
        cursor = self.getDictCursor()
        sql="select * from user where username=%s"
        values=(username,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        return result

    #Creates a trivia question in the database
    def create(self, question):
        cursor = self.getCursor()
        sql="insert into questions (author,category,correct_answer,difficulty,incorrect_answers,question,type) values (%s,%s,%s,%s,%s,%s,%s)"
        values = [
            question["author"],
            question["category"],
            question["correct_answer"],
            question["difficulty"],
            question["incorrect_answers"],
            question["question"],
            question["type"],
        ]
        cursor.execute(sql, values)
        self.db.commit()
        lastRowId=cursor.lastrowid
        cursor.close()
        return lastRowId

    #Gets all trivia questions in the database
    def getAll(self):
        cursor = self.getCursor()
        sql="select * from questions"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        cursor.close()
        return returnArray

    #Find a question by id
    def findById(self, id):
        cursor = self.getCursor()
        sql="select * from questions where id in (%s)"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        question=self.convertToDictionary(result)
        cursor.close()
        return question

    #Update a question with the values passed in
    def update(self, values):
        cursor = self.getCursor()
        sql="update questions set author = %s,category = %s,correct_answer = %s,difficulty = %s,incorrect_answers = %s,question = %s,type = %s  where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()

    #delete a question by id
    def delete(self, id):
        cursor = self.getCursor()
        sql="delete from questions where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()

    #Get 10 random questions from the database    
    def findRandom(self):
        cursor = self.getCursor()
        sql = "SELECT * FROM questions ORDER BY RAND() LIMIT 10;"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        cursor.close()
        return returnArray

    #convert mysql response to a dict
    def convertToDictionary(self, result):
        colnames=['id','author','category',"correct_answer","incorrect_answers","type","difficulty","question"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item

quizDAO = QuizDAO()