from src.datasets import NMvW
from src.results import Result
from src.engines.TypicalityEnginev0 import TypicalityEngine


# NMvW.data = NMvW.data.iloc[:10000]

import os

# os.chdir("/home/valentin.vogelmann")
os.chdir("/data/")

TypicalityEngine.create_and_save(NMvW, 
                                 cached=True,
                                 id_="TypicalityEnginev0",
                                 name="TypicalityEngine/v0",
                                 params=[]
                                )
