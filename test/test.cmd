!$contact_obj:t=contact:C=1
!$Analysis:t=analysis:C=1
!$New_plot_name: t=string: C=1: D=advanced_contact_plot

data_element modify matrix full &
   matrix_name = $model.rn_mtx &
   ! row_count = (eval($_self.tooth*4) - 2) &
   row_count = (eval($model.rn_mtx.row_count) + 6) &
   values =    (eval($model.rn_mtx.values)), &
               ($minor_d/2),           (eval($_self.stub_L) + (eval($_self.tooth) - 1)*$tooth_pitch),                                                                                                              0, &
               ($tooth_pitch_diam/2),  (eval($_self.stub_L) + (eval($_self.tooth) - 1)*$tooth_pitch + eval($_self.bot_flnk_ofst)*($tooth_pitch_diam-$minor_d)/($major_d-$minor_d)),                                0, &
               ($major_d/2),           (eval($_self.stub_L) + (eval($_self.tooth) - 1)*$tooth_pitch + eval($_self.bot_flnk_ofst)),                                                                                 0, &
               ($major_d/2),           (eval($_self.stub_L) + (eval($_self.tooth) - 1)*$tooth_pitch + eval($_self.root_width) - eval($_self.top_flnk_ofst)),                                                       0, &
               ($tooth_pitch_diam/2),  (eval($_self.stub_L) + (eval($_self.tooth) - 1)*$tooth_pitch + eval($_self.root_width) - eval($_self.top_flnk_ofst)*($tooth_pitch_diam-$minor_d)/($major_d-$minor_d)),      0, &
               ($minor_d/2),           (eval($_self.stub_L) + (eval($_self.tooth) - 1)*$tooth_pitch + eval($_self.root_width)),                                                                                    0
    


var set var=$_self.pystr str="import os", &
							"from pathlib import Path", &
							"sys", &
							"sys.path.insert(0, os.path.join('C:\\\\', 'Users', 'bthornt', 'Hexagon', 'NNL - Roller Nut Drive - Engineering', 'plugin', 'working_directory', 'modules'))", &
							"from qual.utilities.spline import check_spline", &
							eval(str_xlate(str_xlate("current_in=" // .rotating_assembly.torque_spln_mtx.values[*,1], "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("lag_in=" // .rotating_assembly.torque_6p0.xs, "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("engagement_in=" // .rotating_assembly.torque_6p0.zs, "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("torque_in =" // .rotating_assembly.torque_6p0.ys, "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("torque_in+=" // .rotating_assembly.torque_8p0.ys, "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("torque_in+=" // .rotating_assembly.torque_10p0.ys, "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("torque_in+=" // .rotating_assembly.torque_12p0.ys, "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("current_out=" // .rotating_assembly.Last_Run.current.Q.values, "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("lag_out=" // .rotating_assembly.Last_Run.lag.Q.values, "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("engagement_out=" // .rotating_assembly.Last_Run.engagement.Q.values, "{", "["), "}", "]")), &
							eval(str_xlate(str_xlate("torque_out=" // .rotating_assembly.Last_Run.stator_torque.TY.values, "{", "["), "}", "]")), &
							"check_spline(current_in, lag_in, engagement_in, torque_in, current_out, lag_out, engagement_out, torque_out)"



def com echo=on
model merge model_name = (eval($_self.mod)) into_model_name = "$assembly_name" duplicate_parts = merge
variable set variable=$_self.varname real=2
! ----------------
! Collate Contacts
! ----------------
! NOTE: This combines multiple contact tracks into one
analysis collate_contacts &
   analysis_name=$Analysis &
   contact=$contact_obj

var set var=sep_str string='.' 
var set var=number real=.05
var set var=$_self.varname real=(eval(abs())))

mar create marker_name = .my_part.marker_1

! Check if plot name already exists and add an incremental suffix if needed

if condition = (.model.analysis != 1 || .model.analysis == 2 && )

if condition = (DB_EXISTS(eval("."//"$New_plot_name")))
   variable set &
	   variable_name = plotname &
	   string = (UNIQUE_NAME(eval("$New_plot_name")))
else
   variable set & 
	   variable_name = plotname &
	   string = (eval("$New_plot_name"))
end

var set var=hello real=(eval(abs))
! -----------
! Create Plot
! -----------
xy_plot template create plot=(eval("."//plotname)) &
   title = (eval("$New_plot_name")) &
   auto_subtitle=yes &
   auto_date=yes &
   auto_analysis_name=yes &
   table=no

! -----------------------------
! FLEX-TO-FLEX OR FLEX-TO-SOLID
! -----------------------------
if condition = (eval($contact_obj.type)=="8")
   ! Find i_flex contact nodes
   variable set &
      variable_name = contact_nodes &
      object = (eval(DB_DESCENDANTS(STOO($Analysis//"."//STR_SPLIT($contact_obj,sep_str)[3]//"."//STR_SPLIT($contact_obj.i_flex,sep_str)[3]),"result_set",1,1 )))
   variable set &
      variable_name = node_count &
      integer = (eval(len(contact_nodes)))
	  
   ! Add Curves
   xy_plot curve create curve=(eval("."//plotname//".total_force")) &
      create_page=no &
      calculate_axis_limits=no &
      y_expression=(eval(node_count//"*"//$contact_obj//".stiffness*abs("//contact_nodes[1]//".penetration.depth)**"//$contact_obj//".exponent-"//node_count//"*"//"STEP(abs("//contact_nodes[1]//".penetration.depth),0,0,"//$contact_obj//".dmax,"//$contact_obj//".damping)*"//contact_nodes[1]//".penetration.velocity")) &
      x_expression=(eval($Analysis.TIME)) &
      y_units = "force" &
      x_units = "time"
   plotcurve3d curve modify curve=(eval("."//plotname//".total_force")) legend="total_force"
   xy_plot curve create curve=(eval("."//plotname//".stiffness_force")) &
      create_page=no &
      calculate_axis_limits=no &
      y_expression=(eval(node_count//"*"//$contact_obj//".stiffness*abs("//contact_nodes[1]//".penetration.depth)**"//$contact_obj//".exponent")) &
      x_expression=(eval($Analysis.TIME)) &
      y_units = "force" &
      x_units = "time"
   plotcurve3d curve modify curve=(eval("."//plotname//".stiffness_force")) legend="stiffness_force"
   xy_plot curve create curve=(eval("."//plotname//".damping_force")) &
      create_page=no &
      calculate_axis_limits=no &
      y_expression=(eval(node_count//"*"//"-STEP(abs("//contact_nodes[1]//".penetration.depth),0,0,"//$contact_obj//".dmax,"//$contact_obj//".damping)*"//contact_nodes[1]//".penetration.velocity")) &
      x_expression=(eval($Analysis.TIME)) &
      y_units = "force" &
      x_units = "time"
   plotcurve3d curve modify curve=(eval("."//plotname//".damping_force")) legend="damping_force"
   
   variable delete &
      variable_name = contact_nodes
   
   variable delete &
      variable_name = node_count

! --------------
! SOLID-TO-SOLID
! --------------
elseif condition = (eval($contact_obj.type)=="0")
   ! Add Curves
   xy_plot curve create curve=(eval("."//plotname//".total_force")) &
      create_page=no &
      calculate_axis_limits=no &
      y_expression=(eval($contact_obj//".stiffness*ABS("//$Analysis//"."//STR_SPLIT($contact_obj,sep_str)[3]//".TRACK_1.Penetration.Depth)**"//$contact_obj//".exponent-STEP(abs("//$Analysis//"."//STR_SPLIT($contact_obj,sep_str)[3]//".TRACK_1.Penetration.Depth),0,0,"//$contact_obj//".dmax,"//$contact_obj//".damping)*"//$Analysis//"."//STR_SPLIT($contact_obj,sep_str)[3]//".TRACK_1.Penetration.velocity")) &
      x_expression=(eval($Analysis.TIME)) &
      y_units = "force" &
      x_units = "time"
   plotcurve3d curve modify curve=(eval("."//plotname//".total_force")) legend="total_force"
   xy_plot curve create curve=(eval("."//plotname//".stiffness_force")) &
      create_page=no &
      calculate_axis_limits=no &
      y_expression=(eval($contact_obj//".stiffness*(-1*"//$Analysis//"."//STR_SPLIT($contact_obj,sep_str)[3]//".TRACK_1.Penetration.Depth)**"//$contact_obj//".exponent")) &
      x_expression=(eval($Analysis.TIME)) &
      y_units = "force" &
      x_units = "time"
   plotcurve3d curve modify curve=(eval("."//plotname//".stiffness_force")) legend="stiffness_force"
   xy_plot curve create curve=(eval("."//plotname//".damping_force")) &
      create_page=no &
      calculate_axis_limits=no &
      y_expression=(eval("-1*STEP(abs("//$Analysis//"."//STR_SPLIT($contact_obj,sep_str)[3]//".TRACK_1.Penetration.Depth),0,0,"//$contact_obj//".dmax,"//$contact_obj//".damping)*"//$Analysis//"."//STR_SPLIT($contact_obj,sep_str)[3]//".TRACK_1.Penetration.velocity")) &
      x_expression=(eval($Analysis.TIME)) &
      y_units = "force" &
      x_units = "time"
   plotcurve3d curve modify curve=(eval("."//plotname//".damping_force")) legend="damping_force"   
   
   variable delete &
      variable_name = contact_nodes
   
   variable delete &
      variable_name = node_count
end
 
! -----------
! Format Plot
! -----------
xy_plots template &
   auto_zoom &
   plot_name=(eval("."//plotname))
   
xy_plot template &
   calculate_axis_limits &
   plot_name=(eval("."//plotname))
   
   

