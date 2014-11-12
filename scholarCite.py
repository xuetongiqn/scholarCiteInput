#coding=utf-8

import sys,math,os,re,json
import web
import sqlite3

reload(sys)
sys.setdefaultencoding('utf8')

from Cheetah.Template import Template

sys.path.append('config')
sys.path.append('templates')
import scholarCiteConfig as config

urls = (
    '/', 'Index',
    '/list/(\d+)?', 'ListPage',
    '/item/(\d+)?', 'ItemPage',
    '/submit/set_cite', 'UpdateCites',
    '/html_data/(.*)', 'ShowCiteData',
    '/goto/(.*)', 'GotoPage'
)

class NextBook(object):
    """docstring for NextBook"""
    def __init__(self, bookId):
        super(NextBook, self).__init__()
        self.bookId = bookId
    def getId(self):
        SQL = "SELECT id FROM selected_books WHERE cite is NULL AND id > %s ORDER BY id LIMIT 1"%self.bookId
        conn = sqlite3.connect(config.database)
        line = conn.execute(SQL).fetchone()

        conn.close()

        return line[0]


class CiteDetail(object):
    """docstring for CiteDetail"""
    def __init__(self, ISBN, catelog):
        super(CiteDetail, self).__init__()
        self.ISBN = ISBN
        self.catelog = catelog
    
    def _file_path(self):
        groups = ('B83', 'C95', 'F0', 'F1', 'F2', 'F4', 'F7', 'F8', 'G', 'K', 'J', 'O6', 'TB', 'TH', 'TN', 'TP', 'TQ', 'TS', 'TU-8', 'TU98')
        for s in groups:
            if self.catelog.find(s) == 0:
                if s in ["G","K"]:
                    s = "G_K"
                elif s in ["TB","TH"]:
                    s = "TB_TH"

                return s + "/%s.html"%self.ISBN
        return False

    def get(self):
        path = self._file_path()

        return {
            "filePath" : path
        }



class ItemDetail(object):
    """docstring for ItemDetail"""
    def __init__(self, itemId):
        super(ItemDetail, self).__init__()
        self.itemId = itemId
    
    def get(self):
        SQL = "SELECT * FROM selected_books WHERE ID = '%s'"%self.itemId
        conn = sqlite3.connect(config.database)
        line = conn.execute(SQL).fetchone()

        conn.close()

        return {
            "book_info" : line,
            "isbn" : line[1],
            "catelog" : line[5]
        }
    def update(self, updateStr):
        SQL = "UPDATE selected_books SET %s WHERE id = %s"%(updateStr, self.itemId);
        conn = sqlite3.connect(config.database)
        cursor = conn.execute(SQL)
        conn.commit()
        return conn.total_changes
        conn.close()


class ItemList(object):
    """docstring for ItemList"""
    def __init__(self, page, which):
        super(ItemList, self).__init__()
        self.page = int(page)
        if self.page < 1 : self.page = 1
        if which == "unsigned":
            self.where = ' WHERE cite is NULL '
        elif which == "signed":
            self.where = ' WHERE cite is not NULL '
        else:
            self.where = ' '

    def _book_query(self):
        # book_query = "SELECT * FROM selected_books ORDER BY id LIMIT %d OFFSET %d"
        book_query = "SELECT * FROM selected_books %s ORDER BY id LIMIT %d OFFSET %d"
            
        offset = config.items_per_page * (self.page-1)
        return (book_query % (self.where, config.items_per_page, offset))


    def get(self):
        SQL = self._book_query()
        conn = sqlite3.connect(config.database)
        cursor = conn.execute(SQL)

        bookCount = conn.execute("SELECT count(*) FROM selected_books %s"%self.where).fetchone()[0]

        books = []
        for i, line in enumerate(cursor):
            books.append(line)

        conn.close()

        nextPage = prevPage = False
        totalPage = int(math.ceil(float(bookCount)/config.items_per_page))

        if(self.page > 1):
            prevPage = self.page-1

        if(self.page < totalPage):
            nextPage = self.page+1

        return {
            "book_list" : books,
            "curr_page" : self.page,
            "next_page" : nextPage,
            "prev_page" : prevPage,
            "total" : bookCount,
            "total_page" : totalPage
        }
        


################
# page handlers
################

class Index:
    def GET(self):
        # return "Hello, world!"
        t = web.input().get('type',"")
        # return t
        web.found('/list/1?type=%s'%t)

class ListPage:
    def GET(self, page):
        if not page: page = 1

        t = web.input().get('type',"")

        # return 'list page ' + page
        items = ItemList(page, t)
        data = items.get()
        data["type"] = t
        #return data
        # web.render('books_list.tpl.html', data)
        return Template(file = config.template_dir + 'books_list.tmpl', searchList = data)



class ItemPage:
    def GET(self, itemId):
        # return 'item id is ' + itemId

        item = ItemDetail(itemId)
        data = item.get()

        cite = CiteDetail(data['isbn'], data['catelog'])
        citeInfo = cite.get()

        data['cite_file'] = citeInfo['filePath']

        return Template(file=config.template_dir + 'book_detail.tmpl', searchList = data)


class ShowCiteData:
    def GET(self, path):
        fullPath = config.html_path+path

        if os.path.isfile(fullPath):
            html = open(fullPath).read()
            html = re.sub(r'\n','',html)
            html = re.sub(r'<script>.*?</script>','',html)
            html = html + "<script src='/static/google_page.js'></script>"

            return html
        else:
            return "no such file: %s" % fullPath

class GotoPage:
    def GET(self, s):
        if s == 'next':
            bookId = int(web.input().get('id',""))
            newId = NextBook(bookId).getId()
            web.redirect('/item/%s'%newId)



class UpdateCites:
    def POST(self):
        data = web.input()
        bookId = int(data.get('id',''))
        citeNum = int(data.get('num',0))

        book = ItemDetail(bookId)
        result = book.update('cite = %d'%citeNum)

        return json.dumps({"change":result})






if __name__ == "__main__":
    app = web.application(urls, globals(), autoreload=True)
    app.run()






