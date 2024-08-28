import moapy.wgsd.wgsd_flow as wgsd_flow
import concreteproperties.results as res
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image
from moapy.mdreporter import ReportUtil
from moapy.wgsd.wgsd_flow import Material, Geometry, PMOptions, Lcom
from moapy.auto_convert import auto_schema, MBaseModel
from concreteproperties.concrete_section import ConcreteSection
from pydantic import Field as dataclass_field

matplotlib.use('Agg')  # Agg 백엔드 사용

class DgnCode(MBaseModel):
    """
    DgnCode
    """
    name: str = dataclass_field(default="", description="DgnCode")

    class Config:
        title = "DgnCode"

class AxialForceOpt(MBaseModel):
    """
    Moment Interaction Curve
    """
    Nx: float = dataclass_field(default=0.0, description="Axial Force")

    class Config:
        title = "Axial Force Option"

class ResultMD(MBaseModel):
    """
    Result Markdown
    """
    md: str = dataclass_field(default="", description="Markdown")

    class Config(MBaseModel.Config):
        title = "Markdown"
        widget = "Markdown"

@auto_schema
def calc_rc_mm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, axialforce: AxialForceOpt) -> res.BiaxialBendingResults:
    """
    Moment Interaction Curve
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        return comp.biaxial_bending_diagram(n=axialforce.Nx)

    return ''

def get_markdownimg_base64(scale=1.0):
    """
    Get SVG Base64 Image for Markdown with specified scale ratio.
    
    :param scale: Ratio to scale the image, default is 1.0 (no scaling)
    """
    # 이미지 버퍼에 SVG 형식으로 저장
    buffer = io.BytesIO()
    plt.savefig(buffer, format='svg')
    buffer.seek(0)

    # SVG 데이터를 문자열로 읽어오기
    svg_data = buffer.getvalue().decode('utf-8')

    # SVG 데이터를 Base64로 인코딩
    img_base64 = base64.b64encode(svg_data.encode('utf-8')).decode('utf-8')
    
    # HTML 태그로 감싸서 비율 조정
    markdown_img = f'<img src="data:image/svg+xml;base64,{img_base64}" width="{int(scale * 100)}%" />'
    return markdown_img

@auto_schema
def report_rc_mm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, axialforce: AxialForceOpt) -> ResultMD:
    """
    Report Moment Interaction Curve
    """
    rpt = ReportUtil("test.md", 'M-M Curve result')
    comp_sect = generate_defaultinfo_markdown_report(rpt, material, geometry)
    plt.clf()
    result = comp_sect.biaxial_bending_diagram(n=axialforce.Nx)
    result.plot_diagram()
    rpt.add_paragraph("Moment-Moment Interaction Curve")
    markdown_img = get_markdownimg_base64(0.6)

    rpt.add_line(markdown_img)
    return ResultMD(md=rpt.get_md_text())

class AngleOpt(MBaseModel):
    """
    Angle Option
    """
    theta: float = dataclass_field(default=0.0, description="theta")

    class Config:
        title = "Theta Option"

class ElasticModulusOpt(MBaseModel):
    """
    Elastic Modulus Option
    """
    E: float = dataclass_field(default=200.0, description="Elastic Modulus")

    class Config:
        title = "Elastic Modulus Option"

@auto_schema
def calc_rc_pm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, angle: AngleOpt):
    """
    Axial Moment Interaction Curve
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        return comp.moment_interaction_diagram(theta=angle.theta)

    return ''

@auto_schema
def report_rc_pm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, angle: AngleOpt):
    """
    Axial Moment Interaction Curve
    """
    rpt = ReportUtil("test.md", 'P-M Interaction Result')
    comp_sect = generate_defaultinfo_markdown_report(rpt, material, geometry)
    plt.clf()
    result = comp_sect.moment_interaction_diagram(theta=angle.theta)
    result.plot_diagram()
    rpt.add_paragraph("Axial-Moment Interaction Curve")
    markdown_img = get_markdownimg_base64(0.7)

    rpt.add_line(markdown_img)
    return ResultMD(md=rpt.get_md_text())

@auto_schema
def calc_rc_uls_stress(material: Material, geometry: Geometry, code: DgnCode, theta: AngleOpt, axialForce: AxialForceOpt):
    """
    reinforced concrete ultimate stress
    """
    pm = wgsd_flow.get_dgncode(code.name)
    comp = pm.calc_compound_section(material, geometry)
    if type(comp) is ConcreteSection:
        ultimate_results = comp.ultimate_bending_capacity(theta=theta.theta, n=axialForce.Nx)
        return comp.calculate_ultimate_stress(ultimate_results)

    return ''

@auto_schema
def calc_rc_uls_bending_capacity(material: Material, geometry: Geometry, code: DgnCode, theta: AngleOpt, axialForce: AxialForceOpt):
    """
    reinforced concrete ultimate bending capacity
    """
    pm = wgsd_flow.get_dgncode(code.name)
    comp = pm.calc_compound_section(material, geometry)
    if type(comp) is ConcreteSection:
        return comp.ultimate_bending_capacity(theta=theta.theta, n=axialForce.Nx)

    return ''

@auto_schema
def calc_rc_cracked_stress(material: Material, geometry: Geometry, code: DgnCode, lcom: Lcom):
    """
    reinforced concrete cracked stress

    Args:
        material: Material
        geometry: Geometry
        code: DgnCode
        lcom: Lcom

    Returns:
        res.StressResult
    """
    pm = wgsd_flow.get_dgncode(code.name)
    comp = pm.calc_compound_section(material, geometry)
    if type(comp) is ConcreteSection:
        cracked_res = comp.calculate_cracked_properties(theta=0.0)
        return comp.calculate_cracked_stress(cracked_res, n=lcom.f.Nz, m=lcom.f.Mx)

    return res.StressResult

@auto_schema
def report_rc_cracked_stress(material: Material, geometry: Geometry, code: DgnCode, lcom: Lcom) -> ResultMD:
    """
    Report Cracked Stress
    """
    rpt = ReportUtil("test.md", 'cracked stress result')
    comp_sect = generate_defaultinfo_markdown_report(rpt, material, geometry)
    cracked_res = comp_sect.calculate_cracked_properties(theta=0.0)
    result = comp_sect.calculate_cracked_stress(cracked_res, n=lcom.f.Nz, m=lcom.f.Mx)
    
    plt.clf()
    result.plot_stress()
    rpt.add_paragraph("Cracked Stress Contour")
    markdown_img = get_markdownimg_base64(0.8)
    rpt.add_line(markdown_img)
    return ResultMD(md=rpt.get_md_text())

@auto_schema
def calc_rc_cracked_properties(material: Material, geometry: Geometry):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.calculate_cracked_properties()

@auto_schema
def calc_rc_uncracked_stress(material: Material, geometry: Geometry, lcb: Lcom):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.calculate_uncracked_stress(n=lcb.f.Nz, m_x=lcb.f.Mx, m_y=lcb.f.My)

@auto_schema
def calc_rc_moment_curvature(material: Material, geometry: Geometry) -> res.MomentCurvatureResults:
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.moment_curvature_analysis()

def generate_comp_sect(material: Material, geometry: Geometry):
    sect = wgsd_flow.MSection(material, geometry)
    return sect.calc_compound_section()

def generate_markdown_table(prop, fmt: str = "8.6e") -> str:
    """Generates a markdown table for the gross concrete section properties."""
    table_md = "| Property                   | Value           |\n"
    table_md += "|----------------------------|-----------------|\n"

    rows = [
        ("Total Area", prop.total_area),
        ("Concrete Area", prop.concrete_area),
    ]

    if prop.reinf_meshed_area:
        rows.append(("Meshed Reinforcement Area", prop.reinf_meshed_area))

    rows.append(("Lumped Reinforcement Area", prop.reinf_lumped_area))

    if prop.strand_area:
        rows.append(("Strand Area", prop.strand_area))

    additional_rows = [
        ("Axial Rigidity (EA)", prop.e_a),
        ("Mass (per unit length)", prop.mass),
        ("Perimeter", prop.perimeter),
        ("E.Qx", prop.e_qx),
        ("E.Qy", prop.e_qy),
        ("x-Centroid", prop.cx),
        ("y-Centroid", prop.cy),
        ("x-Centroid (Gross)", prop.cx_gross),
        ("y-Centroid (Gross)", prop.cy_gross),
        ("E.Ixx_g", prop.e_ixx_g),
        ("E.Iyy_g", prop.e_iyy_g),
        ("E.Ixy_g", prop.e_ixy_g),
        ("E.Ixx_c", prop.e_ixx_c),
        ("E.Iyy_c", prop.e_iyy_c),
        ("E.Ixy_c", prop.e_ixy_c),
        ("E.I11", prop.e_i11),
        ("E.I22", prop.e_i22),
        ("Principal Axis Angle", prop.phi),
        ("E.Zxx+", prop.e_zxx_plus),
        ("E.Zxx-", prop.e_zxx_minus),
        ("E.Zyy+", prop.e_zyy_plus),
        ("E.Zyy-", prop.e_zyy_minus),
        ("E.Z11+", prop.e_z11_plus),
        ("E.Z11-", prop.e_z11_minus),
        ("E.Z22+", prop.e_z22_plus),
        ("E.Z22-", prop.e_z22_minus),
        ("Ultimate Concrete Strain", prop.conc_ultimate_strain),
    ]

    rows.extend(additional_rows)

    if prop.n_prestress:
        rows.append(("n_prestress", prop.n_prestress))
        rows.append(("m_prestress", prop.m_prestress))

    for property_name, value in rows:
        table_md += f"| {property_name:<26} | {value:{fmt}} |\n"

    return table_md

def generate_defaultinfo_markdown_report(rpt: ReportUtil, material: Material, geometry: Geometry):
    rpt.add_paragraph("Material")
    rpt.add_line(f" - Concrete: {material.concrete.grade.design_code} {material.concrete.grade.grade}")
    plt.plot([component.strain for component in material.concrete.curve_sls], [component.stress for component in material.concrete.curve_sls], label='SLS')
    plt.plot([component.strain for component in material.concrete.curve_uls], [component.stress for component in material.concrete.curve_uls], label='ULS')
    plt.xlabel('Strain')
    plt.ylabel('Stress')
    plt.title('Concrete Stress-Strain Curve')
    plt.legend()
    plt.show(block=False)
    markdown_img = get_markdownimg_base64(0.6)
    rpt.add_line("")
    rpt.add_line(markdown_img)

    plt.clf()
    rpt.add_line("")
    rpt.add_line(f" - Rebar: {material.rebar.grade.design_code} {material.rebar.grade.grade}")
    plt.plot([component.strain for component in material.rebar.curve_sls], [component.stress for component in material.rebar.curve_sls], label='SLS')
    plt.plot([component.strain for component in material.rebar.curve_uls], [component.stress for component in material.rebar.curve_uls], label='ULS')
    plt.xlabel('Strain')
    plt.ylabel('Stress')
    plt.title('Rebar Stress-Strain Curve')
    plt.legend()
    plt.show(block=False)
    markdown_img = get_markdownimg_base64(0.6)
    rpt.add_line("")
    rpt.add_line(markdown_img)

    plt.clf()
    comp_sect = generate_comp_sect(material, geometry)
    rpt.add_paragraph("Geometry")
    comp_sect.plot_section()
    plt.show(block=False)
    markdown_img = get_markdownimg_base64(0.7)
    rpt.add_line(markdown_img)
    gross_props = comp_sect.get_gross_properties()
    md = generate_markdown_table(prop=gross_props)
    rpt.add_line(md)
    return comp_sect

@auto_schema
def report_rc_moment_curvature(material: Material, geometry: Geometry) -> ResultMD:
    rpt = ReportUtil("test.md", 'Moment Curvature result')

    comp_sect = generate_defaultinfo_markdown_report(rpt, material, geometry)

    rpt.add_line("")
    plt.clf()
    rpt.add_paragraph("Moment-Curvature Analysis")
    mphi_res = comp_sect.moment_curvature_analysis()
    mphi_res.plot_results()
    markdown_img = get_markdownimg_base64(0.6)

    rpt.add_line(markdown_img)
    return ResultMD(md=rpt.get_md_text())

@auto_schema
def calc_extreme_bar(material: Material, geometry: Geometry, angle: AngleOpt):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.extreme_bar(theta=angle.theta)

@auto_schema
def calc_cracking_moment(material: Material, geometry: Geometry, angle: AngleOpt):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.calculate_cracking_moment(theta=angle.theta)

@auto_schema
def calc_gross_properties(material: Material, geometry: Geometry):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.get_gross_properties()

@auto_schema
def calc_transformed_gross_properties(material: Material, geometry: Geometry, m: ElasticModulusOpt):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.get_transformed_gross_properties(m.E)

# result = calc_gross_properties(material=wgsd_flow.Material(), geometry=wgsd_flow.Geometry(), angle=AngleOpt(theta=0.0))
# result = calc_transformed_gross_properties(material=wgsd_flow.Material(), geometry=wgsd_flow.Geometry(), m=ElasticModulusOpt())
# print(result)


# str = report_rc_cracked_stress(Material(), Geometry(), DgnCode(), Lcom(str='lcom', f={'Nz': 0.0, 'Mx': 100.0, 'My': 0.0}))
# inp = {
#   "material": {
#     "concrete": {
#       "grade": {
#         "design_code": "ACI318M-19",
#         "grade": "C12"
#       },
#       "curve_uls": [
#         {
#           "stress": 0,
#           "strain": 0
#         },
#         {
#           "stress": 0,
#           "strain": 0.0006
#         },
#         {
#           "stress": 34,
#           "strain": 0.0006
#         },
#         {
#           "stress": 34,
#           "strain": 0.003
#         }
#       ],
#       "curve_sls": [
#         {
#           "stress": 0,
#           "strain": 0
#         },
#         {
#           "stress": 32.8,
#           "strain": 0.001
#         }
#       ]
#     },
#     "rebar": {
#       "grade": {
#         "design_code": "ACI318M-19",
#         "grade": "Grade 420"
#       },
#       "curve_uls": [
#         {
#           "strain": 0,
#           "stress": 0
#         },
#         {
#           "strain": 0.0025,
#           "stress": 500
#         },
#         {
#           "strain": 0.05,
#           "stress": 500
#         }
#       ],
#       "curve_sls": [
#         {
#           "strain": 0,
#           "stress": 0
#         },
#         {
#           "strain": 0.0025,
#           "stress": 500
#         },
#         {
#           "strain": 0.05,
#           "stress": 500
#         }
#       ]
#     },
#     "tendon": {
#       "grade": {
#         "design_code": "ACI318M-19",
#         "grade": "Grade 420"
#       },
#       "curve_uls": [
#         {
#           "strain": 0,
#           "stress": 0
#         },
#         {
#           "strain": 0.00725,
#           "stress": 1450
#         },
#         {
#           "strain": 0.05,
#           "stress": 1750
#         }
#       ],
#       "curve_sls": [
#         {
#           "strain": 0,
#           "stress": 0
#         },
#         {
#           "strain": 0.00725,
#           "stress": 1450
#         },
#         {
#           "strain": 0.05,
#           "stress": 1750
#         }
#       ]
#     }
#   },
#   "geometry": {
#     "concrete": {
#       "outerPolygon": [
#         {
#           "x": 0,
#           "y": 0
#         },
#         {
#           "x": 400,
#           "y": 0
#         },
#         {
#           "x": 400,
#           "y": 600
#         },
#         {
#           "x": 0,
#           "y": 600
#         }
#       ],
#       "innerPolygon": [],
#       "material": {
#         "design_code": "ACI318M-19",
#         "grade": "C12"
#       }
#     },
#     "rebar": {
#       "points": [
#         {
#           "x": 40,
#           "y": 40
#         },
#         {
#           "x": 360,
#           "y": 40
#         },
#         {
#           "x": 360,
#           "y": 560
#         },
#         {
#           "x": 40,
#           "y": 560
#         }
#       ],
#       "prop": {
#         "area": 287,
#         "material": {
#           "design_code": "ACI318M-19",
#           "grade": "Grade 420"
#         }
#       }
#     },
#     "tendon": {
#       "points": [],
#       "prop": {
#         "area": 287,
#         "material": {
#           "design_code": "ACI318M-19",
#           "grade": "Grade 420"
#         },
#         "prestress": 0
#       }
#     }
#   },
#   "opt": {
#     "dgncode": "Eurocode2-04",
#     "by_ecc_pu": "ecc"
#   },
#   "axialforce": {
#     "Nx": 0
#   }
# }
# str = report_rc_mm_interaction_curve(**inp)
# str.plot_diagram()
# print(str)

# str = report_rc_cracked_stress(Material(), Geometry(), DgnCode(name='ACI318-14'), Lcom(str='lcom', f={'Nz': 0.0, 'Mx': 100.0, 'My': 0.0}))
# print(str)

# str = calc_rc_pm_interaction_curve(Material(), Geometry(), PMOptions(dgncode='ACI318-14', by_ecc_pu='ecc'), AngleOpt(theta=0.0))
# str.plot_diagram()

# result = report_rc_cracked_stress(Material(), Geometry(), DgnCode(name='ACI318-14'), Lcom(str='lcom', f={'Nz': 0.0, 'Mx': 100.0, 'My': 0.0}))
# result = report_rc_mm_interaction_curve(Material(), Geometry(), PMOptions(dgncode='ACI318-14', by_ecc_pu='ecc'), AxialForceOpt(Nx=0.0))
