import Adams

mod = Adams.Models.create(name='model_1')

part_1 = mod.Parts.createRigidBody(name='part_1',
                                   location=(0,0,0),
                                   mass=1.0)


mkr_1 = part_1.Markers.create(name='mkr_1')

part_2 = mod.Parts.createRigidBody(name='part_2',
                                   location=(1,0,0),
                                   mass=2.0)

mkr_2 = part_2.Markers.create(name='mkr_2',
                              location=mkr_1.location_global,
                              relative_to=mod.ground_part)


fixed_joint = mod.Constraints.createFixed(name='fixed_joint',
                                          i_marker=mkr_1,
                                          j_marker=mkr_2)


