import Adams  # type: ignore

mod = Adams.Models.create(name='test_model')
part = mod.Parts.createRigidBody(name='PART_2')

part.mass = 1
pass
part.mass = 2
