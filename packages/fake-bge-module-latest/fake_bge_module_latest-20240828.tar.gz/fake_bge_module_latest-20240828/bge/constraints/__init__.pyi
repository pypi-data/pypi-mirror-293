"""
Bullet Physics provides collision detection
and rigid body dynamics for the Blender Game Engine.

Features:

* Vehicle simulation.
* Rigid body constraints: hinge and point to point (ball socket).
* Access to internal physics settings,
like deactivation time, and debugging features

[NOTE]
Note about parameter settings
Since this API is not well documented, it can be unclear what kind of values to use for setting parameters.
In general, damping settings should be in the range of 0 to 1 and
stiffness settings should not be much higher than about 10.


--------------------

For more examples of Bullet physics and how to use them
see the pybullet forum.



```../examples/bge.constraints.py```


--------------------


--------------------


--------------------

Debug mode to be used with setDebugMode.


--------------------

Constraint type to be used with createConstraint.

"""

import typing
import collections.abc
import typing_extensions

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

def createConstraint(
    physicsid_1: int,
    physicsid_2: int,
    constraint_type: int,
    pivot_x: float = 0.0,
    pivot_y: float = 0.0,
    pivot_z: float = 0.0,
    axis_x: float = 0.0,
    axis_y: float = 0.0,
    axis_z: float = 0.0,
    flag: int = 0,
):
    """Creates a constraint.

    :param physicsid_1: The physics id of the first object in constraint.
    :type physicsid_1: int
    :param physicsid_2: The physics id of the second object in constraint.
    :type physicsid_2: int
    :param constraint_type: The type of the constraint, see Create Constraint Constants.
    :type constraint_type: int
    :param pivot_x: Pivot X position. (optional)
    :type pivot_x: float
    :param pivot_y: Pivot Y position. (optional)
    :type pivot_y: float
    :param pivot_z: Pivot Z position. (optional)
    :type pivot_z: float
    :param axis_x: X axis angle in degrees. (optional)
    :type axis_x: float
    :param axis_y: Y axis angle in degrees. (optional)
    :type axis_y: float
    :param axis_z: Z axis angle in degrees. (optional)
    :type axis_z: float
    :param flag: 128 to disable collision between linked bodies. (optional)
    :type flag: int
    :return: A constraint wrapper.
    """

    ...

def createVehicle(physicsid: int):
    """Creates a vehicle constraint.

    :param physicsid: The physics id of the chassis object in constraint.
    :type physicsid: int
    :return: A vehicle constraint wrapper.
    """

    ...

def exportBulletFile(filename: str):
    """Exports a file representing the dynamics world (usually using .bullet extension).See Bullet binary serialization.

    :param filename: File path.
    :type filename: str
    """

    ...

def getAppliedImpulse(constraintId: int) -> float:
    """

    :param constraintId: The id of the constraint.
    :type constraintId: int
    :return: The most recent applied impulse.
    :rtype: float
    """

    ...

def getCharacter(gameobj):
    """

    :param gameobj: The game object with the character physics.
    :return: Character wrapper.
    """

    ...

def getVehicleConstraint(constraintId: int):
    """

    :param constraintId: The id of the vehicle constraint.
    :type constraintId: int
    :return: A vehicle constraint object.
    """

    ...

def removeConstraint(constraintId: int):
    """Removes a constraint.

    :param constraintId: The id of the constraint to be removed.
    :type constraintId: int
    """

    ...

def setCFM(cfm):
    """Sets the Constraint Force Mixing (CFM) for soft constraints.
    If the Constraint Force Mixing (CFM) is set to zero, the constraint will be hard.
    If CFM is set to a positive value, it will be possible to violate the constraint by pushing on it (for example, for contact constraints by forcing the two contacting objects together).
    In other words the constraint will be soft, and the softness will increase as CFM increases.

        :param cfm: The CFM parameter for soft constraints.
    """

    ...

def setContactBreakingTreshold(breakingTreshold: float):
    """Sets tresholds to do with contact point management.

    :param breakingTreshold: The new contact breaking treshold.
    :type breakingTreshold: float
    """

    ...

def setDeactivationAngularTreshold(angularTreshold: float):
    """Sets the angular velocity treshold.

    :param angularTreshold: New deactivation angular treshold.
    :type angularTreshold: float
    """

    ...

def setDeactivationLinearTreshold(linearTreshold: float):
    """Sets the linear velocity treshold.

    :param linearTreshold: New deactivation linear treshold.
    :type linearTreshold: float
    """

    ...

def setDeactivationTime(time: float):
    """Sets the time after which a resting rigidbody gets deactived.

    :param time: The deactivation time.
    :type time: float
    """

    ...

def setDebugMode(mode: int):
    """Sets the debug mode.

    :param mode: The new debug mode, see Debug Mode Constants.
    :type mode: int
    """

    ...

def setERPContact(erp2):
    """Sets the Error Reduction Parameter (ERP) for contact constraints.
    The Error Reduction Parameter (ERP) specifies what proportion of the joint error will be fixed during the next simulation step.
    If ERP = 0.0 then no correcting force is applied and the bodies will eventually drift apart as the simulation proceeds.
    If ERP = 1.0 then the simulation will attempt to fix all joint error during the next time step.
    However, setting ERP = 1.0 is not recommended, as the joint error will not be completely fixed due to various internal approximations.
    A value of ERP = 0.1 to 0.8 is recommended.

        :param erp2: The ERP parameter for contact constraints.
    """

    ...

def setERPNonContact(erp):
    """Sets the Error Reduction Parameter (ERP) for non-contact constraints.
    The Error Reduction Parameter (ERP) specifies what proportion of the joint error will be fixed during the next simulation step.
    If ERP = 0.0 then no correcting force is applied and the bodies will eventually drift apart as the simulation proceeds.
    If ERP = 1.0 then the simulation will attempt to fix all joint error during the next time step.
    However, setting ERP = 1.0 is not recommended, as the joint error will not be completely fixed due to various internal approximations.
    A value of ERP = 0.1 to 0.8 is recommended.

        :param erp: The ERP parameter for non-contact constraints.
    """

    ...

def setGravity(x: float, y: float, z: float):
    """Sets the gravity force.Sets the linear air damping for rigidbodies.

    :param x: Gravity X force.
    :type x: float
    :param y: Gravity Y force.
    :type y: float
    :param z: Gravity Z force.
    :type z: float
    """

    ...

def setNumIterations(numiter: int):
    """Sets the number of iterations for an iterative constraint solver.

    :param numiter: New number of iterations.
    :type numiter: int
    """

    ...

def setNumTimeSubSteps(numsubstep: int):
    """Sets the number of substeps for each physics proceed. Tradeoff quality for performance.

    :param numsubstep: New number of substeps.
    :type numsubstep: int
    """

    ...

def setSolverDamping(damping: float):
    """Sets the damper constant of a penalty based solver.

    :param damping: New damping for the solver.
    :type damping: float
    """

    ...

def setSolverTau(tau: float):
    """Sets the spring constant of a penalty based solver.

    :param tau: New tau for the solver.
    :type tau: float
    """

    ...

def setSolverType(solverType: int):
    """Sets the solver type.

    :param solverType: The new type of the solver.
    :type solverType: int
    """

    ...

def setSorConstant(sor: float):
    """Sets the successive overrelaxation constant.

    :param sor: New sor value.
    :type sor: float
    """

    ...

ANGULAR_CONSTRAINT: int

CONETWIST_CONSTRAINT: int

DBG_DISABLEBULLETLCP: int
""" Disable Bullet LCP.
"""

DBG_DRAWAABB: int
""" Draw Axis Aligned Bounding Box in debug.
"""

DBG_DRAWCONSTRAINTLIMITS: int
""" Draw constraint limits in debug.
"""

DBG_DRAWCONSTRAINTS: int
""" Draw constraints in debug.
"""

DBG_DRAWCONTACTPOINTS: int
""" Draw contact points in debug.
"""

DBG_DRAWFREATURESTEXT: int
""" Draw features text in debug.
"""

DBG_DRAWTEXT: int
""" Draw text in debug.
"""

DBG_DRAWWIREFRAME: int
""" Draw wireframe in debug.
"""

DBG_ENABLECCD: int
""" Enable Continuous Collision Detection in debug.
"""

DBG_ENABLESATCOMPARISION: int
""" Enable sat comparison in debug.
"""

DBG_FASTWIREFRAME: int
""" Draw a fast wireframe in debug.
"""

DBG_NODEBUG: int
""" No debug.
"""

DBG_NOHELPTEXT: int
""" Debug without help text.
"""

DBG_PROFILETIMINGS: int
""" Draw profile timings in debug.
"""

GENERIC_6DOF_CONSTRAINT: int

LINEHINGE_CONSTRAINT: int

POINTTOPOINT_CONSTRAINT: int

VEHICLE_CONSTRAINT: int

error: str
""" Symbolic constant string that indicates error.
"""
