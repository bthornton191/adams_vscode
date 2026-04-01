! =============================================================================
! lsp_demo.cmd — MSC Adams CMD LSP Feature Demonstration
! =============================================================================
!
! Open this file in VS Code with the MSC Adams extension active.
! Squiggly underlines show live diagnostics from the Adams CMD language server.
!
! Each section is labelled with the rule code it demonstrates.
!   CLEAN  — no diagnostic produced
!   BROKEN — the listed diagnostic code IS produced (hover for details)
!
! Rules demonstrated:
!   E001  Unknown command
!   E002  Invalid argument name
!   E003  Duplicate argument
!   E004  Invalid enum value
!   E005  Missing required argument (non-object)
!   W005  Missing auto-named object argument (warning, not error)
!   I006  Manual adams_id assignment (info)
!   E006  Mutually-exclusive arguments both supplied
!   E101  Unbalanced parentheses
!   E102  Unclosed string quote
!   E104  Unbalanced control-flow block (if/end, for/end, else without if)
!   W201  Type mismatch — wrong object type for argument
!   I202  Unresolved object reference
!
! Language features demonstrated:
!   Abbreviation  command/argument prefix matching
!   Continuation  trailing '&' joins the next logical line
!   NOT operator  '!' inside parentheses is logical NOT, not a comment
!   != operator   '!=' inside parentheses is inequality, not a comment
! =============================================================================


! =============================================================================
! SETUP — objects created here populate the symbol table used by W201 / I202.
! These statements should produce no diagnostics.
! =============================================================================

model create model_name=.demo_model

part create rigid_body name_and_position  &
   part_name=.demo_model.GROUND  &
   location=0,0,0

marker create  &
   marker_name=.demo_model.GROUND.MAR_1  &
   location=0,0,0

marker create  &
   marker_name=.demo_model.GROUND.MAR_2  &
   location=100,0,0

part create rigid_body name_and_position  &
   part_name=.demo_model.PART_1  &
   location=100,0,0

marker create  &
   marker_name=.demo_model.PART_1.MAR_1  &
   location=100,0,0


! =============================================================================
! E001 — Unknown command
! =============================================================================

! CLEAN: full command name — no E001
model create model_name=.demo_e001_clean

! CLEAN: abbreviated command — 'mar cre' resolves to 'marker create' — no E001
mar cre marker_name=.demo_model.GROUND.MAR_3 location=50,0,0

! CLEAN: comments and blank lines are never treated as commands

! BROKEN: 'xyz_not_a_real_command' does not exist in the schema — E001
xyz_not_a_real_command model_name=.demo_model


! =============================================================================
! E002 — Invalid argument name
! =============================================================================

! CLEAN: all argument names are valid for 'model create'
model create model_name=.demo_e002_clean

! CLEAN: abbreviated argument name — 'model_n' resolves to 'model_name' — no E002
model create model_n=.demo_e002_abbrev

! BROKEN: 'not_a_real_arg' is not a valid argument for 'model create' — E002
model create model_name=.demo_e002_bad not_a_real_arg=value


! =============================================================================
! E003 — Duplicate argument
! =============================================================================

! CLEAN: each argument appears exactly once
model create model_name=.demo_e003_clean

! BROKEN: 'model_name' supplied twice — E003
model create model_name=.demo_dup_a model_name=.demo_dup_b

! BROKEN: two different abbreviations that both resolve to 'model_name' — E003
model create model_n=.demo_dup_c model_na=.demo_dup_d


! =============================================================================
! E004 — Invalid enum value
! =============================================================================

! CLEAN: 'merge' is a valid value for the duplicate_parts enum
model merge  &
   model_name=.demo_model  &
   into_model_name=.demo_model  &
   duplicate_parts=merge

! CLEAN: 'rename' is the other valid value
model merge  &
   model_name=.demo_model  &
   into_model_name=.demo_model  &
   duplicate_parts=rename

! CLEAN: runtime expression ($var) is not validated at lint time — no E004
model merge  &
   model_name=.demo_model  &
   into_model_name=.demo_model  &
   duplicate_parts=$my_mode_variable

! BROKEN: 'overwrite' is not in the allowed set {merge, rename} — E004
model merge  &
   model_name=.demo_model  &
   into_model_name=.demo_model  &
   duplicate_parts=overwrite


! =============================================================================
! E005 — Missing required argument (non-object-name type)
! W005 — Missing auto-named object-name argument (NDBWD_* type)
! =============================================================================

! CLEAN: all required arguments present for 'model merge'
model merge  &
   model_name=.demo_model  &
   into_model_name=.demo_model

! CLEAN: marker_name provided — no W005
marker create  &
   marker_name=.demo_model.GROUND.MAR_4  &
   location=0,50,0

! CLEAN: adams_id omitted — auto-assignment is preferred, no diagnostic produced
marker create  &
   marker_name=.demo_model.GROUND.MAR_5  &
   location=0,100,0

! WARNING W005: marker_name omitted — Adams will auto-name it, but explicit is preferred
marker create location=0,150,0

! ERROR E005: 'model_name' is a required argument for 'model merge' — E005 when omitted
model merge into_model_name=.demo_model


! =============================================================================
! I006 — Manual adams_id assignment (informational)
! =============================================================================

! CLEAN: no adams_id — Adams auto-assigns; no diagnostic produced
marker create  &
   marker_name=.demo_model.GROUND.MAR_6  &
   location=200,0,0

! INFO I006: explicit adams_id supplied — valid but auto-assign is the preferred practice
marker create  &
   marker_name=.demo_model.GROUND.MAR_7  &
   adams_id=42  &
   location=200,50,0


! =============================================================================
! E006 — Mutually-exclusive arguments both supplied
! =============================================================================

! CLEAN: only one member of exclusive group 2 (orientation variants)
marker create  &
   marker_name=.demo_model.GROUND.MAR_8  &
   orientation=0,0,0

! CLEAN: a different single member of the same exclusive group
marker create  &
   marker_name=.demo_model.GROUND.MAR_9  &
   along_axis_orientation=1,0,0

! BROKEN: 'orientation' and 'along_axis_orientation' are in the same exclusive
!         group — only one may be specified — E006
marker create  &
   marker_name=.demo_model.GROUND.MAR_10  &
   orientation=0,0,0  &
   along_axis_orientation=1,0,0


! =============================================================================
! E101 — Unbalanced parentheses
! =============================================================================

! CLEAN: balanced parentheses in a runtime expression
variable set variable_name=a real_value=(eval(abs(1.0)))

! CLEAN: multi-level nested parens — fully balanced
variable set variable_name=b real_value=  &
   (eval(abs(-5.0)))

! CLEAN: parentheses inside a double-quoted string are ignored
model create model_name=.demo_e101_str title="(this paren is inside a string)"

! CLEAN: parentheses inside a single-quoted string are ignored
variable set variable_name=c string_value='(not a real open paren)'

! BROKEN: one '(' opened but never closed — E101
model create model_name=(unclosed

! Note: extra closing ')' also triggers E101. Because the extra ')' confuses
!       the argument parser it may additionally produce E001 or other codes.


! =============================================================================
! E102 — Unclosed string quote
! =============================================================================

! CLEAN: double-quoted string properly closed
model create model_name=.demo_e102_clean title="My Demo Model"

! CLEAN: single-quoted string properly closed
variable set variable_name=sep string_value='.'

! =============================================================================
! E104 — Control-flow balance (if/end, for/end, else without if)
! =============================================================================

! CLEAN: simple if / end
if condition=(1 > 0)
  model create model_name=.demo_if_clean
end

! CLEAN: if / else / end
if condition=(1 > 0)
  model create model_name=.demo_ifelse_a
else
  model create model_name=.demo_ifelse_b
end

! CLEAN: nested if / end
if condition=(1 > 0)
  if condition=(2 > 1)
    model create model_name=.demo_nested_clean
  end
end

! CLEAN: for / end loop
for variable_name=i from=1 to=3
  model create model_name=.demo_for_clean
end

! BROKEN: 'else' with no preceding 'if' — E104
else

! BROKEN: 'end' with no preceding 'if', 'for', or 'while' — E104
end

! BROKEN: 'for' loop opened but never closed with 'end' — E104 (at end of file)
for variable_name=j from=1 to=5
  model create model_name=.demo_for_bad


! =============================================================================
! W201 — Type mismatch (wrong object type supplied for an argument)
! =============================================================================

! CLEAN: reference_marker_name receives a Marker (created in SETUP)
marker create  &
   marker_name=.demo_model.PART_1.MAR_2  &
   reference_marker_name=.demo_model.GROUND.MAR_1

! BROKEN: '.demo_model.PART_1' is a Part, but reference_marker_name expects
!         a Marker — W201
marker create  &
   marker_name=.demo_model.PART_1.MAR_3  &
   reference_marker_name=.demo_model.PART_1


! =============================================================================
! I202 — Unresolved object reference
! =============================================================================

! CLEAN: reference_marker_name points to a Marker defined in the SETUP section
marker create  &
   marker_name=.demo_model.PART_1.MAR_4  &
   reference_marker_name=.demo_model.GROUND.MAR_2

! BROKEN: '.demo_model.GROUND.NONEXISTENT' was never created — I202
marker create  &
   marker_name=.demo_model.PART_1.MAR_5  &
   reference_marker_name=.demo_model.GROUND.NONEXISTENT


! =============================================================================
! CONTINUATION LINES — trailing '&' joins the next logical line before linting
! =============================================================================

! CLEAN: multi-line command; all continuation lines joined before linting
part create rigid_body name_and_position  &
   part_name=.demo_model.PART_2  &
   location=0,200,0  &
   orientation=0,0,0

! CLEAN: inline comment on a continuation line — stripped before joining
marker create  &
   marker_name=.demo_model.PART_2.MAR_1  &   ! inline comment is fine here
   location=0,200,0


! =============================================================================
! '!' OPERATOR EDGE CASES
! Inside parentheses, '!' is a logical NOT operator, not a comment.
! The linter correctly handles all forms without false E101 diagnostics.
! =============================================================================

! CLEAN: '!' as logical NOT inside parentheses — NOT a comment, no E101
if condition=(eval(!DB_EXISTS(".demo_model.PART_1")))
  model create model_name=.demo_not_op
end

! CLEAN: '!=' inequality operator inside parentheses — no E101
variable set variable_name=pitch real_value=5.0
if condition=(eval($pitch != 0))
  model create model_name=.demo_neq_op
end

! CLEAN: '&&' followed by '!' inside nested parens — no false E101 or
!        false line-continuation (the '&&' is inside parens, not trailing '&')
if condition=((eval("yes" == "yes") && !DB_EXISTS(".demo_model.NEW_PART")))
  model create model_name=.demo_and_not
end

! CLEAN: '!' that comes AFTER all closing parens IS a comment (correct)
if condition=(eval(DB_EXISTS(".demo_model"))) ! this is a real inline comment
  model create model_name=.demo_comment_after
end

! CLEAN: '!!' inside a single-quoted string — not a comment, no E101
variable set variable_name=msg string_value=(eval(str_print('HELLO WORLD!!')))

! =============================================================================
! W103 — DANGLING CONTINUATION '&' CASES
! A trailing '&' at the end of a complete command, or at end-of-file,
! causes Adams to silently merge the next command into the same statement.
! The linter reports W103 to catch these errors before running in Adams.
! =============================================================================

! CLEAN: normal multi-line continuation — '&' followed by the continuation of
!        the SAME command.  No W103, no E001.
part create rigid_body name_and_position &
  part_name = .demo_model.PART_W103_CLEAN &
  location = 0.0, 0.0, 0.0 &
  orientation = 0.0, 0.0, 0.0

! BROKEN: trailing '&' at the end of a complete command causes the NEXT
!         command to merge into it.  Adams sees one long unknown command.
!         W103 is emitted; E001 is suppressed.
model create model_name = .demo_model_a &
model create model_name = .demo_model_b

! BROKEN: trailing '&' at end of file — the continuation is never resolved.
!         Adams would silently ignore this, but it almost certainly signals
!         an accidental extra '&' or a missing continuation line.
!         W103 is emitted.
model create model_name = .demo_model_eof &


var set var=$_self.py_str str=(eval($_self.py_str)), (eval("mod = Adams.Models['" // $_self.model.object_value.name // "']"))