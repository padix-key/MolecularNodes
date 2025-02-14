import numpy as np
import biotite.structure.io.mmtf as mmtf
import biotite
from . import AssemblyParser


class MMTFAssemblyParser(AssemblyParser):
    ### Implementation adapted from ``biotite.structure.io.mmtf.assembly``

    def __init__(self, mmtf_file):
        self._file = mmtf_file
    

    def list_assemblies(self):
        return mmtf.list_assemblies(self._file)
    

    def get_transformations(self, assembly_id):
        # Find desired assembly
        selected_assembly = None
        if not "bioAssemblyList" in self._file:
            raise biotite.InvalidFileError(
                "File does not contain assembly information "
                "(missing 'bioAssemblyList')"
            )
        for assembly in self._file["bioAssemblyList"]:
            current_assembly_id = assembly["name"]
            transform_list = assembly["transformList"]
            if current_assembly_id == assembly_id:
                selected_assembly = transform_list
                break
        if selected_assembly is None:
            raise KeyError(
                f"The assembly ID '{assembly_id}' is not found"
            )

        # Parse transformations from assembly
        transformations = []
        for transform in selected_assembly:
            matrix = np.array(transform["matrix"]).reshape(4, 4)
            chain_ids = np.array(self._file["chainNameList"], dtype="U4")
            affected_chain_ids = chain_ids[transform["chainIndexList"]]
            transformations.append((
                affected_chain_ids,
                matrix[:3, :3],
                matrix[:3, 3]
            ))
        
        return transformations