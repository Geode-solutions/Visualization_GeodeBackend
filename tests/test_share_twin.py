import os
import base64

from opengeodeweb_back import geode_objects

geode_objects_list = geode_objects.objects_list()

# ID = os.environ.get("ID")
base_route = f"/share_twin"


def test_allowed_files(client):
    response = client.get(f"{base_route}/allowed_files")
    assert response.status_code == 200
    extensions = response.json["extensions"]
    assert type(extensions) is list
    for extension in list_extensions:
        assert type(extension) == str


def test_allowed_objects(client):
    route = f"{base_route}/allowed_objects"

    # Normal test with filename 'corbi.og_brep'
    response = client.post(route, data={"filename": "corbi.og_brep"})
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    assert "BRep" in allowed_objects

    # Normal test with filename .vtu
    response = client.post(route, data={"filename": "toto.vtu"})
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    list_objects = ["HybridSolid3D", "PolyhedralSolid3D", "TetrahedralSolid3D"]
    for geode_object in list_objects:
        assert geode_object in allowed_objects

    # Test with stupid filename
    response = client.post(route, data={"filename": "toto.tutu"})
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    assert not allowed_objects

    # Test without filename
    response = client.post(route)
    assert response.status_code == 400
    description = response.json["description"]
    assert description == "No filename sent"


# def test_geographic_coordinate_systems(client):
#     route = f"{base_route}/geographic_coordinate_systems"

#     # Normal test with geode_object 'BRep'
#     response = client.post(route, data={"geode_object": "BRep"})
#     assert response.status_code == 200
#     crs_list = response.json["crs_list"]
#     assert type(crs_list) is list
#     for crs in crs_list:
#         assert type(crs) is dict

#     # Test without geode_object
#     response = client.post(route)
#     assert response.status_code == 400
#     description = response.json["description"]
#     assert description == "No geode_object sent"


# def test_output_file_extensions(client):
#     route = f"{base_route}/output_file_extensions"

#     # Normal test with geode_object
#     response = client.post(route, data={"geode_object": "BRep"})
#     assert response.status_code == 200
#     output_file_extensions = response.json["output_file_extensions"]
#     assert type(output_file_extensions) is list
#     list_output_file_extensions = ["msh", "og_brep"]
#     for output_file_extension in list_output_file_extensions:
#         assert output_file_extension in output_file_extensions

#     # Normal test with geode_object
#     response = client.post(route, data={"geode_object": "TriangulatedSurface3D"})
#     assert response.status_code == 200
#     output_file_extensions = response.json["output_file_extensions"]
#     assert type(output_file_extensions) is list
#     list_output_file_extensions = ["obj", "og_tsf3d", "stl", "vtp"]
#     for output_file_extension in list_output_file_extensions:
#         assert output_file_extension in output_file_extensions

#     # Normal test with geode_object
#     response = client.post(route, data={"geode_object": "StructuralModel"})
#     assert response.status_code == 200
#     output_file_extensions = response.json["output_file_extensions"]
#     assert type(output_file_extensions) is list
#     list_output_file_extensions = ["lso", "ml", "msh", "og_brep", "og_strm"]
#     for output_file_extension in list_output_file_extensions:
#         assert output_file_extension in output_file_extensions

#     # Test without object
#     response = client.post(route)
#     assert response.status_code == 400
#     description = response.json["description"]
#     assert description == "No geode_object sent"


# def test_convert_file(client):
#     input_crs_authority = "EPSG"
#     input_crs_code = "2000"
#     input_crs_name = "Anguilla 1957 / British West Indies Grid"
#     output_crs_authority = "EPSG"
#     output_crs_code = "3000"
#     output_crs_name = "Segara / NEIEZ"

#     for geode_object in geode_objects_list.keys():
#         if geode_object != "BRep":
#             if "crs" in geode_objects_list[geode_object]:
#                 print(f"{geode_object=}")
#                 inputs = geode_objects_list[geode_object]["input"]

#                 for input in inputs:
#                     for input_extension in input.list_creators():
#                         print(f"{input_extension=}")
#                         filename = f"corbi.{input_extension}"
#                         file = base64.b64encode(
#                             open(f"./tests/data/test.{input_extension}", "rb").read()
#                         )
#                         filesize = int(
#                             os.path.getsize(f"./tests/data/test.{input_extension}")
#                         )

#                         outputs = geode_objects_list[geode_object]["output"]

#                         for output in outputs:
#                             for output_extension in output.list_creators():
#                                 # if geode_object != 'BRep' and geode_object != 'CrossSection':
#                                 print(f"{output_extension=}")

#                                 if (
#                                     (
#                                         input_extension != "og_brep"
#                                         and geode_object != "BRep"
#                                         and output_extension != "ml"
#                                     )
#                                     and (
#                                         input_extension != "vo"
#                                         and geode_object != "RegularGrid3D"
#                                         and output_extension != "vti"
#                                     )
#                                     and (
#                                         input_extension != "shp"
#                                         and geode_object != "Section"
#                                         and output_extension != "vtm"
#                                     )
#                                     and (
#                                         input_extension != "ml"
#                                         and geode_object != "StructuralModel"
#                                         and output_extension != "lso"
#                                     )
#                                     and (
#                                         input_extension != "og_tsf2d"
#                                         and geode_object != "TriangulatedSurface2D"
#                                         and output_extension != "triangle"
#                                     )
#                                 ):
#                                     # Normal test
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 200
#                                     assert type((response.data)) is bytes
#                                     assert len((response.data)) > 0

#                                     # Test without geode_object
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "file": file,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert error_description == "No geode_object sent"

#                                     # Test without file
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert error_description == "No file sent"

#                                     # Test without filename
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert error_description == "No filename sent"

#                                     # Test without filesize
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filename": filename,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert error_description == "No filesize sent"

#                                     # Test without input_crs_authority
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert (
#                                         error_description
#                                         == "No input_crs_authority sent"
#                                     )

#                                     # Test without input_crs_code
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert error_description == "No input_crs_code sent"

#                                     # Test without input_crs_name
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert error_description == "No input_crs_name sent"

#                                     # Test without output_crs_authority
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert (
#                                         error_description
#                                         == "No output_crs_authority sent"
#                                     )

#                                     # Test without output_crs_code
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_name": output_crs_name,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert (
#                                         error_description == "No output_crs_code sent"
#                                     )

#                                     # Test without output_crs_name
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "extension": output_extension,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert (
#                                         error_description == "No output_crs_name sent"
#                                     )

#                                     # Test without extension
#                                     response = client.post(
#                                         f"{base_route}/convert_file",
#                                         data={
#                                             "geode_object": geode_object,
#                                             "file": file,
#                                             "filename": filename,
#                                             "filesize": filesize,
#                                             "input_crs_authority": input_crs_authority,
#                                             "input_crs_code": input_crs_code,
#                                             "input_crs_name": input_crs_name,
#                                             "output_crs_authority": output_crs_authority,
#                                             "output_crs_code": output_crs_code,
#                                             "output_crs_name": output_crs_name,
#                                         },
#                                     )

#                                     assert response.status_code == 400
#                                     error_description = response.json["description"]
#                                     assert error_description == "No extension sent"
