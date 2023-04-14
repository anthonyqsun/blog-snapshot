import Database

from datetime import date as dt

class MarkdownParser:
    def __init__(self, database: Database.BlogDatabase):
        self.db = database


    def populate(self, filename: str) -> None:
        content = self.read(filename).split("\n")
        
        blockLines = self.findAllIndicesWithin(content, "```")
        lines = [content[i] for i in range(len(content)) if content[i]!="" or i in blockLines]
        
        dates = []

        while lines[0][0] == "(":
            dates.append(lines[0].replace("(","").replace(")","").split("/"))
            lines.pop(0)
        
        date_created = dt(int(dates[0][2]),int(dates[0][0]),int(dates[0][1]))
        i_date_created = dt.toordinal(date_created)
        s_date_created = date_created.strftime("%B %d, %Y")
        s_date_modified = dt(int(dates[-1][2]),int(dates[-1][0]),int(dates[-1][1])).strftime("%B %d, %Y")

        tags=[]
        while lines[0][0] == "@":
            tags.extend([tag[1:] for tag in lines[0].split(" ")])
            lines.pop(0)

        title = lines.pop(0)[1:].strip()
        body = self.parse(lines)
        self.db.addBlog(title, tags, i_date_created, s_date_created, s_date_modified, body)

    def parse(self, body:list[str]) -> str:
        i=0
        s=""
        while i < len(body):
            line = body[i]
            if "//" == line[:2]: # comment
                i+=1
                continue
            if "####" == line[:4]:
                s+= f"<h4>{self.formatLine(line[5:].strip())}</h4>"
            elif "###" == line[:3]:
                s+= f"<h3>{self.formatLine(line[4:].strip())}</h3>"
            elif "##" == line[:2]:
                s+= f"<h2>{self.formatLine(line[3:].strip())}</h2><hr class='subheadingrule'>"
            elif "---" == line.strip():
                s+= "<hr>"

            elif ">GH" == line[:3]:
                s+= f"<div class='flex taglist' id='gh'><img src='static/assets/github-mark.png' class='ghlogo'>{self.formatLine(line[4:])}</div>"
            elif "![" == line[:2]:
                bracket_bounds = self.findBounds(line,"[","]")
                paren_bounds = self.findBounds(line,"(",")")
                s+= f"<img class='mdimg' src='{line[paren_bounds[0]+1:paren_bounds[1]]}' alt='{line[bracket_bounds[0]+1:bracket_bounds[1]]}'><p class='caption'>{line[bracket_bounds[0]+1:bracket_bounds[1]]}</p>"

            elif "```" == line[:3]:
                s+= "<pre class='blockcode'>"
                i+=1
                while body[i][:3] != "```":
                    s+=body[i]+"<br>"
                    i+=1
                s+="</pre>"
            elif "-" == line[:1]:
                s+="<ul>"
                while body[i][0] == "-" and body[i][:3] != "---":
                    if "//" == line[:2]: # comment
                        i+=1
                        continue
                    s+=f"<li>{self.formatLine(body[i][2:].strip())}</li>"
                    i+=1

                    if i == len(body):
                        break
                i-=1
                s+="</ul>"
            elif "1." == line[:2]:
                ctr=1
                s+="<ol>"
                while body[i][:2] == str(ctr)+".":
                    if "//" == line[:2]: # comment
                        i+=1
                        continue
                    s+=f"<li>{self.formatLine(body[i][3:].strip())}</li>"
                    i+=1
                    ctr+=1

                    if i == len(body):
                        break
                i-=1
                s+="</ol>"
            else:
                s+=f"<p>{self.formatLine(line.strip())}</p>"
            i+=1
        return s

    def formatLine(self, line:str) -> str:
        if "`" in line:
            bounds = self.findBounds(line,"`","`")
            return f"{self.formatLine(line[:bounds[0]])}<span class='inlinecode'>{line[bounds[0]+1:bounds[1]]}</span>{self.formatLine(line[bounds[1]+1:])}"
        if "**" in line:
            bounds = self.findBounds(line,"**","**")
            return f"{self.formatLine(line[:bounds[0]])}<span class='bold'>{line[bounds[0]+2:bounds[1]]}</span>{self.formatLine(line[bounds[1]+2:])}"
        if "*" in line: # TODO: changed 1 to 2?
            bounds = self.findBounds(line,"*","*")
            return f"{self.formatLine(line[:bounds[0]])}<i>{line[bounds[0]+1:bounds[1]]}</i>{self.formatLine(line[bounds[1]+1:])}"
        if "[" in line and "](" in line and ")" in line:
            bracket_bounds = self.findBounds(line,"[","]")
            paren_bounds = self.findBounds(line,"(",")")
            return f"{self.formatLine(line[:bracket_bounds[0]])}<a href='{line[paren_bounds[0]+1:paren_bounds[1]]}'>{line[bracket_bounds[0]+1:bracket_bounds[1]]}</a>{self.formatLine(line[paren_bounds[1]+1:])}"
        return line
    
    def findBounds(self, line:str, symbol1:str, symbol2:str) -> list[int]:
        try:
            start = line.index(symbol1)
            end = line[start+len(symbol1):].index(symbol2)+start+len(symbol1)
        except:
            start = -1
            end = -1
        return (start,end)

    def findAllIndicesWithin(self, l: list, symbol):
        index = []
        i=0
        append = False
        while i < len(l):
            if l[i]== symbol:
                append = not append
            if append:
                index.append(i)
            i+=1
        return index


    def read(self, filename):
        with open(filename) as f:
            return f.read()