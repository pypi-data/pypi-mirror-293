import ctypes
import pypandoc
import os
from moapy.auto_convert import auto_schema
from moapy.data_pre import SteelDBaseMaterial, SteelDBaseSection, MemberForce, ReportType
from moapy.data_post import ResultReport

def rtf_to_html(file_path):
    # 파일 경로가 bytes로 주어진 경우 문자열로 변환
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    # 파일 경로 검증
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        # RTF 파일은 보통 ANSI(Windows-1252) 또는 기본 인코딩을 사용함
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file_content = file.read()

        # RTF를 HTML로 변환
        html_content = pypandoc.convert_text(file_content, 'html', format='rtf')
        return html_content
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")
    except Exception as e:
        raise Exception(f"Error converting RTF to HTML: {e}")

def read_txt_file(file_path):
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    # 파일 경로 검증
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        # 파일 열기 및 내용 읽기
        with open(file_path, 'r', encoding='utf-16') as file:
            file_content = file.read()
        return file_content
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")

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

@auto_schema
def report_steel_bc(matl: SteelDBaseMaterial, sect: SteelDBaseSection, load: MemberForce, rptType: ReportType) -> ResultReport:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, 'dll', 'dgn_api.dll')

    # DLL 파일 로드
    dll = ctypes.CDLL(dll_path)

    # JSON 데이터를 변환
    matl_json = matl.json()
    sect_json = sect.json()
    load_json = load.json()
    rptType_json = rptType.json()

    # process_data 함수 정의 및 호출
    dll.Report_Steel.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    dll.Report_Steel.restype = ctypes.c_char_p

    # JSON 데이터를 인코딩해서 전달
    result = dll.Report_Steel(matl_json.encode('utf-8'), sect_json.encode('utf-8'), load_json.encode('utf-8'), rptType_json.encode('utf-8'))

    report = ResultReport()
    if rptType.type == 'Text':
        report.type = 'Text'
        report.contents = read_txt_file(result)
    elif rptType.type == 'Html':
        report.type = 'Html'
        report.contents = rtf_to_html(result)

    return report

# res = report_steel_bc(matl=SteelDBaseMaterial(code='KS18(S)', name='SS275'),
#                  sect=SteelDBaseSection(shape='H', name='H 400x200x8/13'),
#                  load=MemberForce(Nz=1000.0, Mx=500.0, My=200.0, Vx=300.0, Vy=400.0), rptType=ReportType(type='Html'))

# print(res.contents)