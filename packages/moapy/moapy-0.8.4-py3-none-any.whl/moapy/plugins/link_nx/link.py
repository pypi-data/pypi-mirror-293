from moapy.engineers import MidasAPI
from moapy.wgsd.wgsd_flow import ConcreteGeometry, TendonGeometry, ConcreteGrade, InnerPolygon, OuterPolygon, Points, TendonProp
from moapy.auto_convert import auto_schema, MBaseModel
from pydantic import Field as dataclass_field

class LinkKey(MBaseModel):
    """
    LinkConc class
    """
    elemK: int = dataclass_field(default=1, description="Element Key")
    position: float = dataclass_field(default=0.0, description="Position")

    class Config(MBaseModel.Config):
        title = "LinkKey"
        description = "LinkKey class"

class LinkConc(MBaseModel):
    """
    LinkConc class
    """
    linkKey: LinkKey = dataclass_field(default=LinkKey(), description="Check Key")
    concrete_grade: ConcreteGrade = dataclass_field(default=ConcreteGrade(design_code="ACI318M-19", grade="C12"), description="Concrete Grade")

    class Config(MBaseModel.Config):
        title = "LinkConc"
        description = "LinkConc class"


@auto_schema
def calc_concrete_coordinate(inp: LinkConc):
    ElemK = inp.linkKey.elemK
    Position = inp.linkKey.position
    concrete_grade = inp.concrete_grade
    elem = MidasAPI.db_read_item('ELEM', ElemK)
    sect_key = elem['SECT']

    coordination = MidasAPI.ope_section_coord(sect_key, Position)

    innerPolygon = InnerPolygon()
    innerPolygon.points = coordination['innerPolygon'][0]['points']

    outerPolygon = OuterPolygon()
    outerPolygon.points = coordination['outerPolygon'][0]['points']

    return ConcreteGeometry(outerPolygon=outerPolygon.points, innerPolygon=innerPolygon.points, material=concrete_grade)

@auto_schema
def calc_elem_tendon_properties(linkKey: LinkKey):
    ElemK = linkKey.elemK
    position = linkKey.position
    elem = MidasAPI.db_read_item('ELEM', ElemK)
    matl_key = elem['MATL']
    tdnt = MidasAPI.db_read_item('TDNT', matl_key)
    elemtdnt = MidasAPI.ope_elem_tendon(ElemK, position)

    points = Points()
    points.points = elemtdnt['points']

    tendon_properties = TendonProp()
    tendon_properties.area = tdnt['AREA']

    return TendonGeometry(points=points, prop=tendon_properties)


# ElemK = 1
# position = 0.0
# concrete_grade = ConcreteGrade(design_code="ACI318M-19", grade="C12")

# concrete_coordinate = calc_concrete_coordinate(ElemK, position, concrete_grade)
# result_concrete_geometry = concrete_geometry(**concrete_coordinate)

# print(result_concrete_geometry)

# elem_tendon_properties = calc_elem_tendon_properties(ElemK, position)
# result_tendon_geometry = tendon_geometry(**elem_tendon_properties)
# print(result_tendon_geometry)