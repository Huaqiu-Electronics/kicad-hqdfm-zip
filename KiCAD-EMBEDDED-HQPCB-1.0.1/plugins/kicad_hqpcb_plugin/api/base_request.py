import dataclasses
import os

@dataclasses.dataclass
class BaseRequest:
    service: str = "pcb"
    region_id: str = "211"  # TODO
    country: str = "211"  # TODO
    express: str = "31"  # TODO
    sidedirection: str = '无' 
    plate_type: str = 'FR-4'
    units: str = '1'
    testpoint: str = 0
    pbnum: str = 1


    copper: str = '1'

    color: str = '绿色' 
    charcolor: str = '白色'
    cover: str = '过孔盖油'
    spray: str = '有铅喷锡'
    insidecopper: str = '0'
    impendance: str = '0' 
    bankong: str = '0' 
    blind: str = '0' 

    via_in_pad: str = '无' 
    beveledge: str = '0' 
    pressing : str = ''
    baobian: str = '0' 
    test: str = 'Sample Test Free' 
    shipment_report: str = '0' 
    slice_report: str = '0' 
    report_type: str = '0' 
    review_file: str = 0 
    has_period: str = '2' 

    film_report: str = '0' 
    pcb_note: str = '' 
    cross_board: str = 1 
    paper: str = 1 
    user_stamp: str = 1 
    hq_pack: str = 1 
    
    bcount: str = '5' 


    # type: str = 'pcbfile'
    # blayer: str = '2' 
    # blength: str = '16.04' 
    # bwidth: str = '9.94' 
    # lineweight: str = '8'
    # vias: str = '0.3' 
    # bheight: str = '1.6'


@dataclasses.dataclass
class SmtBaseRequest:
    solder_paste_type: str = 0
    is_assembly_weld: str = 0
    is_layout_cleaning: str = 0
    is_material_baking: str = 0
    is_welding_wire: str = 0
    is_test: str = 0
    is_assemble: str = 0
    is_program_burning: str = 0
    need_split: str  = 0      # 拆板出货
    is_increase_tinning: str = 0
    need_conformal_coating: str  = 0  # 刷三防漆
    is_first_confirm: str = 0
    packing_type: str  = 0
    
    postscript: str = ""
    test_duration: str =""
    x_ray_unit_number: str = 1
    x_ray_number: str = 1



@dataclasses.dataclass
class SmtRequest:
    add_plat_form: str = 5
    patch_file_name: str = ""
    bom_file_name: str = ""
    pcb_file_name: str = ""

    solder_paste_type: str = 0
    is_assembly_weld: str = 0
    is_layout_cleaning: str = 0
    is_material_baking: str = 0
    is_welding_wire: str = 0
    is_test: str = 0
    is_assemble: str = 0
    is_program_burning: str = 0
    need_split: str  = 0      # 拆板出货
    is_increase_tinning: str = 0
    need_conformal_coating: str  = 0  # 刷三防漆
    is_first_confirm: str = 0
    packing_type: str  = 0
    
    postscript: str = ""
    test_duration: str =""
    x_ray_unit_number: str = 1
    x_ray_number: str = 1


    
class SmtFiles:
    patch_file: str = ""
    bom_file: str = ""
    pcb_file: str = ""
