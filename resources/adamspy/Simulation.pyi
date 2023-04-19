from typing import Any, ItemsView, Iterable, KeysView, ValuesView

import Manager
import Object

class SimulationManager(Manager.AdamsManager):
    def create(self, **kwargs)->Simulation: ...
    def items(self) -> ItemsView[str, Simulation]: ...
    def values(self) -> ValuesView[Simulation]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Simulation: ...
    def __iter__(self, *args) -> Iterable[str]: ...

class Simulation(Object.ObjectComment):

    """class for creating and running simple and scripted simulations

    Usage
    -----
    
    ```python
    simulation_object=model_object.Simulations.create(name='sim0', [optional_arguments]) #create a simulation object
    ```

    Example
    -------

    ```python
    m=Adams.defaults.model

    s1=m.Simulations.create(name='sim1') 
    s1.simulate() #run a simple simulation with default end_time and number_of_steps

    s2=m.Simulations.create(name='sim2', end_time=1.25, initial_static=True, number_of_steps=50)
    s2.simulate() #run this simple simulation with specified properties values

    s3=m.Simulations.create(name='sim3')
    s3.script_type='solver_commands'
    s3.script="file/command=sim_test.acf"
    s3.simulate() #run simulation using acf commands in sim_test.acf file

    s4_sim_script=["simulate/transient,duration=10, dtout=0.01","linear/statemat,file=model.mat"]
    s4=m.Simulations.create(name='sim4', script_type='solver_commands', script=s4_sim_script)
    s4.simulate() #run simulation with inlined acf commands

    s5=m.Simulations.create(name='sim5', script_type='commands', script="simulation single_run transient type=auto_select initial_static=no end_time=5.0 number_of_steps=50")
    s5.simulate() #run simulation with inlined cmd
    ```
    """

    _manager: SimulationManager
    sim_type: str
    """type of simple simulation, auto_select by default """
    duration: float
    """duration of the simulation"""
    end_time: float
    """end time duration of the simulation"""
    initial_static: bool
    """True if static analysis is to be performed first, False by default"""
    number_of_steps: int
    """number of steps in the simulation"""
    script: str
    """simulation script for a scripted simulation"""
    script_type: str
    """type of script, simple by default"""
    comments: str
    _mutually_exclusive: Any
    def __init__(self, _DBKey: Any) -> Any: ...
    def simulate(self, analysis_name: Any = ...) -> Any: 
        """
        Method runs simulations based on Adams View Settings -> Solver -> Executable
        """
        ...
