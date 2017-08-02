import sqlite3
import Tkinter
import tkMessageBox


class App:
    def __init__(self, master):
        self.word = Tkinter.Button(text="Translate",
                                   command=lambda: self.
                                   get_name('translation.db', raw_input(
                                    "English word: ")))
        self.word.pack(side=Tkinter.LEFT)
        self.button = Tkinter.Button(text="QUIT", fg="red",
                                     command=quit)
        self.button.pack(side=Tkinter.LEFT)

    def get_name(self, database_file, word_eng):
        self.database_file = database_file
        self.word_eng = word_eng
        query = "SELECT english || ' ' || spanish FROM Translation \
        WHERE english=?;"

        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()
        cursor.execute(query, [word_eng])
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        tkMessageBox.showinfo("translation: ", results)


root = Tkinter.Tk()
app = App(root)
root.mainloop()
