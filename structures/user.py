class User:
    def __init__(self , id , name , cnic , password , national_vote , provincial_vote , session_key , session_start_time) -> None:
        self.id = id
        self.name = name
        self.cnic = cnic
        self.password = password
        self.national_vote = national_vote
        self.provincial_vote = provincial_vote
        self.session_key = session_key
        self.session_start_time = session_start_time