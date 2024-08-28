# Copyright (C) 2020-2024 Fraunhofer ITWM and Sebastian Blauth
#
# This file is part of cashocs.
#
# cashocs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cashocs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cashocs.  If not, see <https://www.gnu.org/licenses/>.

"""Mesh input and output."""

from __future__ import annotations

import configparser
import json
import pathlib
import subprocess  # nosec B404
import tempfile
import time
from typing import Dict, Optional, TYPE_CHECKING

import fenics
import h5py
import numpy as np

from cashocs import _exceptions
from cashocs import _loggers
from cashocs import _utils
from cashocs._cli._convert import convert as cli_convert
from cashocs.geometry import measure as measure_module
from cashocs.geometry import mesh as mesh_module

if TYPE_CHECKING:
    from mpi4py import MPI

    from cashocs import _typing


def import_mesh(mesh_file: str, comm: Optional[MPI.Comm] = None) -> _typing.MeshTuple:
    """Imports a mesh file for use with cashocs / FEniCS.

    This function imports a mesh file. The mesh file can either be a Gmsh mesh file
    or an xdmf mesh file that was generated by GMSH and converted to
    .xdmf with the function :py:func:`cashocs.convert`.
    If there are Physical quantities specified in the GMSH file, these are imported
    to the subdomains and boundaries output of this function and can also be directly
    accessed via the measures, e.g., with ``dx(1)``, ``ds(1)``, etc.

    Args:
        mesh_file: The location of the mesh file in .xdmf or .msh file format.
        comm: MPI communicator that is to be used for creating the mesh.

    Returns:
        A tuple (mesh, subdomains, boundaries, dx, ds, dS), where mesh is the imported
        FEM mesh, subdomains is a mesh function for the subdomains, boundaries is a mesh
        function for the boundaries, dx is a volume measure, ds is a surface measure,
        and dS is a measure for the interior facets.

    Notes:
        In case the boundaries in the Gmsh .msh file are not only marked with numbers
        (as physical groups), but also with names (i.e. strings), these strings can be
        used with the integration measures ``dx`` and ``ds`` returned by this method.
        E.g., if one specified the following in a 2D Gmsh .geo file ::

            Physical Surface("domain", 1) = {i,j,k};

        where i,j,k are representative for some integers, then this can be used in the
        measure ``dx`` (as we are 2D) as follows. The command ::

            dx(1)

        is completely equivalent to ::

           dx("domain")

        and both can be used interchangeably.

    """
    mesh_path = pathlib.Path(mesh_file)
    mesh_type = mesh_path.suffix

    if mesh_type == ".msh":
        mesh_tuple = _import_gmsh_mesh(mesh_file, comm)
    elif mesh_type == ".xdmf":
        mesh_tuple = _import_xdmf_mesh(mesh_file, comm)
    else:
        raise _exceptions.InputError(
            "cashocs.io.mesh.import_mesh",
            "mesh_file",
            "Only XDMF (.xdmf) or Gmsh (.msh) meshes are supported.",
        )

    return mesh_tuple


def _import_gmsh_mesh(
    mesh_file: str, comm: Optional[MPI.Comm] = None
) -> _typing.MeshTuple:
    """Imports a mesh file for use with cashocs / FEniCS.

    This function imports a mesh file that was generated by GMSH.
    If there are Physical quantities specified in the GMSH file, these are imported
    to the subdomains and boundaries output of this function and can also be directly
    accessed via the measures, e.g., with ``dx(1)``, ``ds(1)``, etc.

    Args:
        mesh_file: The location of the mesh file in .xdmf file format.
        comm: MPI communicator that is to be used for creating the mesh.

    Returns:
        A tuple (mesh, subdomains, boundaries, dx, ds, dS), where mesh is the imported
        FEM mesh, subdomains is a mesh function for the subdomains, boundaries is a mesh
        function for the boundaries, dx is a volume measure, ds is a surface measure,
        and dS is a measure for the interior facets.

    Notes:
        In case the boundaries in the Gmsh .msh file are not only marked with numbers
        (as physical groups), but also with names (i.e. strings), these strings can be
        used with the integration measures ``dx`` and ``ds`` returned by this method.
        E.g., if one specified the following in a 2D Gmsh .geo file ::

            Physical Surface("domain", 1) = {i,j,k};

        where i,j,k are representative for some integers, then this can be used in the
        measure ``dx`` (as we are 2D) as follows. The command ::

            dx(1)

        is completely equivalent to ::

           dx("domain")

        and both can be used interchangeably.

    """
    convert(mesh_file, quiet=True)
    mesh_filename = f"{mesh_file[:-4]}.xdmf"
    mesh_tuple = _import_xdmf_mesh(mesh_filename, comm)

    return mesh_tuple


@mesh_module._get_mesh_stats(mode="import")  # pylint:disable=protected-access
def _import_xdmf_mesh(
    mesh_file: str, comm: Optional[MPI.Comm] = None
) -> _typing.MeshTuple:
    """Imports a mesh file for use with cashocs / FEniCS.

    This function imports a mesh file that was generated by GMSH and converted to
    .xdmf with the function :py:func:`cashocs.convert`.
    If there are Physical quantities specified in the GMSH file, these are imported
    to the subdomains and boundaries output of this function and can also be directly
    accessed via the measures, e.g., with ``dx(1)``, ``ds(1)``, etc.

    Args:
        mesh_file: The location of the mesh file in .xdmf file format.
        comm: MPI communicator that is to be used for creating the mesh.

    Returns:
        A tuple (mesh, subdomains, boundaries, dx, ds, dS), where mesh is the imported
        FEM mesh, subdomains is a mesh function for the subdomains, boundaries is a mesh
        function for the boundaries, dx is a volume measure, ds is a surface measure,
        and dS is a measure for the interior facets.

    Notes:
        In case the boundaries in the Gmsh .msh file are not only marked with numbers
        (as physical groups), but also with names (i.e. strings), these strings can be
        used with the integration measures ``dx`` and ``ds`` returned by this method.
        E.g., if one specified the following in a 2D Gmsh .geo file ::

            Physical Surface("domain", 1) = {i,j,k};

        where i,j,k are representative for some integers, then this can be used in the
        measure ``dx`` (as we are 2D) as follows. The command ::

            dx(1)

        is completely equivalent to ::

           dx("domain")

        and both can be used interchangeably.

    """
    if isinstance(mesh_file, configparser.ConfigParser):
        raise _exceptions.InputError(
            "cashocs.import_mesh",
            "mesh_file",
            "Calling cashocs.import_mesh with a ConfigParser instance"
            " is not allowed anymore starting with cashocs v2.",
        )
    # Check for the file format
    file_string = mesh_file[:-5]

    if comm is None:
        comm = fenics.MPI.comm_world

    mesh = fenics.Mesh(comm)
    xdmf_file = fenics.XDMFFile(mesh.mpi_comm(), mesh_file)
    xdmf_file.read(mesh)
    xdmf_file.close()

    subdomains_mvc = fenics.MeshValueCollection(
        "size_t", mesh, mesh.geometric_dimension()
    )
    boundaries_mvc = fenics.MeshValueCollection(
        "size_t", mesh, mesh.geometric_dimension() - 1
    )

    subdomains_path = pathlib.Path(f"{file_string}_subdomains.xdmf")
    if subdomains_path.is_file():
        xdmf_subdomains = fenics.XDMFFile(mesh.mpi_comm(), str(subdomains_path))
        xdmf_subdomains.read(subdomains_mvc, "subdomains")
        xdmf_subdomains.close()

    boundaries_path = pathlib.Path(f"{file_string}_boundaries.xdmf")
    if boundaries_path.is_file():
        xdmf_boundaries = fenics.XDMFFile(mesh.mpi_comm(), str(boundaries_path))
        xdmf_boundaries.read(boundaries_mvc, "boundaries")
        xdmf_boundaries.close()

    physical_groups: Optional[Dict[str, Dict[str, int]]] = None
    physical_groups_path = pathlib.Path(f"{file_string}_physical_groups.json")
    if physical_groups_path.is_file():
        with physical_groups_path.open("r", encoding="utf-8") as file:
            physical_groups = json.load(file)

    subdomains = fenics.MeshFunction("size_t", mesh, subdomains_mvc)
    boundaries = fenics.MeshFunction("size_t", mesh, boundaries_mvc)

    dx = measure_module.NamedMeasure(
        "dx", domain=mesh, subdomain_data=subdomains, physical_groups=physical_groups
    )
    ds = measure_module.NamedMeasure(
        "ds", domain=mesh, subdomain_data=boundaries, physical_groups=physical_groups
    )
    d_interior_facet = measure_module.NamedMeasure(
        "dS", domain=mesh, subdomain_data=boundaries, physical_groups=physical_groups
    )

    # Add the physical groups to the mesh in case they are present
    if physical_groups is not None:
        mesh.physical_groups = physical_groups

    return mesh, subdomains, boundaries, dx, ds, d_interior_facet


def export_mesh(
    mesh: fenics.Mesh,
    mesh_file: str,
    subdomains: Optional[fenics.MeshFunction] = None,
    boundaries: Optional[fenics.MeshFunction] = None,
    comm: Optional[MPI.Comm] = None,
) -> None:
    """Exports a mesh (together with its subdomains and boundaries).

    This is useful so that the mesh can be reimported later on again. This is used for
    checkpointing in cashocs, but also has other use cases, e.g., storing a function
    on hard disk and later reimporting it to perform a post-processing.

    Args:
        mesh: The fenics mesh which shall be exported.
        mesh_file: Filename / path to the exported mesh. Has to end in .xdmf. Boundaries
            and subdomains will be named accordingly.
        subdomains: The subdomains meshfunction corresponding to the mesh. Optional,
            default is `None`, so that no subdomain information is used.
        boundaries: The boundaries meshfunction corresponding to the mesh. Optional,
            default is `None`, so that no boundary information is used.
        comm: The MPI communicator used. Optional, default is `None`, so that the
            `fenics.MPI.comm_world` is used.

    """
    if comm is None:
        comm = fenics.MPI.comm_world

    _utils.check_file_extension(mesh_file, "xdmf")

    filepath = pathlib.Path(mesh_file)
    folder_path = filepath.parent
    filename = filepath.stem

    if not folder_path.is_dir():
        folder_path.mkdir(parents=True, exist_ok=True)

    with fenics.XDMFFile(comm, mesh_file) as file:
        file.write(mesh)

    if subdomains is not None:
        with fenics.XDMFFile(
            comm, f"{str(folder_path)}/{filename}_subdomains.xdmf"
        ) as file:
            file.write(subdomains)

    if boundaries is not None:
        with fenics.XDMFFile(
            comm, f"{str(folder_path)}/{filename}_boundaries.xdmf"
        ) as file:
            file.write(boundaries)


def convert(
    input_file: str,
    output_file: Optional[str] = None,
    mode: str = "physical",
    quiet: bool = False,
) -> None:
    """Converts the input mesh file to a xdmf mesh file for cashocs to work with.

    Args:
        input_file: A gmsh .msh file.
        output_file: The name of the output .xdmf file or ``None``. If this is ``None``,
            then a file name.msh will be converted to name.xdmf, i.e., the name of the
            input file stays the same
        quiet: A boolean flag which silences the output.
        mode: The mode which is used to define the subdomains and boundaries. Should be
            one of 'physical' (the default), 'geometrical', or 'none'.

    """
    args = [input_file]

    if output_file is not None:
        args += ["-o", output_file]
    if quiet:
        args += ["-q"]

    args += ["--mode", mode]

    cli_convert(args)
    fenics.MPI.barrier(fenics.MPI.comm_world)


def create_point_representation(
    dim: int, points: np.ndarray, idcs: np.ndarray, subwrite_counter: int
) -> str:
    """Creates the representation of the mesh coordinates for gmsh .msh file.

    Args:
        dim: Dimension of the mesh.
        points: The array of the mesh coordinates.
        idcs: The list of indices of the points for the current element.
        subwrite_counter: A counter for looping over the indices.

    Returns:
        A string representation of the mesh coordinates.

    """
    mod_line = ""
    if dim == 2:
        mod_line = (
            f"{points[idcs[subwrite_counter]][0]:.16e} "
            f"{points[idcs[subwrite_counter]][1]:.16e} 0\n"
        )
    elif dim == 3:
        mod_line = (
            f"{points[idcs[subwrite_counter]][0]:.16e} "
            f"{points[idcs[subwrite_counter]][1]:.16e} "
            f"{points[idcs[subwrite_counter]][2]:.16e}\n"
        )

    return mod_line


def gather_coordinates(mesh: fenics.Mesh) -> np.ndarray:
    """Gathers the mesh coordinates on process 0 to write out the mesh to a Gmsh file.

    Args:
        mesh: The corresponding mesh.

    Returns:
        A numpy array which contains the vertex coordinates of the mesh

    """
    comm = mesh.mpi_comm()
    rank = comm.Get_rank()
    top = mesh.topology()
    global_vertex_indices = top.global_indices(0)
    num_global_vertices = mesh.num_entities_global(0)
    local_mesh_coordinates = mesh.coordinates().copy()
    local_coordinates_list = comm.gather(local_mesh_coordinates, root=0)
    vertex_map_list = comm.gather(global_vertex_indices, root=0)

    if rank == 0:
        coordinates = np.zeros((num_global_vertices, local_mesh_coordinates.shape[1]))
        for coords, verts in zip(local_coordinates_list, vertex_map_list):
            coordinates[verts] = coords
    else:
        coordinates = np.zeros((1, 1))
    fenics.MPI.barrier(fenics.MPI.comm_world)

    return coordinates


def parse_file(
    original_msh_file: str, out_msh_file: str, points: np.ndarray, dim: int
) -> None:
    """Parses the mesh file and writes a new, corresponding one.

    Args:
        original_msh_file: Path to the original GMSH mesh file of the mesh object, has
            to end with .msh.
        out_msh_file: Path to the output mesh file, has to end with .msh.
        points: The mesh coordinates gathered on process 0
        dim: The dimensionality of the mesh

    """
    with open(original_msh_file, "r", encoding="utf-8") as old_file, open(
        out_msh_file, "w", encoding="utf-8"
    ) as new_file:
        node_section = False
        info_section = False
        subnode_counter = 0
        subwrite_counter = 0
        idcs = np.zeros(1, dtype=int)

        for line in old_file:
            if line == "$EndNodes\n":
                node_section = False

            if not node_section:
                new_file.write(line)
            else:
                split_line = line.split(" ")
                if info_section:
                    new_file.write(line)
                    info_section = False
                else:
                    if len(split_line) == 4:
                        num_subnodes = int(split_line[-1][:-1])
                        subnode_counter = 0
                        subwrite_counter = 0
                        idcs = np.zeros(num_subnodes, dtype=int)
                        new_file.write(line)
                    elif len(split_line) == 1:
                        idcs[subnode_counter] = int(split_line[0][:-1]) - 1
                        subnode_counter += 1
                        new_file.write(line)
                    elif len(split_line) == 3:
                        mod_line = create_point_representation(
                            dim, points, idcs, subwrite_counter
                        )

                        new_file.write(mod_line)
                        subwrite_counter += 1

            if line == "$Nodes\n":
                node_section = True
                info_section = True


def check_mesh_compatibility(mesh: fenics.Mesh, original_mesh_file: str) -> None:
    """Checks, whether the supplied mesh file is compatible with the mesh used.

    This function returns `None` if they are compatible and raises an exception
    otherwise.

    Args:
        mesh: The mesh that is currently used.
        original_mesh_file: The path to the mesh file.

    """
    num_points = 0
    if fenics.MPI.rank(fenics.MPI.comm_world) == 0:
        with open(original_mesh_file, "r", encoding="utf-8") as file:
            node_info = False
            for line in file:
                if node_info:
                    split_line = line.split(" ")
                    num_points = int(split_line[1])
                    break

                if line == "$Nodes\n":
                    node_info = True

    fenics.MPI.barrier(fenics.MPI.comm_world)

    number_of_points = int(fenics.MPI.comm_world.bcast(num_points, root=0))

    if mesh.num_entities_global(0) != number_of_points:
        raise _exceptions.CashocsException(
            "The mesh supplied in the configuration file is not "
            "compatible with the mesh used."
        )


def write_out_mesh(  # noqa: C901
    mesh: fenics.Mesh, original_msh_file: str, out_msh_file: str
) -> None:
    """Writes out mesh as Gmsh .msh file.

    This method updates the vertex positions in the ``original_gmsh_file``, the
    topology of the mesh and its connections are the same. The original GMSH
    file is kept, and a new one is generated under ``out_mesh_file``.

    Args:
        mesh: The mesh object in fenics that should be saved as Gmsh file.
        original_msh_file: Path to the original GMSH mesh file of the mesh object, has
            to end with .msh.
        out_msh_file: Path to the output mesh file, has to end with .msh.

    Notes:
        The method only works with GMSH 4.1 file format. Others might also work, but
        this is not tested or ensured in any way.

    """
    check_mesh_compatibility(mesh, original_msh_file)
    dim = mesh.geometric_dimension()

    if not pathlib.Path(out_msh_file).parent.is_dir():
        pathlib.Path(out_msh_file).parent.mkdir(parents=True, exist_ok=True)

    points = gather_coordinates(mesh)

    if fenics.MPI.rank(fenics.MPI.comm_world) == 0:
        parse_file(original_msh_file, out_msh_file, points, dim)
    fenics.MPI.barrier(fenics.MPI.comm_world)


def read_mesh_from_xdmf(
    filename: str, step: int = 0, comm: Optional[MPI.Comm] = None
) -> fenics.Mesh:
    """Reads a mesh from a .xdmf file containing a checkpointed function.

    Args:
        filename: The filename to the .xdmf file.
        step: The checkpoint number. Default is ``0``.
        comm: MPI communicator that is to be used for creating the mesh.

    Returns:
        The corresponding mesh for the checkpoint number.

    """
    h5_filename = f"{filename[:-5]}.h5"
    with h5py.File(h5_filename) as file:
        name = list(file.keys())[0]
        step_name = f"{name}_{step}"
        coordinates = file[name][step_name]["mesh"]["geometry"][()]
        cells = file[name][step_name]["mesh"]["topology"][()]

    gdim = coordinates.shape[1]

    if cells.shape[1] == 2:
        tdim = 1
        cell_type = "line"
    elif cells.shape[1] == 3:
        tdim = 2
        cell_type = "triangle"
    elif cells.shape[1] == 4:
        tdim = 3
        cell_type = "tetrahedron"
    else:
        raise _exceptions.CashocsException("The mesh saved in the xdmf file is faulty.")

    if tdim > gdim:
        raise _exceptions.CashocsException(
            "The topological dimension of a mesh must not be larger than its "
            "geometrical dimension"
        )

    if comm is None:
        comm = fenics.MPI.comm_world

    mesh = fenics.Mesh(comm)

    if fenics.MPI.rank(fenics.MPI.comm_world) == 0:
        mesh_editor = fenics.MeshEditor()
        mesh_editor.open(mesh, cell_type, tdim, gdim)
        mesh_editor.init_vertices(coordinates.shape[0])
        mesh_editor.init_cells(cells.shape[0])

        for i, vertex in enumerate(coordinates):
            mesh_editor.add_vertex(i, vertex)
        for i, cell in enumerate(cells):
            mesh_editor.add_cell(i, cell)

        mesh_editor.close()
        mesh.init()
        mesh.order()

    fenics.MeshPartitioning.build_distributed_mesh(mesh)

    return mesh


def extract_mesh_from_xdmf(
    xdmffile: str,
    iteration: int = 0,
    outputfile: Optional[str] = None,
    original_gmsh_file: Optional[str] = None,
    quiet: bool = False,
) -> None:
    """Extracts a Gmsh mesh file from an XDMF state file.

    Args:
        xdmffile: The path to the XDMF state file.
        iteration: The iteration of interest (for a time series saved in the XDMF file),
            default is 0.
        outputfile: The path to the output Gmsh file. The default is `None` in which
            case the output is saved in the same directory as the XDMF state file.
        original_gmsh_file: The original gmsh .msh file used to create the mesh. This
            can be used to generate output files which preserve, e.g., physical tags
            and only updates the nodal positions. This will not work if the geometry
            has been remeshed. The default is `None`, which uses a more robust (but
            less detailed) approach.
        quiet: When this is set to `True`, verbose output is disabled. Default is
            `False`.

    """
    start_time = time.time()

    _utils.check_file_extension(xdmffile, "xdmf")
    if outputfile is None:
        outputfile = f"{xdmffile[:-5]}.msh"
    _utils.check_file_extension(outputfile, "msh")

    mesh = read_mesh_from_xdmf(xdmffile, step=iteration)

    if fenics.MPI.rank(fenics.MPI.comm_world) == 0:
        tmp = tempfile.mkdtemp(prefix="cashocs_tmp_")
    else:
        tmp = ""
    fenics.MPI.barrier(fenics.MPI.comm_world)
    tempdir = fenics.MPI.comm_world.bcast(tmp, root=0)

    mesh_location_xdmf = f"{tempdir}/mesh.xdmf"
    fenics.MPI.barrier(fenics.MPI.comm_world)
    if original_gmsh_file is None:
        try:
            with fenics.XDMFFile(fenics.MPI.comm_world, mesh_location_xdmf) as file:
                file.write(mesh, fenics.XDMFFile.Encoding.HDF5)

            fenics.MPI.barrier(fenics.MPI.comm_world)
            if fenics.MPI.rank(fenics.MPI.comm_world) == 0:
                subprocess.run(  # nosec B603, B607
                    [
                        "meshio",
                        "convert",
                        "--output-format",
                        "gmsh",
                        "--ascii",
                        mesh_location_xdmf,
                        outputfile,
                    ],
                    check=True,
                )
            fenics.MPI.barrier(fenics.MPI.comm_world)
        finally:
            fenics.MPI.barrier(fenics.MPI.comm_world)
            if fenics.MPI.rank(fenics.MPI.comm_world) == 0:
                subprocess.run(["rm", "-r", tempdir], check=True)  # nosec B603, B607
            fenics.MPI.barrier(fenics.MPI.comm_world)

    else:
        write_out_mesh(mesh, original_gmsh_file, outputfile)

    end_time = time.time()
    if not quiet:
        _loggers.info(
            f"Successfully extracted the desired mesh {outputfile} from {xdmffile}"
            f" in {end_time - start_time:.2f} s"
        )
