from datasets import NMvW
from results import Result
from engines.TypicalityEnginev0 import TypicalityEngine


NMvW.data = NMvW.data.iloc[:100]

import os

# os.chdir("/home/valentin.vogelmann")
os.chdir("precomputed/")

TypicalityEngine.create_and_save(NMvW, 
                                 cached=True,
                                 id_="TypicalityEnginev0",
                                 name="TypicalityEngine/v0",
                                 params=[]
                                )
