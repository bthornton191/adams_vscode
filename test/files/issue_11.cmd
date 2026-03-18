variable set variable=$_self.pyExe integer= &
(eval(run_python_code("execute_cmd('variable set variable=$_self.fileList string=(eval(STR_SPLIT(STR_REPLACE_ALL(STR_SUBSTR('+repr(str(files))+',2,STR_LENGTH('+repr(str(files))+')-2),"\'", ""),",")))')")))

variable set variable=after_expr real=1.0
