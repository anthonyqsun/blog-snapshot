import sqlite3 as sql
import util

class BlogDatabase:
    def __init__(self, name: str) -> None:
        self.name = name
        self.db = sql.connect(name, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.run("DROP TABLE IF EXISTS blogs")
        self.run("CREATE TABLE blogs ( \
                    title TEXT, \
                    tags TEXT, \
                    i_date_created INTEGER, \
                    date_created TEXT, \
                    date_modified TEXT, \
                    body TEXT \
                    );"
                )
        
    def addBlog(self, title: str, tags: list, i_created: int, s_created:str, s_modified: str, body: str):
        self.run_param("INSERT INTO blogs VALUES (?,?,?,?,?,?);", (title, ",".join(tags), i_created, s_created, s_modified, body))
        self.commit()
    
    def getTitles(self) -> list:
        titles = self.run("SELECT title FROM blogs ORDER BY i_date_created DESC").fetchall()
        return [title[0] for title in titles]
    
    def checkIfMissing(self, title: str) -> bool:
        return self.run_param("SELECT * FROM blogs WHERE title = ?",(title,)).fetchall() == []
    
    def getPost(self,title: str) -> list:
        return self.run_param("SELECT * FROM blogs WHERE title = ?",(title,)).fetchall()[0]


    def getPostFormatted(self, title: str) -> list:
        content = [a for a in self.getPost(title)]
        content[1] = [(tag, util.colorGen(tag)) for tag in content[1].split(",")]
        if content[3] != content[4]:
            content[4] = "Edited on "+content[4]
        return content
    


    def getTags(self, title: str) -> list:
        return self.getPost(title)[1].split(",")
    
    def getCreationDate(self, title: str) -> str:
        return self.getPost(title)[3]
    
    def getDirectoryPosts(self) -> list:
        return [(title, [(tag, util.colorGen(tag)) for tag in self.getTags(title)], self.getCreationDate(title)) for title in self.getTitles()]

    def commit(self) -> None:
        self.db.commit()

    def run(self, s:str) -> sql.Cursor:
        return self.cursor.execute(s)
    
    def run_param(self, s:str, params:list) -> sql.Cursor:
        return self.cursor.execute(s, params)