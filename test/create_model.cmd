model create model='hello'

for var=.mdi.obj obj=(eval(db_children(db_default(system_defaults, "model"), "all")))
    var set var=.mdi.tmpstr str=(eval(str_print(.mdi.obj)))
end

var set var=.mdi.tmpstr str=(eval(str_print('HELLO WORLD!!')))

part create rigid_body name_and_position  &
    part_name = "hello_part3"


geometry create &
    geometry_name = "hello" &

part create rigid_body name_and_position 


part create rigid_body name_and_position location=0,0,0 part_name="part" relative_to="other_part"

geometry create point point_name="point_name" ref_marker_name=marker 
