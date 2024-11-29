from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.popup import Popup
import sqlite3


Window.size = (360, 640)


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('voting.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (name TEXT, cnic TEXT PRIMARY KEY, password TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS candidates
                               (id INTEGER PRIMARY KEY, name TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS votes
                               (candidate_id INTEGER, FOREIGN KEY(candidate_id) REFERENCES candidates(id))''')
        self.conn.commit()

    def check_user(self, cnic, password):
        self.cursor.execute("SELECT * FROM users WHERE cnic = ? AND password = ?", (cnic, password))
        return self.cursor.fetchone()

    def add_user(self, name, cnic, password):
        self.cursor.execute("INSERT INTO users (name, cnic, password) VALUES (?, ?, ?)", (name, cnic, password))
        self.conn.commit()

    def get_candidates(self):
        self.cursor.execute("SELECT * FROM candidates")
        return self.cursor.fetchall()

    def add_candidate(self, name):
        self.cursor.execute("INSERT INTO candidates (name) VALUES (?)", (name,))
        self.conn.commit()

    def vote_for_candidate(self, candidate_id):
        self.cursor.execute("INSERT INTO votes (candidate_id) VALUES (?)", (candidate_id,))
        self.conn.commit()

    def get_results(self):
        self.cursor.execute('''SELECT candidates.name, COUNT(votes.candidate_id) AS votes
                               FROM candidates LEFT JOIN votes
                               ON candidates.id = votes.candidate_id
                               GROUP BY candidates.id''')
        return self.cursor.fetchall()


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        layout.add_widget(Label(text="Login", font_size=dp(30), color=(1, 1, 1, 1)))

        self.cnic_input = TextInput(hint_text="CNIC", size_hint=(1, None), height=dp(40))
        layout.add_widget(self.cnic_input)

        self.password_input = TextInput(hint_text="Password", password=True, size_hint=(1, None), height=dp(40))
        layout.add_widget(self.password_input)

        login_button = Button(text="Login", size_hint=(1, None), height=dp(40), background_color=(0.1, 0.5, 0.7, 1))
        login_button.bind(on_release=self.login)
        layout.add_widget(login_button)

        signup_button = Button(
            text="Sign Up", size_hint=(1, None), height=dp(40), background_color=(0.1, 0.5, 0.7, 1)
        )
        signup_button.bind(on_release=lambda x: App.get_running_app().change_screen('signup'))
        layout.add_widget(signup_button)

        self.add_widget(layout)

    def login(self, instance):
        cnic = self.cnic_input.text
        password = self.password_input.text
        if not cnic or not password:
            self.show_popup("Error", "Enter both details.")
            return
        if db.check_user(cnic, password):
            App.get_running_app().change_screen('voting')
        else:
            self.show_popup("Error", "Invalid CNIC or password.")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.3))
        popup.open()


class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        layout.add_widget(Label(text="Sign Up", font_size=dp(30), color=(1, 1, 1, 1)))

        self.name_input = TextInput(hint_text="Name", size_hint=(1, None), height=dp(40))
        layout.add_widget(self.name_input)

        self.cnic_input = TextInput(hint_text="CNIC", size_hint=(1, None), height=dp(40))
        layout.add_widget(self.cnic_input)

        self.password_input = TextInput(hint_text="Password", password=True, size_hint=(1, None), height=dp(40))
        layout.add_widget(self.password_input)

        self.confirm_password_input = TextInput(
            hint_text="Confirm Password", password=True, size_hint=(1, None), height=dp(40)
        )
        layout.add_widget(self.confirm_password_input)

        signup_button = Button(text="Sign Up", size_hint=(1, None), height=dp(40), background_color=(0.1, 0.5, 0.7, 1))
        signup_button.bind(on_release=self.signup)
        layout.add_widget(signup_button)

        self.add_widget(layout)

    def signup(self, instance):
        name = self.name_input.text
        cnic = self.cnic_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text
        if not name or not cnic or not password or not confirm_password:
            self.show_popup("Error", "Please fill in all fields.")
            return
        if password != confirm_password:
            self.show_popup("Error", "Passwords do not match.")
            return
        if db.check_user(cnic, password):
            self.show_popup("Error", "CNIC already exists.")
            return
        db.add_user(name, cnic, password)
        App.get_running_app().change_screen('login')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.3))
        popup.open()


class VotingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        layout.add_widget(Label(text="Voting", font_size=dp(30), color=(1, 1, 1, 1)))

        self.candidate_buttons = []
        candidates = db.get_candidates()
        for candidate in candidates:
            button = Button(
                text=candidate[1], size_hint=(1, None), height=dp(40), background_color=(0.1, 0.5, 0.7, 1)
            )
            button.bind(on_release=lambda btn, candidate_id=candidate[0]: self.vote(candidate_id))
            self.candidate_buttons.append(button)
            layout.add_widget(button)

        results_button = Button(
            text="View Results", size_hint=(1, None), height=dp(40), background_color=(0.1, 0.5, 0.7, 1)
        )
        results_button.bind(on_release=lambda x: App.get_running_app().change_screen('results'))
        layout.add_widget(results_button)

        self.add_widget(layout)

    def vote(self, candidate_id):
        db.vote_for_candidate(candidate_id)
        self.show_popup("Success", "Vote cast successfully!")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.3))
        popup.open()


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        layout.add_widget(Label(text="Voting Results", font_size=dp(30), color=(1, 1, 1, 1)))

        results = db.get_results()
        for result in results:
            layout.add_widget(Label(text=f"{result[0]}: {result[1]} votes", font_size=dp(20), color=(1, 1, 1, 1)))

        back_button = Button(
            text="Back to Voting", size_hint=(1, None), height=dp(40), background_color=(0.1, 0.5, 0.7, 1)
        )
        back_button.bind(on_release=lambda x: App.get_running_app().change_screen('voting'))
        layout.add_widget(back_button)

        self.add_widget(layout)


class MainApp(App):
    def build(self):
        global db
        db = Database()

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(VotingScreen(name='voting'))
        sm.add_widget(ResultScreen(name='results'))
        return sm

    def change_screen(self, screen_name):
        self.root.current = screen_name


if __name__ == '__main__':
    MainApp().run()
