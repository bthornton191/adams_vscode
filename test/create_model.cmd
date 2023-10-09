model create model='hello'

for var=.mdi.obj obj=(eval(db_children(db_default(system_defaults, "model"), "all")))
    var set var=.mdi.tmpstr str=(eval(str_print(.mdi.obj)))
end

var set var=.mdi.tmpstr str=(eval(str_print('HELLO WORLD!!')))

part create rigid_body name_and_position  &
    part_name = "hello_part3"

