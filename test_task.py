from abc import ABC
import string
import random
import os, shutil, glob, zipfile
from multiprocessing import Process
import csv
from xml.etree import ElementTree as xmlet


class Randomizer:
    def randomstr():
        return ''.join(random.choice(string.ascii_letters) for i in range(8))
    def randomint(r:int):
        return random.randrange (1,r,1)
    def random_tag(t:str,r:int):

        return '\n'.join(f"""<{t} name="{Randomizer.randomstr()}"/>""" for i in range(r))

    
class AbcZiper(ABC):
    def __init__(self, shape:tuple):
        self.shape = tuple
        

class XMLZiper(AbcZiper):
    def __init__(self, shape:tuple):
        super().__init__(shape=shape)
        self.shape = shape
    
    #Работа с xml так и не нашла себе места в структуре программы.
    #TODO: вырвать метод fill из Ziper в отдельный соответствующий класс 
    #      ObjTypeXml из соответствующей фабрики модуля xmlutils
    @staticmethod
    def unzip_it(path:str, f:str):
        try:

            with zipfile.ZipFile(os.path.join(path,f), 'r') as unzip:
                t_dir = f.replace('.','')
                os.mkdir(f.replace('.',''))
                unzip.extractall(os.path.join(path,t_dir))

        except Exception as ex:
            print('unziping was failed: '+str(ex))
    
    def fill(self):
        result = f"""
        <root>
        <var name="id" value="{Randomizer.randomstr()}"/>
        <var name="level" value="{Randomizer.randomint(100)}"/>
        <objects>
            {Randomizer.random_tag("object",Randomizer.randomint(10))}
        </objects>
        </root>""".replace("\n","")
        return result
    
    def generate(self, dir_name:str):
        
        path = os.path.join(os.getcwd(),dir_name)
        self.dir_name = path
        os.mkdir(path)
        for i in range(self.shape[1]):
            with open(os.path.join(path,'_'+str(i)+'.xml'),'w') as f:
                f.write(self.fill())
        return None
    
    def rm_generated(self):
        shutil.rmtree(self.dir_name)
        return None
    
    def to_zip(self):
        for i in range(self.shape[0]):
            self.generate('temp')
            files = glob.glob(f"{self.dir_name}/*.xml")
            with zipfile.ZipFile(f"{Randomizer.randomstr()}{str(i)}.zip", mode="w") as archive:
                for f in files:
                    #print(f)
                    archive.write(f, os.path.basename(f))
            self.rm_generated()
        return None
    

class DataFile:
    
    def __init__(self, columns:list):
        self.columns = columns
    
    def make_file(self, file_name:str, encoding='utf-8'):
        with open(file_name,'w',encoding=encoding) as csvfile:
            csvfile_writer = csv.writer(csvfile)
            csvfile_writer.writerow(self.columns)

            
#TODO:собрать "свободные" методы в соответствующий класс трансформирующий xml->csv
def parse_docs(file:str, tag:str, task:str):
    print("FILEEE ", file+"\n"+"FILEEE")
    root = xmlet.parse(file).getroot()
    
    x = root.findall(tag)
    result = []
    for i in x:
        result.append(i.get(task))
    return result

def parse_objs(file:str, tags:list, tasks:list):
    root = xmlet.parse(file).getroot()
    pk = root.findall(tags[0])[0].get(tasks[0])
    objs = root.findall(tags[1])[0].findall(tags[2])
   
    result = []
    for i in objs:
        result.append([pk, i.get(tasks[1])])
    return result

def local_parse(f:str, writed_objs:list):
    #TODO: пересмотреть положение вызова распаковки и мб перенести на более низкий ур-нь
    XMLZiper.unzip_it(os.getcwd(), f)
    f = glob.glob(f"{os.path.join(os.getcwd(), f.replace('.',''))}/*.xml")
    for i in f:
        docs = parse_docs(i, 'var','value')
        objs = parse_objs(i, ['var','objects', 'object'],['value','name'])
        writed_objs[0].writerow(docs)
        for o in objs:
            writed_objs[1].writerow(o)
            print(o)
            
    return None


def parse(encoding='utf-8'):
    
    data= XMLZiper((50,100))
    data.to_zip()

    DataFile(['id','level']).make_file('docs.csv')
    DataFile(['id','object']).make_file('objs.csv')
    
    zips = glob.glob(f"{os.getcwd()}/*.zip")
    mid = zips.__len__()//2
    
    def firstpart(iter_files_obj=zips[:mid]):
        docsfile=open('docs.csv','a+',encoding=encoding)
        docsfile_writer = csv.writer(docsfile)

        objsfile=open('objs.csv','a+',encoding=encoding)
        objsfile_writer = csv.writer(objsfile)
        
        for i in iter_files_obj:
            local_parse(i,[docsfile_writer,objsfile_writer])
        return None

    def scndpart(iter_files_obj=zips[mid:]):
        docsfile=open('docs.csv','a+',encoding=encoding)
        docsfile_writer = csv.writer(docsfile)

        objsfile=open('objs.csv','a+',encoding=encoding)
        objsfile_writer = csv.writer(objsfile)
        
        for i in iter_files_obj:
            local_parse(i,[docsfile_writer,objsfile_writer])
        return None
    
    #В н.в. потоки используются неявно
    #TODO: сделать потоки явными, вывести на верхний уровень
    process1 = Process(target=firstpart)
    process2 = Process(target=scndpart)
    process1.start()
    process2.start()          



if __name__ == "__main__":
    parse()
