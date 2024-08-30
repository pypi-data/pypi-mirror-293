import ctypes
import os
from moapy.auto_convert import auto_schema
from moapy.data_pre import SteelDBaseMaterial, SteelDBaseSection, MemberForce
from moapy.data_post import TextReport

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

def read_txt_file(file_path):
    """
    주어진 텍스트 파일(.txt)의 경로를 읽어 파일 내용을 문자열로 반환합니다.

    Args:
    file_path (str): 텍스트 파일의 경로

    Returns:
    str: 파일의 내용

    Raises:
    FileNotFoundError: 파일이 존재하지 않는 경우
    IOError: 파일을 읽는 동안 오류가 발생한 경우
    """
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    file_path = file_path + ".txt"
        
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
def report_steel_bc(matl: SteelDBaseMaterial, sect: SteelDBaseSection, load: MemberForce) -> TextReport:
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
    contents = read_txt_file(result)
    return TextReport(text=contents)

