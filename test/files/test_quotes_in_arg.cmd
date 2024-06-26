
interface dialog_box create &
    dialog_box_name=test & ! This is a comment
    execution_commands="var set var=.mdi.tmp_int int=1", & ! This is a comment
                       "var set var=.mdi.tmp_str str=hello"

model create &
    comments="comment 1" &
    model_name=mod1 &
    list_arg = "a=1", &
               "b=2", &
               "c" &
    another_arg = "hello"



