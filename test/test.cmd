!$contact_obj:t=contact:C=1
!$Analysis:t=analysis:C=1
!$New_plot_name: t=string: C=1: D=advanced_contact_plot

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
      integer = (eval(rows(contact_nodes)))
	  
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
   
   

