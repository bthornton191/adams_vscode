# THIS FILE IS AUTOMATICALLY GENERATED, DO NOT EDIT.

from typing import Any

from Object import Object

class Solver(Object):
    arr_len: int
    def __init__(self, Name: Any, ParentDBKey: Any, _DBKey: Any): ...
    
    @staticmethod
    def create(Name: Any, Parent: Any) -> Solver: ...
    def setInitialCondition(self, ic: Any) -> Any: 
        """
        Set Initial Condition for solver

        Parameters
        ----------
        float
            Initial Condition value       
        """
        ...
    def getInitialCondition(self) -> Any: 
        """
        Returns initial condition of solver
        """
        ...

    def setFunction(self, *args) -> Any: 
        """
        Set Function for solver. Supports Min : 1 & Max : 100 arguments

        Parameters
        ----------
        str
            Solver Function       
        """
        ...

    def getFunction(self) -> str: 
        """
        Returns Solver Function
        """
        ...

    def setUserFunction(self, *args) -> Any: 
        """
        Set User Function for solver.Supports Min : 1 & Max : 30 arguments

        Parameters
        ----------
        float
            Solver User Function       
        """
        ...
        
    def getUserFunction(self) -> str: 
        """
        Returns Solver User Function
        """
        ...

    def setRoutine(self, rout: Any) -> Any: 
        """
        Set Routine for Solver.

        Parameters
        ----------
        str
            Solver Routine     
        """
        ...

    def getRoutine(self) -> Any: 
        """
        Returns Solver Routine
        """
        ...

    def evaluateExpression(self, text: Any) -> Any: ...
    def evaluateVectorExpression(self, *args) -> Any: ...
    def simIC(self, ic: Any) -> Any: ...
