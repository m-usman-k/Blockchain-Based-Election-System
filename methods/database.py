import bcrypt
import sqlite3
import datetime
import secrets
import string

from structures.user import User
from structures.candidate import Candidate

# All Database Related Methods:
class Database:
    def __init__(self , db_name: str) -> None:
        self.db_name = db_name
        self.salt = bcrypt.gensalt()
        
        self.__create_tables__()
        
    def __connection__(self) -> sqlite3.Connection:
        with sqlite3.connect(self.db_name) as connection:
            return connection
        
        
    def __create_tables__(self) -> None:
        connection = self.__connection__()
        cursor = connection.cursor()
        
        cursor.execute(f"""
                       CREATE TABLE IF NOT EXISTS 'users' (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           cnic TEXT UNIQUE NOT NULL,
                           password TEXT NOT NULL,
                           national_vote INTEGER,
                           provincial_vote INTEGER,
                           session_key TEXT,
                           session_start_time TEXT)""")
        
        cursor.execute(f"""
                       CREATE TABLE IF NOT EXISTS 'candidates' (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           image TEXT NOT NULL,
                           name TEXT NOT NULL,
                           party TEXT NOT NULL,
                           poll_id INTEGER NOT NULL)""")
        
        cursor.close()
        connection.commit()
        connection.close()
        
    def __signup__(self , data: dict) -> User | dict:
        try:
            with self.__connection__() as connection:
                cursor = connection.cursor()
                hashed_password = bcrypt.hashpw(data["password"].encode("utf-8") , self.salt)

                cursor.execute(f"""INSERT INTO 'users' (name , cnic , password) VALUES (? , ? , ?)""" , (data["name"] , data["cnic"] , hashed_password))
                

                cursor.execute(f"""SELECT * FROM 'users' WHERE cnic = {data['cnic']}""")
                user_data = cursor.fetchone()
                connection.commit()
                return User(id=user_data[0] , name=user_data[1] , cnic=user_data[2] , password=user_data[3] , national_vote=user_data[4] , provincial_vote=user_data[5] , session_key=user_data[6] , session_start_time=user_data[7] , )
        except Exception as e:
            return None
        
    def __login__(self , data: dict) -> User | None:
        try:
            with self.__connection__() as connection:
                cursor = connection.cursor()
                
                cursor.execute(f"""SELECT * FROM 'users' WHERE cnic={data['cnic']}""")
                user_data = cursor.fetchone()
                connection.commit()

                if user_data and bcrypt.checkpw(data["password"].encode("utf-8") , user_data[3]):
                    session_key = self.__generate_session_key__()
                    current_timestamp = round(datetime.datetime.now().timestamp())

                    cursor.execute("""
                        UPDATE users
                        SET session_key = ?, session_start_time = ?
                        WHERE cnic = ?
                    """, (session_key, current_timestamp, data['cnic']))

                    cursor.execute(f"""SELECT * FROM 'users' WHERE cnic={data['cnic']}""")
                    user_data = cursor.fetchone()
                    return User(id=user_data[0] , name=user_data[1] , cnic=user_data[2] , password=user_data[3] , national_vote=user_data[4] , provincial_vote=user_data[5] , session_key=user_data[6] , session_start_time=user_data[7])
                else:
                    return None

        except Exception as e:
            print(e)
            return None
        
    def __generate_session_key__(self , length: int = 32) -> str:
        alphabet = string.ascii_letters + string.digits
        session_key = ''.join(secrets.choice(alphabet) for _ in range(length))
        return session_key
        
    def __get_all_candidates__(self) -> list[Candidate]:
        list_of_candidates = []

        with self.__connection__() as connection:
            cursor = connection.cursor()

            cursor.execute(f"""SELECT * FROM 'candidates'""")
            all_candidates = cursor.fetchall()

            for each_candidate in all_candidates:
                list_of_candidates.append(
                    {"id":each_candidate[0] ,"image": each_candidate[1] ,"name": each_candidate[2] ,"party": each_candidate[3] ,"poll_id": each_candidate[4]}
                )
                
        return list_of_candidates
    
    def __get_one_candidate__(self , poll_id) -> Candidate:
        with self.__connection__() as connection:
            cursor = connection.cursor()

            cursor.execute(f"""SELECT * FROM 'candidates' WHERE poll_id = ?""" , (poll_id,))
            user_details = cursor.fetchone()
            
            return Candidate(user_details[0] , user_details[1] , user_details[2] , user_details[3] , user_details[4])


    
    def __post_vote__(self , cnic: str , password: str , poll_id: int) -> User | None:
        with self.__connection__() as connection:
            cursor = connection.cursor()


            cursor.execute("""UPDATE users SET national_vote = ? , provincial_vote = ? WHERE cnic = ?""" , (poll_id , poll_id , cnic))
            
        data = {
            "cnic": cnic,
            "password": password
        }
        user = self.__login__(data=data)
        
        return user


