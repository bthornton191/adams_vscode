import Adams  # type: ignore

mod = Adams.getCurrentModel()
part = mod.Parts['PART_2']

mass = part.mass
print(mass)
