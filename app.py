# program by cbh778899-https://github.com/cbh778899

from flask import *
import sqlite3
import os

id_calculator = []

class db():
    def create(self):
        global id_calculator
        conn = sqlite3.connect("clipboard.db")
        conn.cursor().execute("create table if not exists clipboard(id, content, type)")
        ids = conn.cursor().execute("select id from clipboard")
        for i in ids:
            id_calculator.append(i[0])
        conn.commit()
        conn.close()

    def getID(self):
        global id_calculator
        for i in range(len(id_calculator)):
            if id_calculator[i] == -1:
                id_calculator[i] = i
                return i
        id_calculator.append(len(id_calculator))
        return len(id_calculator) - 1

    def write(self, content, type):
        conn = sqlite3.connect("clipboard.db")
        conn.cursor().execute("insert into clipboard values(?,?,?)",(self.getID(), content, type))
        conn.commit()
        conn.close()

    def read(self):
        conn = sqlite3.connect("clipboard.db")
        result = conn.cursor().execute('select * from clipboard')
        li = []
        for r in result:
            li.append(r)
        conn.close()
        return li

    def getContentById(self, id):
        conn = sqlite3.connect("clipboard.db")
        result = conn.cursor().execute('select * from clipboard where id=%d'%(id))
        for r in result:
            result = r
            break
        return result
    
    def rm(self, id):
        conn = sqlite3.connect("clipboard.db")
        if id == None:
            conn.cursor().execute('delete from clipboard')
        else:
            col = self.getContentById(id)
            if col[2] == "file":
                os.remove(col[1])
            conn.cursor().execute('delete from clipboard where id=%d'%(id))
            global id_calculator
            id_calculator[id_calculator.index(id)] = -1
        conn.commit()
        conn.close()

db().create()

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def root():
    if request.method == 'POST':
        text_content = request.form['text']
        file_content = request.files.getlist('file[]')
        if text_content != "":
            db().write(text_content.replace("\r\n","<br>"), "text")
        if file_content:
            for f in file_content:
                if not f:
                    break
                f.save(f.filename)
                db().write(f.filename,"file")
        
    return render_template("index.html")

@app.route("/contents")
def contents():
    all_contents = db().read()
    calljs = "loadConetnt({},{})"
    content_str = "["
    for t in all_contents:
        content_str += "['{}','{}','{}'],".format(str(t[0]),t[1],t[2])
    content_str = content_str[0:-2]+"]]"
    calljs = calljs.format(len(all_contents),content_str)
    return render_template("contents.html", js = calljs)

@app.route("/remove/<id>")
def remove(id):
    db().rm(int(id))
    return redirect(url_for('contents'))

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    response = make_response(send_from_directory(os.getcwd(), filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return send_from_directory(os.getcwd(), filename, as_attachment=True)

@app.route('/clean_up')
def clean():
    db().rm(None)
    return redirect(url_for("root"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
