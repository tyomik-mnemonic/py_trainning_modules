from abc import ABC
import copy
import os
from typing import Dict, List

class AbcEditedXml(ABC):
    def fill(self):
        pass
    def generate(self):
        pass

class AbcXMLFabric(ABC):
    def make_xmlobj():
        pass

class ObjTypeXml(AbcEditedXml):
    
    def __init__(self, tasked_tags:Dict[str,str]):
        self.pattern = f"""
                    <root>
                        <var name="id" value=""/>
                        <var name="level" value=""/>
                        <objects>
                        </objects>
                    </root>"""
        self.tasked_tags = tasked_tags
     
    def fill(self) -> str:
        self.result = copy.deepcopy(self.pattern)
        for t,f in self.tasked_tags.items():
            self.result = self.result.replace(t,f)
        self.result = self.result.replace('\n','')
        return self.result
    
    def generate(self) -> None:
        path = os.path.join(os.getcwd(),dir_name)
        self.dir_name = path
        os.mkdir(path)
        for i in range(self.shape[1]):
            with open(os.path.join(path,'_'+str(i)+'.xml'),'w') as f:
                f.write(self.fill())
        return None

  
class ObjTypeXmlFabric(AbcXMLFabric): 
    def make_xmlobj() -> ObjTypeXml:
        return ObjTypeXml({
            'id" value="':f'id" value="{Randomizer.randomstr()}',
            'level" value="':f'level" value="{Randomizer.randomint(100)}',
            '<objects>':f'<objects>{Randomizer.random_tag("object",Randomizer.randomint(10))}'
            }

        )
