import mysql.connector
import dbconfig as cfg
class QuizDAO:
    
    def initConnectToDB(self):
        db = mysql.connector.connect(
            host=       cfg.mysql['host'],
            user=       cfg.mysql['user'],
            password=   cfg.mysql['password'],
            database=   cfg.mysql['database'],
            pool_name='my_connection_pool',
            pool_size=20,
            connection_timeout=300
        )
        return db

    def getConnection(self):
        db = mysql.connector.connect(
            pool_name='my_connection_pool'
        )
        return db

    def __init__(self): 
        db=self.initConnectToDB()
        db.close()

    def createUser(self, username, password):
        db = self.getConnection()
        cursor = db.cursor()
        sql="INSERT INTO user (username, password) VALUES (%s,%s)"
        values=(username,password)
        cursor.execute(sql, values)
        db.commit()
        db.close()
        
    def getUser(self, username, password):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from user where username=%s and password=%s"
        values=(username,password)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        db.close()
        return result
    
    def checkForUser(self, username):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from user where username=%s"
        values=(username,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return result


    def create(self, question):
        db = self.getConnection()
        cursor = db.cursor()
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
        db.commit()
        lastRowId=cursor.lastrowid
        db.close()
        return lastRowId

    def getAll(self):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select * from questions"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        db.close()
        return returnArray

    def findById(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select * from questions where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        question=self.convertToDictionary(result)
        db.close()
        return question

    def update(self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql="update questions set author = %s,category = %s,correct_answer = %s,difficulty = %s,incorrect_answers = %s,question = %s,type = %s  where id = %s"
        cursor.execute(sql, values)
        db.commit()
        db.close()

    def delete(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql="delete from questions where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        db.commit()
        db.close()
        
    def getQuestionIds(self):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "SELECT id FROM questions"
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        return results


    def convertToDictionary(self, result):
        colnames=['id','author','category',"correct_answer","incorrect_answers","type","difficulty","question"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item

quizDAO = QuizDAO()