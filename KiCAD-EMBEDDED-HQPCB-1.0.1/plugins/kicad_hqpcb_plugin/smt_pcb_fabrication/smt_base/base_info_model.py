from dataclasses import dataclass

@dataclass
class BaseInfo:
    
    single_or_double_technique: str
    pcb_ban_height: str  # GetPcbLength
    pcb_ban_width: str  # GetPcbWidth
     
    pcb_width: str = ""   # pcb单片宽
    pcb_height: str = ""   # pcb单片长
    
    application_sphere: int = 1
    is_pcb_soft_board: str = 0
    single_or_double_technique: str
    custom_pcb_ban: str = 1
    bom_purchase: str = 1
    number: str = 5
    

    

@dataclass
class BaseInfoModel:
    
    application_sphere: int
    is_pcb_soft_board: str
    single_or_double_technique: str
    custom_pcb_ban: str 
    bom_purchase: str 
    number: str
    
    pcb_ban_height: str  # GetPcbLength
    pcb_ban_width: str  # GetPcbWidth
     
    pcb_width: str = ""   # pcb单片宽
    pcb_height: str = ""   # pcb单片长
    


        
