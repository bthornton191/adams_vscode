from typing import Any, Dict, Literal
import Object
import Model
from Model import ModelManager
from Group import GroupManager
from Expression import eval as eval, expression as expression
from Defaults import AdamsDefaults

DBRoot: Any

class AdamsRoot(Object.Object): ...


Models: ModelManager
defaults: AdamsDefaults
preferences: Any
Groups: GroupManager
Libraries: Any
AttributesLibraries: Any
Colors: Any
Materials: Any

def getCurrentModel()->Model.Model: ...
def execute_cmd(cmd : str) -> None: 
    """Executs a Command Language(cmd) command though python. 

    Parameters
    ----------
    cmd : str
        Command to be executed

    Example
    -------
    ``` 
    Adams.execute_cmd("model create model_name=MODEL_1") 
    ```
    """
    ...

def evaluate_exp(exp : str) -> Any:
    """Evaluates and returns the value of the given expression. 

    Parameters
    ----------
    exp : str
        Expression to be evaluated.

    Returns
    -------
    Any
        Expression value

    Example
    -------
    ```
    dv_val=Adams.evaluate_exp(".MODEL_1.DV_1") 
    ```
    """
    ...
def evaluate_real_exp(exp : str) -> Any:
    """Evaluates and returns the value of the given expression that results in an real value or an array of reals.

    Parameters
    ----------
    exp : str
        Expression to be evaluated.

    Returns
    -------
    Any
        Expression value

    Example
    -------
    ```
    dv_val=Adams.evaluate_exp(".MODEL_1.DV_1") 
    ```

    """
    ...
def write_binary_file(file_name : str) -> bool:
    """Exports a Adams View binary database file.

    Parameters
    ----------
    file_name : str
        Name of file to write.

    Returns
    -------
    bool
        True
    
    Example
    -------
    ```
    Adams.write_binary_file("model_test.bin") 
    ```

    """
    ...
def read_binary_file(file_name : str) -> bool:
    """Reads a Adams View binary file.

    Parameters
    ----------
    file_name : str
        Name of file to read.

    Returns
    -------
    bool
        True
    
    Example
    -------
    ``` 
    Adams.read_binary_file("model_test.bin") 
    ```
    
    """
    ...
def write_command_file(file_name : str, model : Model.Model) -> bool: 
    """Exports a Adams View command file. 

    Parameters
    ----------
    file_name : str
        Name of file to write.
    model : Model.Model
        Model to write.

    Returns
    -------
    bool
        True

    Example
    -------
    ```
    Adams.write_command_file(file_name = "model_test.cmd", model = model_1) 
    ```

    """
    ...
def read_command_file(file_name : str) -> bool:
    """Reads a command file and execute commands contained within. 

    Parameters
    ----------
    file_name : str
        Name of file to read.

    Returns
    -------
    bool
        True

    Example
    -------
    ```
    Adams.read_command_file("model_test.cmd") 
    ```

    """
    ...
def read_geometry_file(
    type_of_geometry : Literal[
        'catiav4',
        'catiav5',
        'catiav6',
        'igs',
        'inventor',
        'acis',
        'proe',
        'solidworks',
        'stp',
        'unigraphics',
        'jt',
        'dxf',
        'dwg'
    ],
    file_name : str,
    **kwargs) -> None:
    """Reads a geometry file given file name and type_of_geometry contained in the file. Must  provide either `part_name` or `model_name`.

    Parameters
    ----------
    type_of_geometry : str
        Geometry file type. Options are 'catiav4', 'catiav5', 'catiav6', 'igs', 'inventor', 'acis', 'proe', 'solidworks', 'stp', 'unigraphics', 'jt', 'dxf', 'dwg'

    file_name : str
        Name of file to read.
    
    model_name : str
        Name of model to read the geometry into
    
    part_name : str
        Name of part to read the geometry into

    Example
    -------
    ```
    Adams.read_geometry_file(file_name="test.igs", type_of_geometry="igs")
    ```
    """
    ...
def write_geometry_file(
    type_of_geometry : Literal[
        'catiav4',
        'catiav5',
        'catiav6',
        'igs',
        'inventor',
        'acis',
        'proe',
        'solidworks',
        'stp',
        'unigraphics',
        'jt',
        'dxf',
        'dwg'
    ],
    file_name : str,
    **kwargs) -> None:
    """Exports a geometry file given type_of_geometry, file_name, and one of model_name, part_name, or analysis_name and frame_number.  Must  provide either `part_name`, `model_name`, or `analysis_name` keyword arguments.

    Parameters
    ----------
    type_of_geometry : str
        Geometry file type. Options are 'catiav4', 'catiav5', 'catiav6', 'igs', 'inventor', 'acis', 'proe', 'solidworks', 'stp', 'unigraphics', 'jt', 'dxf', 'dwg'

    file_name : str
        Name of file to read.

    model_name : str, optional
        Name of model to write

    part_name : str, optional
        Name of model to write

    analysis_name : str, optional
        Name of analysis to write

    frame_number : int, optional
        Frame to write.  Required if `analysis_name` is given.

    Example
    -------
    ```
    Adams.write_geometry_file(file_name="test.igs", type_of_geometry="igs", model_name="MODEL_1") 
    ```

    """
    ...
def undo_begin_block() -> None:
    """Signals the start of a new undo block in an existing nested set of undo blocks. 
    This allow you to group commands, as you issue them from the command window, into undo blocks. 
    By grouping them into undo blocks, you can use a single Undo command to reverse all the operations in the block. 
    You can define undo blocks around macros, command files, or any group of commands. You can nest them to any level

    Example
    -------
    ```
    Adams.undo_begin_block()
    ```

    """
    ...
def undo_end_block() -> None:
    """Signals the end of the last undo block in the nested set of undo blocks. You can nest undo blocks to any level.

    Example
    -------
    ```
    Adams.undo_end_block()
    ```

    """
    ...
def undo() -> None:
    """Allows you to reverse the action of the previous undo-block given to Adams View, so that Adams View appears as it did before the command was originally issued.

    Example
    ------
    ```
    Adams.undo()
    ```

    """
    ...
def redo() -> None:
    """Allows you to reverse the action of the last undo backward command, and makes Adams View appear as it did before the reverse action was originally done.
    
    Example
    -------
    ```
    Adams.redo()
    ```

    """
    ...
def read_parasolid_file(file_name : str, **kwargs) -> None:
    """Reads a parasolid file given the file_name and one of model_name, part_name or fe_part_name.  Must  provide either `part_name`, `model_name`, or `fe_part_name` keyword arguments.

    Parameters
    ----------
    file_name : str
        Name of file to read
    

    model_name : str, optional
        Name of model to read geometry into

    part_name : str, optional
        Name of model to read geometry into

    fe_part_name : str, optional
        Name of fe_part to read geometry into

    Example
    -------
    ```
    Adams.read_parasolid_file(file_name="Parasolid.xmt_txt", part_name = "MODEL_1.Part_2") 
    ```

    """
    ...
def write_parasolid_file(file_name: str, **kwargs) -> None:
    """Writes a parasolid file given the file_name and one of model_name, part_name or analysis_name.  

    Parameters
    ----------
    file_name : str
        Name of file to read.

    model_name : str, optional
        Name of model to write

    part_name : str, optional
        Name of model to write

    analysis_name : str, optional
        Name of analysis to write

    frame_number : int, optional
        Frame to write.  Required if `analysis_name` is given.

    Example
    -------
    ```
    Adams.write_parasolid_file(file_name = "Parasolid.xmt_txt",model_name = "MODEL_1") 
    ```

    """
    ...
def stoo(name : str) -> Object.Object:
    """Returns python object of a given full name.

    Parameters
    ----------
    name : str
        A string that is the name of an existing object.

    Returns
    -------
    Object.Object
        An existing object

    Example
    ```
    mrk_1=Adams.stoo(".MODEL_TEST.PART_1.MARKER_1") 
    ```

    """
    ...
def switchToCmd() -> None:
    """Switches the active scripting language to the Adams CMD language in a cmd script having a mix of CMD & Python commands.
    To switch back to Python, use the CMD language command "language switch_to python".
    
    Example
    -------
    ```
    Adams.switchToCmd()
    ```
    
    """
    ...
