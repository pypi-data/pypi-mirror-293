import ctypes
import os
import pypandoc
from pydantic import Field as dataclass_field
from moapy.auto_convert import auto_schema, MBaseModel

class SteelDBaseSection(MBaseModel):
    """
    Steel DB Section
    """
    shape: str = dataclass_field(default='H', description="Shape")
    name: str = dataclass_field(default='H 400x200x8/13', description="Section Name")

    class Config(MBaseModel.Config):
        title = "Steel DB Section"
        description = "Steel DB Section"

class SteelDBaseMaterial(MBaseModel):
    """
    Steel DB Material
    """
    code: str = dataclass_field(default='KS18(S)', description="Material Code")
    name: str = dataclass_field(default='SS275', description="Material Name")

    class Config(MBaseModel.Config):
        title = "Steel DB Material"
        description = "Steel DB Material"

class MemberForce(MBaseModel):
    """Force class

    Args:
        Nz (float): Axial force
        Mx (float): Moment about x-axis
        My (float): Moment about y-axis
        Vx (float): Shear about x-axis
        Vy (float): Shear about y-axis
    """
    Nz: float = dataclass_field(default=0.0, description="Axial force")
    Mx: float = dataclass_field(default=0.0, description="Moment about x-axis")
    My: float = dataclass_field(default=0.0, description="Moment about y-axis")
    Vx: float = dataclass_field(default=0.0, description="Shear about x-axis")
    Vy: float = dataclass_field(default=0.0, description="Shear about y-axis")

    class Config(MBaseModel.Config):
        title = "Member Force"
        description = "Member Force"

@auto_schema
def calc_steel_bc(matl: SteelDBaseMaterial, sect: SteelDBaseSection, load: MemberForce):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, 'dll', 'dgn_api.dll')

    # DLL 파일 로드
    dll = ctypes.CDLL(dll_path)

    # JSON 데이터를 변환
    matl_json = matl.json()
    sect_json = sect.json()
    load_json = load.json()

    # process_data 함수 정의 및 호출
    dll.Calc_Steel.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    dll.Calc_Steel.restype = ctypes.c_char_p

    # JSON 데이터를 인코딩해서 전달
    result = dll.Calc_Steel(matl_json.encode('utf-8'), sect_json.encode('utf-8'), load_json.encode('utf-8'))
    
    # JSON 문자열을 Python 딕셔너리로 변환
    return result

def convert_rtf_to_html(input_file):
    if isinstance(input_file, bytes):
        input_file = input_file.decode('utf-8')

    html_content = pypandoc.convert_file(input_file, 'html')
    return html_content

@auto_schema
def report_steel_bc(matl: SteelDBaseMaterial, sect: SteelDBaseSection, load: MemberForce):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, 'dll', 'dgn_api.dll')

    # DLL 파일 로드
    dll = ctypes.CDLL(dll_path)

    # JSON 데이터를 변환
    matl_json = matl.json()
    sect_json = sect.json()
    load_json = load.json()

    # process_data 함수 정의 및 호출
    dll.Report_Steel.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    dll.Report_Steel.restype = ctypes.c_char_p

    # JSON 데이터를 인코딩해서 전달
    result = dll.Report_Steel(matl_json.encode('utf-8'), sect_json.encode('utf-8'), load_json.encode('utf-8'))
    html_data = convert_rtf_to_html(result)
    return html_data

# res = report_steel_bc(matl=SteelDBaseMaterial(code='KS18(S)', name='SS275'),
#                     sect=SteelDBaseSection(shape='H', name='H 400x200x8/13'),
#                     load=MemberForce(Nz=1000.0, Mx=500.0, My=200.0, Vx=300.0, Vy=400.0))
# print(res)