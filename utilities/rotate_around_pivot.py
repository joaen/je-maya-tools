import maya.api.OpenMaya as om
import pymel.core as pm


def rotate_around_pivot(x, y, z, pivot, rotate_transform):
    # Euler angles in degrees (X, Y, Z)
    euler_deg = [x, y, z]

    # Convert degrees to radians
    euler_rad = [angle * (3.141592653589793 / 180.0) for angle in euler_deg]

    # Move object to pivot origin and store direction and position vector
    pivot_vec = om.MVector(pm.xform(pivot, q=True, worldSpace=True, translation=True))
    transform_vec = om.MVector(pm.xform(rotate_transform, worldSpace=True, q=True, translation=True))
    direction = (transform_vec - pivot_vec)
    diff = (pivot_vec - transform_vec)
    pm.xform(rotate_transform, worldSpace=True, translation=diff)
    
    # Rotate object
    current_rotation = pm.xform(rotate_transform, query=True, worldSpace=True, rotation=True)
    pm.xform(rotate_transform,
            worldSpace=True,
            rotation=[
                current_rotation[0] + euler_deg[0],
                current_rotation[1] + euler_deg[1],
                current_rotation[2] + euler_deg[2]
                ])

    # Create quaternion from euler angles
    quaternion = om.MEulerRotation(euler_rad).asQuaternion()
    new_direction = direction.rotateBy(quaternion)

    # Calculate new position
    new_pos = pivot_vec + new_direction.normalize() * direction.length()
    
    # Set new position
    pm.xform(rotate_transform, translation=new_pos)

# Example code:
# rotate_around_pivot(0, 0, 90, "earth_mesh", "sun_mesh")