from requests import request
from bs4 import BeautifulSoup
import smtplib

novi_zg_istok = 'http://www.njuskalo.hr/prodaja-stanova/zagreb?locationId=1254&page='
novi_zg_zapad = 'http://www.njuskalo.hr/prodaja-stanova/zagreb?locationId=1255&page='

base = 'http://www.njuskalo.hr'
kvartovi = [novi_zg_istok, novi_zg_zapad]
regex = ['nekret', 'd.o.o', 'Nekretn', 'trgovina', 'Trgovina','agencija','Agencija','investitor','Investitor']



class FileHandler(object):
    def __init__(self, filename):
        self.filename = filename
        f = open(self.filename, 'r')
        self.visited = [i.strip() for i in f.readlines()]
        f.close()
    def getVisisted(self):
        return self.visited
    def returnNotVisited(self, list_to_check):
        not_visited = [new.strip() for new in list_to_check if new not in self.visited]
        return not_visited
    def writeNew(self, ids_to_add):
        f = open(self.filename, 'a')
        for i in ids_to_add:
            f.write(i+'\n')
        f.close()


class Scrapper(object):
    def __init__(self, lista_kvartova, how_deep):
        self.kvartovi = lista_kvartova
        self.depth = int(how_deep)
    def getLinksForBLocks(self, visited_ids):
        l_to_search = []
        for kvart in self.kvartovi:
            for i in range(1, self.depth + 1):
                body = BeautifulSoup(request('get', kvart + str(i)).text, 'lxml')
                links = body.findAll('h3', attrs={'class': 'entity-title'})
                for link in links:
                    rellink = link.a['href']
                    if 'nekretnine' in rellink:
                        nekretnina = base + link.a['href']
                        id = nekretnina.split('-')[-1]
                        if id not in visited_ids:
                            l_to_search.append(base + link.a['href'])
        self.unrefinedList = l_to_search
        return self.unrefinedList

    def removeFirms(self, fileHandler):
        non_firms = []
        non_firm_ids = []
        className = "Profile-username link"
        for nekretnina in self.unrefinedList:
            tmp = BeautifulSoup(request('get', nekretnina).text, 'lxml')
            a = tmp.find('a', attrs={'class': className})
            if 'korisnik' in a['href']:
                # print a['href']
                # print nekretnina
                # print 'Written to file id: %s' % nekretnina.split('-')[-1]
                non_firms.append(nekretnina)
                non_firm_ids.append(nekretnina.split('-')[-1])

        fileHandler.writeNew(non_firm_ids)
        return non_firms


class Mailer(object):
    def __init__(self, stanovi_list):
        self.stanovi = stanovi_list
    def sendMail(self):
        fromaddr = 'sasa17031981@gmail.com'
        toaddrs = 'danijelabokarica@gmail.com'
        username = 'sasa17031981@gmail.com'
        password = 'Setokaiba17'
        #msg = self.stanovi
        msg = """
            %s
        """ % self.stanovi
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        #server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()

ff = FileHandler('add_data.txt')
vIds = ff.getVisisted()
a = Scrapper(kvartovi, 10)
raw_links = a.getLinksForBLocks(vIds)
print 'raw links => %d' % len(raw_links)
lista = a.removeFirms(ff)
m = Mailer(lista)
m.sendMail()