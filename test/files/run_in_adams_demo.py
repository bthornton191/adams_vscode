import Adams
from Part import RigidBody
from Model import Model

def create_geom(idx: int, part: RigidBody):
    
    # test if idx is even
    if idx % 2 == 0:
        geom = part.Geometries.createEllipsoid(name=f'sphere_{idx}',
                                               center_marker=part.cm,
                                               x_scale_factor=1,
                                               y_scale_factor=1,
                                               z_scale_factor=1)
    else:
        corner_mkr = part.Markers.create(name=f'crnr_mkr',
                                         location=[-0.25, -0.25, -0.25],
                                         relative_to=part.cm)
        
        geom = part.Geometries.createBlock(name=f'block_{idx}',
                                           corner_marker=corner_mkr,
                                           x=0.5,
                                           y=0.5,
                                           z=0.5)
    return geom

def create_parts(mod: Model):
    for idx, part in enumerate(mod.Parts.values()):
        if part.ground_part:
            continue
        part: RigidBody
        cm = part.Markers.create(name='cm', location=[idx, 0, 0])
        i_mkr = part.Markers.create(name='i_mkr', location=[idx, 0, 0])
        j_mkr = mod.ground_part.Markers.create(name=f'j_mkr_{idx}', location=[idx, 0, 0])

        part.cm = cm
        part.mass = idx*0.2

        create_geom(idx, part)

        jnt = mod.Constraints.createFixed(name=f'fj_{idx}',
                                        i_marker=i_mkr,
                                        j_marker=j_mkr)
    

mod = Adams.getCurrentModel()
create_parts(mod)

