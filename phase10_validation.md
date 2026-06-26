# Phase 10 Validation

## Query: What is SPAposition?
```text
==================================================
            ACIS CODE ASSISTANT
==================================================

Query

What is SPAposition?

Context Reached Llm

```text
[GRAPH CONTEXT]
Entity
Class
SPAPOSITION_ARRAY

Documentation
SPAposition array.

Inherits
- ACIS_OBJECT

Returned By
- operator=


--------------------------------------------------

Entity
Class
SPAposition_cloud

Documentation
SPAposition_cloud is a class for geometrically querying large sets of points. The querying is handled through the select methods. The cloud is organized into subclouds: each subcloud knows its box and how to get to its points. The select methods provide an interface for querying through the subclouds. The SPAposition_cloud_iterator class allows access to batches of points from this cloud.

Inherits
- ACIS_OBJECT

Methods
- read_position_cloud_from_file
- read_position_cloud_from_file
- read_position_cloud_from_stl_file

Returned By
- get_Scm_Position_Cloud
- get_bin
- operator=


--------------------------------------------------

Entity
Function
SPAposition

Documentation
C++ initialize constructor requests memory for this object and populates it with the data supplied as arguments.
Role: Creates a SPAposition using the x, y, z coordinates.
@param xi x-coordinate value.
@param yi y-coordinate value.
@param zi z-coordinate value.

Used As Parameter
- api_make_flat_on_faces
- find_cross_curve
- api_slice_of_model
- cur_snap_data
- cur_snap_data
- set_position
- SPAnvector
- api_make_polygon
- epd_output
- rotate
- process
- process
- process
- point_perp
- point_perp
- closest_point
- closest_point
- point_perp
- point_perp
- evaluateP_P
- point_perp
- point_perp
- closest_point
- closest_point
- point_perp
- point_perp
- transform
- transform_inverse
- point_perp
- sphere_cylinder_intersect
- sphere_cylinder_intersect
- api_tweak_faces
- api_tweak_faces
- api_taper_faces
- api_taper_faces
- api_edge_taper_faces
- api_edge_taper_faces
- api_shadow_taper_faces
- api_shadow_taper_faces
- api_move_faces
- api_move_faces
- api_offset_faces
- api_offset_faces
- api_offset_faces_specific
- api_offset_faces_specific
- api_offset_body
- api_offset_body
- api_sweep_more
- api_sweep_more
- api_tweak_extend_faces
- api_tweak_extend_faces
- api_tweak_faces_init
- api_tweak_faces_init
- set_apoint
- vector_law
- bend_law
- unbend_law
- api_set_view_phlv5_computer
- api_set_view_phlv5_computer
- api_create_hatch_lines
- splitSegment
- api_remove_and_repair_body
- api_remove_and_repair_body
- api_remove_faces
- api_remove_faces
- set_view
- set_view
- api_rh_set_view
- api_rh_set_view
- api_hollow_body
- api_hollow_body
- api_hollow_body_specific
- api_hollow_body_specific
- api_sheet_thicken
- api_sheet_thicken
- api_offset_faces_make_sheet
- api_offset_faces_make_sheet
- constrain_surface_data2
- constrain_surface_data
- constrain_surface_data
- sg_calculate_surface_normal_dervs
- trim_guide_curve
- trim_guide_curve
- point_perp
- point_perp

Returns
- void


--------------------------------------------------

Entity
Function
find_candidates

Documentation
the SPAposition if any do.

Returns
- tree_list


--------------------------------------------------

Entity
Function
bounded_point

Documentation
point from a SPAposition

Returns
- class DECL_KERN


--------------------------------------------------

Entity
Function
view_spec

Documentation
SPAposition which anchors the view

Returns
- class DECL_INTR


--------------------------------------------------

Entity
Function
dbpos

Documentation
debug a SPAposition

Returns
- void


--------------------------------------------------

Entity
Function
coords

Documentation
Returns the coordinates of this APOINT as an SPAposition .

Used As Parameter
- triangle
- triangle
- triangle

Returns
- SPAposition


--------------------------------------------------

Entity
Function
mark

Documentation
Return the current SPAposition in the

Returns
- long


--------------------------------------------------

Entity
Function
NODE

Documentation
Basic constructor (from a SPAposition).

Returns
- void


[QUESTION]
What is SPAposition?

[INSTRUCTIONS]
Query Intent: Definition

Using ONLY the supplied Knowledge Graph context, summarize the retrieved documentation.
If a section cannot be supported by the retrieved documentation, omit that section entirely.
Preferred Adaptive Layout (if supported by evidence):

Definition



Purpose



Graph Relationships



Related Components

Answer ONLY using the supplied graph context.
Treat Graph Relationships as first-class evidence.
If relationship information exists, incorporate it naturally into the explanation.
Do not invent relationships.
Do not infer missing graph edges.
If a relationship section is empty, omit it.
Every factual statement must be traceable to the supplied graph context.
Never use generic AI filler like "It is important for geometry."

```

Knowledge Graph Evidence

Primary Match

Class

SPAPOSITION_ARRAY

Inherits

ACIS_OBJECT

Returned By

operator=()

Returned By : 1

Related Classes

SPAposition_cloud

Related Functions

SPAposition()

find_candidates()

bounded_point()

view_spec()

dbpos()

coords()

mark()

NODE()

==================================================
```

## Query: What is ENTITY?
```text
==================================================
            ACIS CODE ASSISTANT
==================================================

Query

What is ENTITY?

Context Reached Llm

```text
[GRAPH CONTEXT]
Entity
Function
ENTITY

Returns
- class DECL_KERN


--------------------------------------------------

Entity
Function
entity

Documentation
The entity the blend is running along in contact with.

Returns
- ENTITY


--------------------------------------------------

Entity
Function
SetEntityColor

Documentation
The ENTITY to display

Returns
- outcome


--------------------------------------------------

Entity
Method
Entity

Documentation
rtn: ptr to Surf_mesh (INDEXED_MESH *)

Returns
- void

Owning Class
- DS_dmod


--------------------------------------------------

Entity
Class
HH_Node

Documentation
ENTITY

Inherits
- ATTRIB_HH

Inherited By
- HH_GlobalNode

Returned By
- first_vertex
- second_vertex


--------------------------------------------------

Entity
Class
HH_GNode

Documentation
ENTITY

Inherits
- ATTRIB_HH

Inherited By
- HH_SurfSnap

Returned By
- get_root_node
- root
- node


--------------------------------------------------

Entity
Class
HH_Arc

Documentation
ENTITY

Inherits
- ATTRIB_HH

Inherited By
- HH_GlobalArc

Returned By
- create


--------------------------------------------------

Entity
Function
lose

Documentation
entities.

Returns
- void


--------------------------------------------------

Entity
Function
get_ent

Documentation
Gets ENTITY .

Returns
- ENTITY


--------------------------------------------------

Entity
Function
api_dm_remove_dm_attributes

Documentation
from an entity

Returns
- outcome


[QUESTION]
What is ENTITY?

[INSTRUCTIONS]
Query Intent: Definition

Using ONLY the supplied Knowledge Graph context, summarize the retrieved documentation.
If a section cannot be supported by the retrieved documentation, omit that section entirely.
Preferred Adaptive Layout (if supported by evidence):

Definition



Purpose



Graph Relationships



Related Components

Answer ONLY using the supplied graph context.
Treat Graph Relationships as first-class evidence.
If relationship information exists, incorporate it naturally into the explanation.
Do not invent relationships.
Do not infer missing graph edges.
If a relationship section is empty, omit it.
Every factual statement must be traceable to the supplied graph context.
Never use generic AI filler like "It is important for geometry."

```

Knowledge Graph Evidence

Primary Match

Function

ENTITY()

Returns

class DECL_KERN

Related Functions

entity()

SetEntityColor()

lose()

get_ent()

api_dm_remove_dm_attributes()

Related Methods

Entity()

Related Classes

HH_Node

HH_GNode

HH_Arc

==================================================
```

## Query: How does variable radius blending work?
```text
==================================================
            ACIS CODE ASSISTANT
==================================================

Query

How does variable radius blending work?

Context Reached Llm

```text
[GRAPH CONTEXT]
Entity
Function
radius

Documentation
or elliptical blend.

Returns
- double


--------------------------------------------------

Entity
Function
var_blend_spl_sur

Documentation
Create a surface-surface variable radius blend.

Returns
- class DECL_KERN


--------------------------------------------------

Entity
Function
on_support

Documentation
Provided for variable radius blending only.

Returns
- point_support_containment


--------------------------------------------------

Entity
Function
limit_extension_var_rad

Documentation
extending variable radius blend surfaces.

Returns
- void


--------------------------------------------------

Entity
Function
on_support

Documentation
edge. Provided for variable radius blending only.

Returns
- point_support_containment


--------------------------------------------------

Entity
Function
api_blend_edges_pos_rad

Documentation
Applies a variable radius blend on the list of edges, simplifying the blend for ends with constant blend radius.
Role: This API function substitutes for several calls to API functions which create a calibration curve and a radius object, apply the variable radius attribute, and, finally, fix the blend. In addition to facilitating the development and tracking of memory clean-up, this API function attempts to simplify the blend by substituting the variable radius attribute with the constant radius blend for the edges, within which the radius function is constant. If an attempt of simplification fails, this API function performs the regular variable radius blending. The first four arguments (list of edges to blend, number of position-radius pairs, position and radius arrays) are required. Positions (specified in the global coordinate system) are projected on the calibration curve, composed of the given edges, to find the calibration curve parameter values, corresponding to the given radii. The last two arguments, start_slope and end_slope , are optional and make sense only for open calibration curves. They specify the derivative of the radius function with respect to the parameter along the calibration curve. Their value is interpreted as the slope (dR/dp) of the radius function vs. parameter along the calibration curve: 0 = horizontal 1 = 45 degrees NULL = "unspecified" As the parameter speed is set arbitrarily (or, more accurately, depending on the first edge in the sequence), only zero slope value is independent of parameter speed and is safe and meaningful. If there are features lying inside the support region that is replaced by blend, then blending attempts to retain those features. This behavior can be controlled by the option bl_retain_features . However, if blending fails to retain such features then it would continue to give a result ignoring them. A sys_warning is raised when blending detects features but unable to retain them.
Effect: Changes model
Journal: Available
Product(s): 3D ACIS Modeler
@param eds edges to blend.
@param num_fixes number of pairs.
@param fix_positions array of positions.
@param fix_radii array of radii.
@param start_slope starting slope value.
@param end_slope ending slope value.
@param ao ACIS options such as versioning and journaling.

Returns
- outcome


--------------------------------------------------

Entity
Function
copy

Documentation
Copies a variable radius.

Returns
- var_radius


--------------------------------------------------

Entity
Function
copy

Documentation
Copies a variable radius.

Returns
- var_radius


--------------------------------------------------

Entity
Function
copy

Documentation
Copies a variable radius.

Returns
- var_radius


--------------------------------------------------

Entity
Class
ATTRIB_VAR_BLEND

Documentation
Defines the blend attribute for variable radius blends.
@see SPAinterval, CURVE, EDGE

Inherits
- ATTRIB_FFBLEND


[QUESTION]
How does variable radius blending work?

[INSTRUCTIONS]
Query Intent: Functional Explanation

Using ONLY the supplied Knowledge Graph context, summarize the retrieved documentation.
If a section cannot be supported by the retrieved documentation, omit that section entirely.
Preferred Adaptive Layout (if supported by evidence):

Overview



Execution Flow



Key Functions



Supporting Classes

Answer ONLY using the supplied graph context.
Treat Graph Relationships as first-class evidence.
If relationship information exists, incorporate it naturally into the explanation.
Do not invent relationships.
Do not infer missing graph edges.
If a relationship section is empty, omit it.
Every factual statement must be traceable to the supplied graph context.
Never use generic AI filler like "It is important for geometry."

```

Knowledge Graph Evidence

Primary Match

Function

radius()

Returns

double

Related Functions

var_blend_spl_sur()

on_support()

limit_extension_var_rad()

api_blend_edges_pos_rad()

copy()

Related Classes

ATTRIB_VAR_BLEND

==================================================
```

## Query: Which classes inherit ENTITY?
```text
==================================================
            ACIS CODE ASSISTANT
==================================================

Query

Which classes inherit ENTITY?

Context Reached Llm

```text
[GRAPH CONTEXT]
Entity
Method
Entity

Documentation
rtn: ptr to Surf_mesh (INDEXED_MESH *)

Returns
- void

Owning Class
- DS_dmod


--------------------------------------------------

Entity
Function
ENTITY

Returns
- class DECL_KERN


--------------------------------------------------

Entity
Function
entity

Documentation
The entity the blend is running along in contact with.

Returns
- ENTITY


--------------------------------------------------

Entity
Function
read

Documentation
derived classes.

Returns
- size_t


--------------------------------------------------

Entity
Function
dbentkids

Documentation
debug ENTITY and children

Returns
- void


--------------------------------------------------

Entity
Class
ADM_draw_engine

Documentation
Overrides the base class for the drawing engine.
Role: This class implements the abstract draw primitive interface between the ADM icons and the view controller.

Inherits
- DM_draw_engine

Inherited By
- ADM_gidraw_engine
- ADMHOOPS_draw_engine

Returned By
- Spatial_cast
- operator=
- Spatial_cast


--------------------------------------------------

Entity
Method
get_CATError

Documentation
Reuse parent class constructors

Returns
- thisClass

Owning Class
- ThrowSmartPtr


--------------------------------------------------

Entity
Method
Set_nrows

Documentation
eff: access method for derived classes

Returns
- void

Owning Class
- DS_abs_matrix


--------------------------------------------------

Entity
Method
Set_nclms

Documentation
eff: access method for derived classes

Returns
- void

Owning Class
- DS_abs_matrix


--------------------------------------------------

Entity
Method
Set_size

Documentation
eff: access method for derived classes

Returns
- void

Owning Class
- DS_abs_matrix


[QUESTION]
Which classes inherit ENTITY?

[INSTRUCTIONS]
Query Intent: Relationship

Using ONLY the supplied Knowledge Graph context, summarize the retrieved documentation.
If a section cannot be supported by the retrieved documentation, omit that section entirely.
Preferred Adaptive Layout (if supported by evidence):

Summary



Relationship Tree



Related Entities

Answer ONLY using the supplied graph context.
Treat Graph Relationships as first-class evidence.
If relationship information exists, incorporate it naturally into the explanation.
Do not invent relationships.
Do not infer missing graph edges.
If a relationship section is empty, omit it.
Every factual statement must be traceable to the supplied graph context.
Never use generic AI filler like "It is important for geometry."

```

Knowledge Graph Evidence

Primary Match

Method

Entity()

Returns

void

Owning Class

DS_dmod

Related Functions

ENTITY()

entity()

read()

dbentkids()

Related Classes

ADM_draw_engine

Related Methods

get_CATError()

Set_nrows()

Set_nclms()

Set_size()

==================================================
```

## Query: What returns outcome?
```text
==================================================
            ACIS CODE ASSISTANT
==================================================

Query

What returns outcome?

Context Reached Llm

```text
[GRAPH CONTEXT]


[QUESTION]
What returns outcome?

[INSTRUCTIONS]
Query Intent: Relationship

Using ONLY the supplied Knowledge Graph context, summarize the retrieved documentation.
If a section cannot be supported by the retrieved documentation, omit that section entirely.
Preferred Adaptive Layout (if supported by evidence):

Summary



Relationship Tree



Related Entities

Answer ONLY using the supplied graph context.
Treat Graph Relationships as first-class evidence.
If relationship information exists, incorporate it naturally into the explanation.
Do not invent relationships.
Do not infer missing graph edges.
If a relationship section is empty, omit it.
Every factual statement must be traceable to the supplied graph context.
Never use generic AI filler like "It is important for geometry."

```

Knowledge Graph Evidence

Primary Match

Class

outcome

Inherits

ACIS_OBJECT

Returned By

api_initialize_booleans()
api_terminate_booleans()
api_boolean()
api_boolean()
api_imprint()
api_intersect()
api_slice()
api_slice()
api_subtract()
api_unite()
api_imprint()
api_intersect()
api_subtract()
api_unite()
api_boolean_chop_body()
api_boolean_chop_body()
api_imprint_shadow_edges()
api_planar_slice()
api_planar_slice()
api_scribe()
api_uncover_face()
api_remove_wire_edge()
api_remove_face()
api_unhook_wire_edge()
api_unhook_face()
api_unhook_faces()
api_fafa_int()
api_edfa_int()
api_fafa_int()
api_edfa_int()
api_embed_wire_in_faces()
api_boolean_glue()
api_boolean_glue()
api_boolean_chop_complete()
api_boolean_chop_complete()
api_boolean_start()
api_update_intersection()
api_fixup_intersection()
api_selectively_intersect()
api_selectively_intersect()
api_bool_make_intersection_graph()
api_bool_make_intersection_graph()
api_imprint_complete()
api_slice_complete()
api_complete_intersection_graph()
api_imprint_stitch_complete()
api_boolean_complete()
api_boolean_complete()
api_selectively_imprint()
api_selectively_imprint()
api_regularise_entity()
api_clean_entity()
api_clean_list_of_entities()
api_clean_wire()
api_check_entity_ff_ints()
api_check_list_ff_ints()
api_merge_faces()
api_merge_seam_edges()
api_set_no_merge_attrib()
api_remove_no_merge_attrib()
api_join_edges()
api_stitch()
api_imprint_stitch()
api_imprint_stitch()
api_unite_wires()
api_project_edge_to_face()
api_project_wire_to_body()
api_slice_of_model()
api_clean_body()
check_tags_validity()
merge_child_state()
celltop_attach()
celltop_remove()
celltop_expand()
celltop_flatten()
api_fix_check_problems()
set_fixed_distance_chamfers()
api_initialize_clearance()
api_terminate_clearance()
api_check_solid_clearance()
api_check_face_clearance()
abh_set_adv_chamfers()
abh_set_const_chamfers()
abh_chamfer_edges()
copy_single_entity()
api_initialize_covering()
api_terminate_covering()
api_cover_circuits()
api_cover_sheet()
api_cover_wire()
api_cover_wires()
api_cover_circuits()
api_cover_sheet()
api_cover_wire()
api_cover_wires()
api_cover_planar_edges()
api_cover_planar_wires()
api_combine_edges()
api_heal_edges_to_regions()
api_heal_edges_to_regions()
api_unite_edges()
api_cover_wire_loops()
create_line_2pt()
create_line_tangent()
create_arc_center_radius()
create_arc_3pt()
create_arc_center_edge()
create_arc_diagonal()
create_ellipse()
create_spline_curve()
create_spline_curve2()
create_bezier_curve()
curve_arc_3curve()
modify_line()
modify_ellipse()
edge_to_spline()
api_initialize_constructors()
api_terminate_constructors()
api_body()
api_make_cuboid()
api_solid_block()
api_make_sphere()
api_solid_sphere()
api_make_frustum()
api_solid_cylinder_cone()
api_make_torus()
api_solid_torus()
api_make_prism()
api_make_pyramid()
api_wiggle()
api_make_spline()
api_sheet_from_ff()
api_make_ewire()
api_make_ewires()
api_make_ewires()
api_make_polygon()
api_make_wire()
api_face_plane()
api_make_plface()
api_make_planar_disk()
api_face_sphere()
api_make_spface()
api_face_conic()
api_face_cylinder_cone()
api_make_cnface()
api_face_torus()
api_make_trface()
api_face_law()
api_face_spl_ctrlpts()
api_mk_fa_spl_ctrlpts()
api_face_spl_apprx()
api_mk_fa_spl_fit()
api_face_spl_intrp()
api_mk_fa_spl_intp()
api_make_approx_surface()
api_curve_line()
api_curve_line_tangent()
api_mk_ed_line()
api_curve_arc()
api_curve_arc_3pt()
api_curve_arc_center_edge()
api_curve_arc_diagonal()
api_curve_arc_3curve()
api_curve_fillet()
api_curve_ellipse()
api_mk_ed_ellipse()
api_mk_ed_conic()
api_edge_helix()
api_edge_spiral()
api_edge_spiral()
api_edge_spring()
api_edge_spring_taper()
api_edge_spring_law()
api_edge_law()
api_curve_law()
api_edge_plaw()
api_curve_bezier()
api_mk_ed_int_ctrlpts()
api_mk_ed_cubic()
api_curve_spline()
api_curve_spline2()
api_curve_spline2_periodic()
api_edge()
api_edge_arclength_param()
api_edge_arclength_param()
api_trans_edge()
api_make_edge_from_curve()
api_mk_ed_bs3_curve()
api_split_curve()
api_split_edge_at_disc()
api_ed_inters_to_ents()
api_edge_to_spline()
api_make_approx_curve()
api_create_point()
api_create_text()
api_mk_by_faces()
api_build_wire()
api_make_kwire()
api_make_wire()
api_reverse_body()
api_reverse_wire()
api_body_to_1d()
api_body_to_2d()
api_reverse_wire()
api_reverse_face()
api_enclose_void()
api_accurate_bs3_approximation()
api_reset_bs3_approximation()
api_orient_wire()
api_set_pcurve_tightness()
api_modify_line()
api_modify_ellipse()
api_trim_curve()
api_trim_middle()
api_trim_2curves()
api_trim_chain()
api_fillet_vertex()
api_chamfer_wire_vertex()
api_closed_wire()
api_closed_wire()
api_closed_wire()
api_find_face()
api_find_vertex()
api_wire_to_chain()
api_edge_arclength_metric()
api_loop_external()
api_manifold_class()
api_q_edges_around_vertex()
api_shell_external()
api_wire_len()
api_wire_len()
api_compute_pcurve_tightness()
api_set_edge_tightness()
api_simplify_pcurve()
api_set_coedge_tightness()
api_edge_approx_line_arc()
api_compute_points_segments()
api_make_wire_from_points_segments()
api_fit_plane()
api_fit_line()
api_initialize_cellular_topology()
api_terminate_cellular_topology()
api_ct_add_to_group()
api_ct_attach_cells()
api_ct_cell_area()
api_ct_cell_mass_pr()
api_ct_copy_cell()
api_ct_expand_cells()
api_ct_flatten_cells()
api_ct_lose_cells()
api_ct_lose_group()
api_ct_make_group()
api_ct_point_in_cell()
api_ct_propagate_cface_attribs()
api_ct_remove_from_group()
api_ct_return_ents()
api_ct_return_groups()
api_ct_vacate_cell()
api_ct_get_all_cells()
api_get_faces_from_all_entities()
api_get_edges_from_all_entities()
api_get_vertices_from_all_entities()
api_ct_attach()
api_ct_expand()
api_ct_flatten()
api_ct_remove()
api_check_ct()
api_ct_merge_cells()
api_copy_entity_contents()
api_body_mass_pr()
api_body_mass_pr()
api_ray_test_body()
api_ray_test_ents()
api_raytest_body()
api_raytest_ents()
api_stitch()
api_pierce_sheet()
api_rsw_face_path()
api_rsw_face_vec()
api_rsw_wire_path()
api_rsw_wire_path()
api_rsw_wire_vec()
api_rsw_wire_vec()
api_sw_chain_axis()
api_sw_chain_axis()
api_sw_chain_path()
api_sw_chain_path_options()
api_sw_chain_surface()
api_sw_chain_surface()
api_sw_chain_vec()
api_sw_chain_vec()
api_sw_chain_wire()
api_sw_chain_wire()
api_sw_face_axis()
api_sw_face_norm()
api_sw_face_surface()
api_sw_face_vec()
api_sw_face_wire()
api_sw_face_wire()
api_sw_wire_axis_sol()
api_sw_wire_axis_sol()
api_simplify_body()
api_simplify_face()
api_dm_get_attrib_dm2acis()
api_dm_rm_multi_face()
api_dm_add_link()
api_initialize_deformable_modeling()
api_terminate_deformable_modeling()
api_dm_get_attrib_dm2acis()
api_dm_query_attrib_dm2acis()
api_dm_query_attrib_dm2acis()
api_dm_commit_attrib_dm2acis()
api_dm_remove_dm_attributes()
api_dm_remove_attrib_dm2acis()
api_dm_add_patch()
api_dm_rm_patch()
api_dm_add_multi_face()
api_dm_rm_multi_face()
api_dm_add_link()
api_dm_set_tolerance()
api_dm_use_link_cstrns()
api_dm_auto_elevate()
api_dm_set_array_size()
api_dm_journal_on()
api_dm_journal_play()
api_dm_journal_play()
api_dm_journal_off()
api_dm_get_hierarchy_entities()
adm_disable_legacy_domain_scaling()
DS_build_test_spline_face()
DS_build_test_spline_edge()
api_move_edge()
api_move_edge()
api_simplify_entity()
api_initialize_euler_ops()
api_terminate_euler_ops()
api_combine_body()
api_separate_body()
api_expand_body()
api_expand_body()
api_flatten_body()
api_unshare_body_geometry()
api_unstitch_nonmani()
api_unstitch_nonmani()
api_split_face()
api_convert_to_spline()
api_convert_to_spline()
api_get_facet_edge_points()
api_get_facet_face_tri_points()
api_reset_entity_refinement()
api_get_sequential_mesh()
api_delete_entity_facets()
facet_unfaceted_faces()
initialize_facetter()
api_initialize_generic_attributes()
api_terminate_generic_attributes()
api_add_generic_named_attribute()
api_add_generic_named_attribute()
api_add_generic_named_attribute()
api_add_generic_named_attribute()
api_add_generic_named_attribute()
api_add_generic_named_attribute()
api_add_generic_named_attribute()
api_add_generic_named_attribute()
api_find_named_attribute()
api_remove_generic_named_attribute()
asmi_component_set_name()
asmi_component_find_name()
asmi_component_get_name()
PickScreenPosition()
PickEntity()
PickFaces()
PickAsmEntities()
PickAsmFaces()
PickAsmEdges()
PickAsmVertices()
PickEntityFromRay()
TempRenderEntity()
RefreshActive()
HighlightEntity()
HighlightComponentEntity()
GetHighlight()
SetHighlightColor()
SetHighlightColor()
GetHighlightColor()
SetActiveWCSColor()
GetActiveWCSColor()
SetEntityColor()
EraseModel()
EraseEntity()
DisplayEntity()
SetEntityColor()
GetEntityColor()
GetDefaultColor()
GetDefaultFaceColor()
GetDefaultEdgeColor()
GetDefaultVertexColor()
GetDefaultBackGroundColor()
SetDefaultColor()
SetDefaultFaceColor()
SetDefaultEdgeColor()
SetDefaultVertexColor()
SetDefaultBackGroundColor()
IsDisplayed()
get_entity_box()
api_initialize_healing()
api_terminate_healing()
api_tighten_gaps()
api_tighten_gaps()
api_hh_init_body_for_healing()
api_hh_end_body_for_healing()
api_hh_auto_heal()
api_hh_simplify_auto()
api_hh_simplify_auto()
api_hh_simplify_analyze()
api_hh_simplify_analyze()
api_hh_simplify_calculate()
api_hh_simplify_fix()
api_hh_simplify_cleanup()
api_hh_force_simplify_to_cylinder()
api_hh_force_simplify_to_cone()
api_hh_force_simplify_to_plane()
api_hh_force_simplify_to_sphere()
api_hh_force_simplify_to_torus()
api_hh_stitch_auto()
api_hh_stitch_analyze()
api_hh_stitch_calculate()
api_hh_stitch_fix()
api_hh_stitch_cleanup()
api_hh_geombuild_auto()
api_hh_geombuild_analyze()
api_hh_geombuild_calc_fix()
api_hh_geombuild_cleanup()
api_hh_geombuild_check()
api_hh_analytic_auto()
api_hh_analytic_analyze()
api_hh_analytic_calc_fix()
api_hh_isospline_auto()
api_hh_isospline_analyze()
api_hh_isospline_calc_fix()
api_hh_sharp_edge_auto()
api_hh_sharp_edge_analyze()
api_hh_sharp_edge_calc_fix()
api_hh_gen_spline_auto()
api_hh_gen_spline_analyze()
api_hh_gen_spline_calc_fix()
api_hh_wrapup_auto()
api_hh_wrapup_analyze()
api_hh_wrapup_calc_fix()
api_hh_preprocess()
api_hh_postprocess()
api_hh_make_tolerant()
api_hh_analyze_vertices()
api_hh_analyze_edges()
api_hh_analyze_coedges()
api_hh_analyze_loops()
api_hh_analyze_faces()
api_hh_analyze_shells()
api_hh_analyze_lumps()
api_hh_analyze_body()
api_hh_get_bad_edges()
api_hh_get_bad_vertices()
api_hh_get_bad_coedges()
api_hh_get_bad_loops()
api_hh_get_bad_faces()
api_hh_get_bad_shells()
api_hh_get_bad_lumps()
api_hh_store_entity_details()
api_hh_get_entity_details()
api_fix_face_coedge_sense()
distributeDeltaState()
checkDeltaForDistribute()
api_initialize_hlc()
api_terminate_hlc()
api_initialize_hlr()
api_terminate_hlr()
api_hedgehog()
api_initialize_interactive_hidden_line()
api_terminate_interactive_hidden_line()
api_ihl_retrieve()
api_ihl_clean()
api_ihl_facet()
api_ihl_get_mesh()
api_ihl_compute()
api_ihl_compute()
api_ihl_compute_entity_silhouette()
api_ihl_set_output_manager()
api_ihl_get_output_manager()
api_ihl_compute_from_meshes()
api_ihl_occlusion()
api_imprint()
api_incr_bool_prepare()
api_initialize_intersectors()
api_terminate_intersectors()
api_point_in_face()
api_point_in_face()
api_crv_self_inters()
api_ed_self_inters()
api_edge_convexity_param()
api_face_nu_nv_isolines()
api_face_u_iso()
api_face_v_iso()
api_facet_curve()
api_inter_ed_ed()
api_intersect_curves()
api_silhouette_edges()
api_silhouette_edges()
api_check_cur_smoothness()
api_check_entity()
api_brep_health_report()
api_check_entity()
api_check_wire_self_inters()
api_check_wire_self_intersects()
api_check_wire_self_inters()
api_check_edge()
api_check_edge()
api_check_face()
api_check_face()
api_entity_extrema()
api_entity_extrema()
api_create_boundary_field()
api_create_boundary_field()
api_create_boundary_field()
api_create_boundary_field()
api_edge_tangent()
api_get_entity_box()
api_get_entity_box()
api_get_entity_box()
api_check_body()
asmi_component_mass_props()
asmi_raytest_ents()
modify_wire()
remove_vertex_wires()
remove_vertex_wires()
remove_vertex_wire()
collapse_degenerate_wires()
collapse_degenerate_wires()
sg_merge_coedges()
remove_vertex_from_wire()
remove_cvty_pts_from_stitched_lateral_edge()
api_initialize_kernel()
api_terminate_kernel()
api_checking()
api_logging()
api_set_stream_logging()
api_get_stream_logging()
api_start_modeller()
api_stop_modeller()
api_set_int_option()
api_set_dbl_option()
api_set_str_option()
api_add_state()
api_change_state()
api_merge_states()
api_delete_ds()
api_note_state()
api_get_file_info()
api_set_file_info()
api_restore_entity_list()
api_save_entity_list()
api_restore_entity_list_file()
api_save_entity_list_file()
api_save_version()
api_get_save_version()
api_remove_state()
api_roll_n_states()
api_change_to_state()
api_distribute_state_to_streams()
api_find_named_state()
api_name_state()
api_prune_history()
api_ensure_empty_root_state()
api_get_history_size()
api_prune_following()
api_get_modified_faces()
api_get_modified_entities()
api_get_refacet_faces()
api_get_active_entities()
api_get_all_user_attributes()
api_make_root_state()
api_restore_entity_list_with_history()
api_restore_entity_list_with_history_file()
api_restore_history()
api_restore_history_file()
api_save_entity_list_with_history()
api_save_entity_list_with_history_file()
api_save_history()
api_save_history_file()
api_apply_transf()
api_change_body_trans()
api_remove_transf()
api_copy_body()
api_copy_entity()
api_copy_entity_list()
api_deep_copy_entity()
api_deep_down_copy_entity()
api_deep_copy_entity_list()
api_test_deep_copy()
api_test_deep_down_copy()
api_down_copy_entity()
api_delent()
api_del_entity()
api_del_entity_list()
api_wcs_create()
api_wcs_set_active()
api_wcs_get_active()
api_get_owner()
api_get_curve_ends()
api_get_ellipse_parameters()
api_get_lumps()
api_get_shells()
api_get_faces()
api_get_loops()
api_get_wires()
api_get_edges()
api_get_coedges()
api_get_vertices()
api_get_tedges()
api_get_tcoedges()
api_get_tvertices()
api_get_entities()
api_str_to_law()
api_integrate_law()
api_integrate_law_wrt()
api_integrate_law_wrt_and_splits()
api_ndifferentiate_law()
api_nroots_of_law()
api_nmax_of_law()
api_nmin_of_law()
api_nsolve_laws()
api_make_rails()
api_law_to_entity()
api_transform_entity()
api_extract_coed_info()
api_make_VBL_output_surfaces()
api_stackmon_limit()
api_check_face_loops()
api_loop_type()
api_calculate_edge_tolerance()
api_calculate_vertex_tolerance()
api_update_tolerance()
api_find_annotations()
api_hook_annotations()
api_unhook_annotations()
api_clear_annotations()
api_make_linear()
api_make_cubic()
api_make_quintic()
api_make_polynomial_law()
api_reset_boxes()
api_project_curve_to_surface()
api_project_curve_to_surface()
api_save_state()
api_load_state()
api_create_history()
api_set_default_history()
api_get_default_history()
api_delete_history()
api_get_history_from_entity()
api_get_active_state()
api_query_state_validity()
api_get_state_from_id()
api_get_state_id()
api_get_entity_from_id()
api_get_entity_id()
api_check_histories()
api_abort_state()
api_get_version_tag()
api_get_version_tag()
api_get_version_tag()
api_make_version_object()
api_make_version_object()
api_make_version_object()
api_minimize_entities()
api_set_default_minimize_options()
api_make_face_from_surface()
api_make_face_spline()
api_return_collection_ents()
api_return_collections()
api_add_to_collection()
api_remove_from_collection()
api_delete_collection_entities()
api_share_geometry()
api_share_geometry()
api_clear_geometry_sharing_info()
api_get_spaentity_id()
api_get_entity_from_spaentity_id()
api_get_faces()
api_get_edges()
api_get_owner_transf()
api_get_acis_version()
api_pm_load_part()
for_tvertex()
api_local_remove()
makeWires()
alignWires()
breakupWires()
minimizeTwist()
simplifyWires()
smoothWires()
buildEdges()
buildFaces()
createBody()
modifyWire()
addVertex()
removeVertex()
collapseWires()
setLoftingOptions()
getOptions()
reenterLoftConnectedCoedgeList()
estimateMinRadOfCurvature()
loseSurfaceConditions()
sections()
estimateTanfacScale()
setTangentFactors()
getTangentFactors()
ownLaws()
replaceSurfaceWithLaws()
postProcessStitch()
makePointCurves()
losePointCurves()
api_initialize_lopt_ops()
api_terminate_lopt_ops()
api_initialize_local_ops()
api_terminate_local_ops()
api_tweak_faces()
api_tweak_faces()
api_tweak_faces()
api_tweak_to_body()
api_tweak_to_body()
api_tweak_open_circuits()
api_taper_faces()
api_taper_faces()
api_edge_taper_faces()
api_edge_taper_faces()
api_shadow_taper_faces()
api_shadow_taper_faces()
api_move_faces()
api_move_faces()
api_offset_faces()
api_offset_faces()
api_offset_faces_specific()
api_offset_faces_specific()
api_offset_body()
api_offset_body()
api_tweak_fix_edge()
api_tweak_fix_edge()
api_tweak_fix_vertex()
api_tweak_fix_vertex()
api_sweep_more()
api_sweep_more()
api_tweak_extend_faces()
api_tweak_extend_faces()
api_tweak_faces_init()
api_tweak_faces_init()
api_tweak_pick_edge_solution()
api_tweak_query_edge_solutions()
api_remove_lop_attribs()
api_extend_sheetbody()
api_tweak_replace_face()
api_tweak_tighten_edge()
api_detect_protrusion()
api_detect_depression()
set_NO_MERGE_ATTRIB()
remove_NO_MERGE_ATTRIB()
asmi_save_model_contents()
asmi_restore_model_list()
asmi_model_get_box()
asmi_set_entity_color()
asmi_get_entity_color()
asmi_model_get_root_element()
api_stitch_make_input()
api_stitch_preview()
api_stitch_manage_coins()
api_stitch()
api_stitch_query()
api_n_body_unite()
api_n_body_unite_2d()
api_initialize_offsetting()
api_terminate_offsetting()
api_offset_face()
api_offset_face()
api_offset_face_edge()
api_offset_planar_wire()
api_offset_planar_wire()
api_offset_planar_wire()
api_offset_planar_wire()
api_offset_face_loops()
api_offset_face_loops()
api_offset_edges_on_faces()
api_offset_edges_on_faces()
api_offset_edges_on_faces()
api_offset_edges_on_faces()
api_wire_area()
api_wire_area()
get_Scm_Outcome()
load()
load()
load()
save()
save()
save()
save()
save_selection()
fixup_part_ids()
part_remove_entity()
api_initialize_part_manager()
api_terminate_part_manager()
api_part_create()
api_part_delete()
api_part_set_distribution_mode()
api_part_get_distribution_mode()
api_part_add_entity()
api_part_remove_entity()
api_part_lookup_entity()
api_part_entity_id()
api_part_entities()
api_part_save()
api_part_load()
api_part_start_state()
api_part_note_state()
api_part_name_state()
api_part_roll_to_state()
api_part_roll_n_states()
api_part_delete_all_states()
pm_remove_entity()
api_pattern_create_on_curve()
api_pattern_create_cylindrical()
api_pattern_create_cylindrical()
api_pattern_create_on_edge()
api_pattern_create_on_edge()
api_pattern_create_on_edge()
api_pattern_create_elliptical()
api_pattern_create_hex_cylindrical()
api_pattern_create_hex_cylindrical()
api_pattern_create_hex()
api_pattern_create_linear()
api_pattern_create_polar_grid()
api_pattern_create_radial()
api_pattern_create_random()
api_pattern_create_spherical()
api_pattern_create_on_surface()
api_pattern_create_on_surface()
api_pattern_modify_filter_alternating()
api_pattern_modify_scale_alternating()
api_pattern_modify_scale_alternating()
api_pattern_modify_scale_linear()
api_pattern_modify_scale_linear()
api_pattern_modify_filter_periodic()
api_pattern_modify_scale_periodic()
api_pattern_modify_scale_periodic()
api_pattern_modify_filter_random()
api_pattern_modify_offset_random()
api_pattern_modify_orient_random()
api_pattern_modify_scale_random()
api_pattern_modify_scale_random()
api_pattern_find_bump()
api_pattern_query_transformations()
api_pattern_modify_element_remove()
api_pattern_modify_element_remove()
api_pattern_modify_element_restore()
api_pattern_modify_element_restore()
api_pattern_modify_element_transform()
api_pattern_modify_element_transform()
api_pattern_modify_element_scale()
api_pattern_modify_element_scale()
api_pattern_modify_element_scale()
api_pattern_modify_element_scale()
api_pattern_modify_transform()
api_pattern_modify_mirror()
api_pattern_modify_reflect()
api_pattern_modify_compose()
api_pattern_modify_concatenate()
api_pattern_modify_concatenate()
api_pattern_create_from_list()
api_pattern_create_from_list()
api_pattern_create_from_list()
api_pattern_create_from_laws()
api_pattern_copy()
api_pattern_destroy()
api_pattern_modify_filter()
api_pattern_modify_scale()
api_pattern_modify_root_transformation()
api_pattern_query_root_transformation()
api_pattern_query_size()
api_pattern_query_coordinate_dimension()
api_pattern_query_coordinates()
api_pattern_query_element_indices()
api_pattern_to_entity()
api_curve_pattern()
api_cylindrical_pattern()
api_cylindrical_pattern()
api_edge_pattern()
api_edge_pattern()
api_edge_pattern()
api_elliptical_pattern()
api_hex_cylindrical_pattern()
api_hex_cylindrical_pattern()
api_hex_pattern()
api_linear_pattern()
api_polar_grid_pattern()
api_radial_pattern()
api_random_pattern()
api_spherical_pattern()
api_surface_pattern()
api_surface_pattern()
api_alternating_keep_pattern()
api_alternating_scale_pattern()
api_alternating_scale_pattern()
api_linear_scale_pattern()
api_linear_scale_pattern()
api_periodic_keep_pattern()
api_periodic_scale_pattern()
api_periodic_scale_pattern()
api_random_keep_pattern()
api_random_offset_pattern()
api_random_orient_pattern()
api_random_scale_pattern()
api_random_scale_pattern()
api_remove_pattern()
api_get_pattern_transfs()
api_initialize_hidden_line_removal()
api_terminate_hidden_line_removal()
api_phlv5_compute()
api_phlv5_compute()
api_asm_model_phlv5_compute()
api_phlv5_clean()
api_phlv5_retrieve()
api_build_phlv5_computer()
api_add_bodies_phlv5_computer()
api_set_view_phlv5_computer()
api_compute_view_phlv5_computer()
api_delete_phlv5_computer()
api_create_hatch_lines()
api_create_hatch_lines()
api_create_hlr_input_handle()
api_add_asm_model_to_hlr_handle()
api_add_bodies_to_hlr_handle()
api_compute_hlr_view()
api_cleanup_hlr_input_handle()
PreProcessBody()
api_initialize_persistent_id()
api_terminate_persistent_id()
api_pidset()
api_pidget()
api_pidrem()
api_pm_create_part()
api_pm_delete_part()
api_pm_add_entity()
api_pm_remove_entity()
api_pm_lookup_entity()
api_pm_entity_id()
api_pm_part_entities()
api_pm_save_part()
api_pm_load_part()
api_pm_start_state()
api_pm_note_state()
api_pm_name_state()
api_pm_roll_to_state()
api_pm_roll_n_states()
api_pm_delete_all_states()
api_process_mt()
api_process_mt()
api_initialize_query()
api_terminate_query()
api_edent_rel()
api_ptent_rel()
api_point_in_body()
api_get_ents()
api_ray_fire()
api_ray_fire()
api_ray_fire()
api_entity_entity_distance()
api_entity_entity_distance()
api_entity_point_distance()
api_entity_point_distance()
api_entity_point_distance()
api_entity_point_distance()
api_entity_entity_touch()
api_find_cls_ptto_face()
api_body_mass_props()
api_ent_area()
api_planar_face_pr()
api_clash_bodies()
api_clash_bodies()
api_n_body_clash()
api_n_body_clash()
api_clash_faces()
api_clash_faces()
api_detect_match()
for_bodies()
api_detect_match()
api_initialize_rbi()
api_terminate_rbi()
api_repair_body_self_ints()
api_remove_and_repair_body()
api_pattern_update_entities()
api_pattern_apply_to_entity()
api_pattern_apply_to_entity()
api_pattern_apply_to_faces()
api_initialize_face_removal()
api_terminate_face_removal()
api_remove_faces()
api_remove_faces()
api_remove_wire_edges()
api_remove_open_gap()
api_remove_open_gap()
api_remove_edges()
initialize_vf()
terminate_vf()
render_model_vf()
get_render_scenes_vf()
delete_render_scene_contents_vf()
highlight_model_element_vf()
highlight_render_scene_element_vf()
hide_render_scene_element_vf()
initialize()
terminate()
render_model()
get_render_scenes()
delete_render_scene_contents()
highlight_model_element()
highlight_render_scene_element()
hide_render_scene_element()
api_repair_planar_slices()
asmi_component_set_color()
asmi_component_find_color()
asmi_component_remove_color()
asmi_component_has_color_modifications()
asmi_component_set_transparency()
asmi_component_find_transparency()
asmi_component_has_material_modifications()
set_clipping_planes()
api_initialize_rendering()
api_terminate_rendering()
api_rh_initialise()
api_rh_terminate()
api_rh_set_render_mode()
api_rh_get_render_mode()
api_rh_set_control_variable()
api_rh_get_control_variable()
api_rh_set_output_mode()
api_rh_get_output_mode()
api_rh_render_entities()
api_rh_initialise_supl_shaders()
api_rh_create_material()
api_rh_copy_material()
api_rh_delete_material()
api_rh_set_color_comp()
api_rh_get_color_comp()
api_rh_set_transp_comp()
api_rh_get_transp_comp()
api_rh_set_transp_status()
api_rh_get_transp_status()
api_rh_set_reflect_status()
api_rh_get_reflect_status()
api_rh_set_reflect_comp()
api_rh_get_reflect_comp()
api_rh_set_displace_comp()
api_rh_get_displace_comp()
api_rh_set_displace_status()
api_rh_get_displace_status()
api_rh_get_color_comp_list()
api_rh_get_transp_comp_list()
api_rh_get_reflect_comp_list()
api_rh_get_displace_comp_list()
api_rh_set_color_arg()
api_rh_set_transp_arg()
api_rh_set_reflect_arg()
api_rh_set_displace_arg()
api_rh_def_color_comp()
api_rh_def_transp_comp()
api_rh_def_reflect_comp()
api_rh_def_displace_comp()
api_rh_create_light()
api_rh_copy_light()
api_rh_delete_light()
api_rh_get_light_types()
api_rh_create_light_shadow()
api_rh_delete_light_shadow()
api_rh_set_light_list()
api_rh_get_light_list()
api_rh_get_light_args()
api_rh_set_light_arg()
api_rh_get_light_state()
api_rh_set_light_state()
api_rh_get_background_types()
api_rh_create_background()
api_rh_copy_background()
api_rh_delete_background()
api_rh_set_background()
api_rh_get_background()
api_rh_get_background_args()
api_rh_set_background_arg()
api_rh_get_foreground_types()
api_rh_create_foreground()
api_rh_copy_foreground()
api_rh_delete_foreground()
api_rh_set_foreground()
api_rh_get_foreground()
api_rh_get_foreground_args()
api_rh_set_foreground_arg()
api_rh_get_texture_space_types()
api_rh_create_texture_space()
api_rh_copy_texture_space()
api_rh_delete_texture_space()
api_rh_get_texture_space_args()
api_rh_set_texture_space_arg()
api_rh_render_cube_environment()
api_rh_delete_environment_map()
api_rh_set_environment_map()
api_rh_get_environment_map()
api_rh_create_cube_environment()
api_rh_set_material()
api_rh_get_material()
api_rh_set_texture_space()
api_rh_get_texture_space()
api_rh_get_material_color()
api_rh_get_material_color()
api_rh_get_material_reflection()
api_rh_get_material_transp()
api_rh_get_material_texture()
api_rh_set_material_color()
api_rh_set_material_reflection()
api_rh_set_material_transp()
api_rh_set_material_texture()
api_rh_set_sidedness()
api_rh_get_sidedness()
api_rh_render_std_entities()
api_rh_set_std_material()
api_rh_get_std_material()
api_rh_set_std_light()
api_rh_get_std_light()
api_rh_set_std_background()
api_rh_get_std_background()
api_rh_set_view()
api_rh_set_clipping()
api_rh_set_resolution()
api_rh_set_sub_image()
api_rh_get_view()
api_rh_get_clipping()
api_rh_get_resolution()
api_rh_get_sub_image()
api_rh_initialise_image_utilities()
api_rh_terminate_image_utilities()
api_rh_set_conversion_method()
api_rh_set_conversion_colour_map()
api_rh_convert_image_start()
api_rh_convert_image_end()
api_rh_convert_rgb_scanline()
api_rh_convert_rgb_float_scanline()
api_rh_read_lightworks_image_size()
api_rh_read_lightworks_image()
api_rh_display_image()
api_rh_set_entity_rgb()
api_rh_get_entity_rgb()
api_rh_set_default_rgb()
api_rh_get_default_rgb()
api_rh_set_default_background_rgb()
api_rh_get_default_background_rgb()
api_rh_set_default_face_rgb()
api_rh_get_default_face_rgb()
api_rh_set_default_edge_rgb()
api_rh_get_default_edge_rgb()
api_rh_set_default_vertex_rgb()
api_rh_get_default_vertex_rgb()
api_rh_set_highlight_rgb()
api_rh_get_highlight_rgb()
rough_align_entity_to_points()
rough_align_entity_to_points()
api_equal_turning_samples_from_edges()
api_sample_edges()
api_selective_boolean_stage1()
api_selective_boolean_stage2()
api_selective_boolean_stage2()
api_create_graph_from_cells()
api_create_graph_from_faces()
api_create_graph_from_edges()
api_boolean_tube_body()
api_subset_graph_with_plane()
api_subgraph_2dcell()
api_subgraph_3dcell()
api_selective_unite()
api_make_shadow()
api_sheet_loop()
api_initialize_shelling()
api_terminate_shelling()
api_hollow_body()
api_hollow_body()
api_hollow_body_specific()
api_hollow_body_specific()
api_sheet_thicken()
api_sheet_thicken()
api_sheet_thicken()
api_offset_faces_make_sheet()
api_offset_faces_make_sheet()
api_make_solid_from_faces()
api_make_solid_from_faces()
api_create_wire_for_miter_faces()
api_make_mid_sheet_body()
api_make_mid_sheet_body()
api_detect_mid_sheet_face_pairs()
api_get_mid_sheet_progenitor_info()
api_cleanup_mid_sheet_progenitor_info()
sg_skin_wires()
sg_skin_wires_path()
sg_skin_wires_ruled()
sg_skin_wires_normal()
sg_skin_wires_vectors()
sg_skin_wires_vectors_guides()
sg_skin_wires_draft_angle()
sg_skin_wires_draft_angle()
sg_skin_wires_guide_curves()
sg_loft_coedges()
sg_loft_coedges()
sg_skin_faces()
sg_loft_faces()
api_initialize_skinning()
api_terminate_skinning()
api_loft_coedges()
api_loft_coedges()
api_loft_coedges()
api_loft_faces()
api_loft_faces()
api_loft_faces()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_wires()
api_skin_faces()
api_skin_faces()
api_net_wires()
api_net_wires()
api_net_sections()
api_create_li()
api_create_li()
api_create_li()
api_create_li()
api_create_si()
api_create_si()
api_create_si()
api_create_si()
api_create_si()
api_create_si()
api_create_si()
api_set_options_li()
api_set_options_li()
api_set_options_si()
api_set_options_si()
api_reenter_coedges_li()
api_make_wires_sli()
api_build_edges_sli()
api_modify_wire_sli()
api_add_vertex_sli()
api_start_vertex_sli()
api_start_vertex_sli()
api_remove_vertex_sli()
api_build_body_sli()
api_collapse_wires_sli()
api_delete_sli()
api_align_wires_sli()
api_valid_start_vertices_sli()
api_breakup_wires_sli()
api_minimize_twist_wires_sli()
api_simplify_wires_sli()
api_build_faces_sli()
api_lose_surface_conditions_li()
api_estimate_tangent_factor_scale_li()
api_set_tangent_factors_li()
api_get_tangent_factors_li()
api_estimate_min_rad_curvature_skin()
api_add_guide_curve_si()
api_add_mapping_curve_sli()
api_remove_mapping_curve_sli()
api_clear_mapping_curves_sli()
api_make_mapping_curves_sli()
api_clear_guide_curves_sli()
api_show_guides_si()
api_move_vertex_sli()
makeWires()
alignWires()
breakupWires()
minimizeTwist()
buildEdges()
buildFaces()
createBody()
modifyWire()
addVertex()
removeVertex()
collapseWires()
setSkinningOptions()
estimateMinRadOfCurvature()
getOptions()
setSkinningPath()
setSkinningNormal()
setSkinningVectorsAndMagnitudes()
setSkinningDraftValues()
simplifyWires()
smoothWires()
sg_order_coedges()
order_coedge_list()
makePointCurves()
losePointCurves()
create_block()
create_solid_block()
create_solid_cyl_cone()
create_solid_sphere()
create_solid_torus()
calculate_solid_mass_properties()
api_slice()
api_planar_slice()
api_planar_slice()
api_sliver_entities()
api_detect_short_edges()
api_replace_edge_with_tvertex()
api_replace_face_with_tedge()
api_detect_sliver_faces()
api_remove_zero_length_edge()
api_bs3_curve_from_chain()
api_3dpm_create_cadsurf_session()
api_3dpm_create_cadsurf_session()
api_3dpm_create_cadsurf_session()
api_3dpm_create_cleaner_session()
api_3dpm_create_hexa_session()
api_3dpm_create_hybrid_session()
api_3dpm_create_hybrid_cfd_session()
api_3dpm_create_tetra_session()
api_3dpm_create_tetra_hpc_session()
api_3dpm_compute_mesh()
api_3dpm_update_sizemap()
api_3dpm_update_mesh()
api_3dpm_create_volume_assoc()
api_3dpm_load_mesh()
api_3dpm_save_mesh()
api_initialize_3dpm_bridge()
api_terminate_3dpm_bridge()
api_entity_point_distance()
api_entity_point_distance()
api_spring_back()
api_split_periodic_faces()
api_split_edges_at_poles()
api_split_face_at_disc()
api_split_wire_edges()
api_subdivide_face()
api_initialize_spline()
api_terminate_spline()
api_initialize_stitching()
api_terminate_stitching()
api_stitch()
api_stitch_nonmanifold()
stch_tolerize_entities()
makeWires()
alignWires()
breakupWires()
minimizeTwist()
buildEdges()
buildFaces()
createBody()
postProcessStitch()
modifyWire()
addVertex()
removeVertex()
collapseWires()
setStartVertex()
setStartVertex()
setWireFixed()
setWireUnFixed()
validStartVertices()
estimateMinRadOfCurvature()
simplifyWires()
clearMappingCurves()
addGuide()
addGuide()
clearGuides()
getGuides()
setOptions()
addGuide()
makeVirtualGuideCurves()
api_initialize_sweeping()
api_terminate_sweeping()
api_sweep_with_options()
api_sweep_with_options()
api_sweep_with_options()
api_sweep_with_options()
api_project_wire()
api_offset_planar_face_loops()
api_extrude_planar_faces()
api_make_sweep_twist_rail()
api_make_sweep_path()
sweep_wire_along_vector()
sweep_face_along_vector()
sweep_wire_about_axis()
sweep_face_about_axis()
sweep_rigid()
sweep_along_vector()
sweep_about_axis()
sweep_along_path()
sweep_with_twist()
api_check_and_fix_tedge()
api_replace_edge_with_tedge()
api_replace_vertex_with_tvertex()
api_replace_tedge_with_edge()
api_replace_tvertex_with_vertex()
api_optimize_tvertex_tolerance()
api_check_edge_errors()
api_check_vertex_errors()
api_tolerize_entity()
api_unfold()
api_unfold()
api_va_initialize()
api_va_terminate()
api_va_create_surface_mesh()
api_va_generate_tessellation_mesh()
api_va_generate_tessellation_mesh()
api_va_generate_surface_mesh()
api_va_generate_surface_mesh()
api_va_generate_tet_mesh()
api_va_generate_subset_surface_mesh()
api_va_generate_hybrid_mesh()
api_va_generate_hybrid_mesh()
api_va_generate_surface_mesh()
api_va_generate_tet_mesh()
api_va_generate_hybrid_mesh()
api_va_generate_tet_mesh()
api_va_generate_tet_mesh()
api_va_create_tet_mesh()
api_va_delete_mesh()
api_va_set_refinement()
api_va_refine()
api_va_set_entity_size_control()
api_va_set_non_persistent_entities()
api_va_set_non_subdividable_entities()
api_va_set_non_defeaturable_entities()
api_va_get_node_count()
api_va_get_node_positions()
api_va_get_element_count()
api_va_get_element_data()
api_va_get_edge_nodes()
api_va_get_face_nodes()
api_va_get_faceter_refinement()
api_va_get_elements()
api_va_get_nodes()
api_va_get_entity()
api_va_get_entity()
api_va_get_entity()
api_va_get_entity()
api_va_get_node_entities()
api_va_get_mesh_options()
api_va_export_mesh()
api_va_check_mesh()
api_va_set_integer_meshing_parameter()
api_va_set_double_meshing_parameter()
api_va_get_vki_handles()
api_va_get_vki_handles()
api_va_get_vki_handles()
api_vha_initialize()
api_vha_terminate()
api_vha_render_mesh()
api_vha_render_mesh()
api_initialize_warp()
api_terminate_warp()
api_space_warp()
api_bend_entity()
api_rebend_entity()
api_bend_to_curve_entity()
api_twist_entity()
api_bulge_entity()
api_stretch_entity()
api_warp_entity_slice()
imprint_plane()
wcs_create()
wcs_create()
wcs_set_origin()
api_arc_len_samples_from_edges()
create_wire_from_edge_list()
get_curves_from_wires()
copy_solid_edge_ent()
api_wrap()
api_measure_wall_thickness_polyhedra()
api_segment_polyhedra_body()
api_polyhedra_decimate()
api_facet_body()
api_initialize_advanced_blending()
api_terminate_advanced_blending()
api_set_abh_blends()
api_set_ee_cr_blend()
api_set_ee_cr_blend()
api_set_ee_vr_blend()
api_set_inst_blend()
api_abh_edge_offset()
api_make_radius_constant()
api_make_radius_two_ends()
api_make_radius_fixed_width()
api_make_radius_rnd_chamfer()
api_make_radius_rot_ellipse()
api_make_radius_pos_rads()
api_make_radius_pos_rads()
api_make_radius_param_rads()
api_make_radius_param_rads_tan()
api_make_radius_spline_rad()
api_make_radius_holdline()
api_abh_edge_project()
api_abh_vblend()
api_abh_vblend()
api_abh_chamfer_edges()
api_blend_edges_pos_rad()
api_blend_holdline()
api_blend_holdline_face_face()
api_blend_three_ent()
api_set_cc_blend()
set_edge_blends()
api_find_and_remove_features()
api_find_and_remove_features()
api_initialize_defeature()
api_terminate_defeature()
set_pause_after_recognize()
set_recognize_blends()
set_recognize_blends()
set_blends_max_radius()
set_blends_max_radius()
set_blends_num_curvature_samples()
set_blends_num_curvature_samples()
set_recognize_chamfers()
set_recognize_chamfers()
set_chamfers_max_width()
set_chamfers_max_width()
set_recognize_holes()
set_recognize_holes()
set_hole_max_diameter()
set_hole_max_diameter()
set_blend_supports_max_angle()
set_blend_supports_max_angle()
set_chamfer_supports_max_angle()
set_chamfer_supports_max_angle()
set_chamfer_support_width_ratio()
set_recognize_sphericalholes()
set_recognize_sphericalholes()
get_feature()
get_failed_feature()
api_get_journal()
api_start_journal()
api_end_journal()
api_pause_journal()
api_resume_journal()
api_set_journal()
api_set_journal_name()
api_set_journal_name()
api_set_acis_options()
api_set_acis_options()
api_set_acis_options()
api_set_version()
api_advanced_cover()
api_advanced_cover()
api_advanced_cover_no_stitch()
api_terminate_admgi_control()
api_initialize_admgi_control()
api_terminate_admgi_draweng()
api_initialize_admgi_draweng()
api_terminate_admhoops()
api_initialize_admhoops()
api_terminate_admicon()
api_initialize_admicon()
api_initialize_faceter()
api_terminate_faceter()
api_set_mesh_manager()
api_get_mesh_manager()
api_create_refinement()
api_set_entity_refinement()
api_get_entity_refinement()
api_set_default_refinement()
api_get_default_refinement()
api_facet_entity()
api_facet_entities()
api_facet_bodies()
api_delete_entity_facets()
api_mark_faceted_faces()
api_create_vertex_template()
api_modify_vertex_template()
api_get_entity_vertex_template()
api_set_entity_vertex_template()
api_set_default_vertex_template()
api_get_default_vertex_template()
api_faceted_face()
api_get_body_facets()
api_get_lump_facets()
api_get_shell_facets()
api_get_face_facets()
api_get_indexed_mesh()
api_get_facet_edge_points()
api_set_auto_clipping()
api_fast_find_face()
api_fast_find_face()
api_facet_area()
api_facet_curve()
api_facet_curve()
api_facet_edge()
api_facet_edge()
api_delete_all_AF_POINTs()
api_set_mesh_manager_to_default()
make_af_points_from_param_list()
clear_annotations_from_curr_bb()
operator=()
api_create_polyhedra_body()
api_create_polyhedra_mesh()
api_create_polyhedra_body()
api_initialize_polyhedra()
api_terminate_polyhedra()
api_get_default_cgm_container()
api_polyhedra_get_mesh()
api_polyhedra_get_mesh()
api_align()
api_align()
api_approx()
wire_2d()
wire_3d()
api_convex_hull()
api_convex_hull()
api_create_global_mesh()
api_create_global_meshes()
api_create_global_mesh()
api_approx()
api_approx()
api_model_comparison()
api_offset_edges_on_faces()
api_sample_faces()
api_void_volume()
api_wrap_wire()
asmi_model_create()
asmi_model_create()
asmi_model_create_for_translation()
asmi_model_create_for_export()
asmi_model_create_assembly()
api_asm_assembly_get_owning_model()
asmi_model_del_assembly()
asmi_model_has_assembly()
asmi_model_get_entity_mgr()
asmi_model_get_entities()
asmi_model_get_entities()
asmi_model_get_info()
asmi_model_get_components()
asmi_model_get_sub_models()
asmi_get_models_which_share_history()
asmi_save_model_list()
asmi_save_model_list()
asmi_save_model_atomic()
asmi_restore_model_list()
asmi_restore_model_list()
asmi_set_entity_mgr_factory()
asmi_get_entity_mgr_factory()
asmi_model_add_model_ref()
asmi_model_add_model_ref()
asmi_model_remove_model_ref()
asmi_model_get_model_refs()
asmi_model_ref_get_transform()
asmi_model_ref_set_transform()
asmi_model_ref_apply_transform()
asmi_model_ref_get_model()
asmi_model_ref_get_owning_model()
asmi_component_get_sub_components()
asmi_component_get_sub_components()
asmi_component_get_transform()
asmi_component_get_relative_transform()
asmi_component_get_entities()
asmi_component_get_component_entities()
asmi_component_get_box()
asmi_component_get_path()
asmi_component_get_root_model()
asmi_component_get_parent()
asmi_component_get_unmodified_model()
asmi_component_get_unmodified_model()
asmi_component_is_model_modified()
api_asm_model_get_entity_handle()
api_asm_model_get_entity_handle()
api_asm_entity_handle_get_ptr()
asmi_model_get_component_handle()
asmi_model_get_component_handle()
asmi_model_get_component_handle()
asmi_model_get_component_handle()
asmi_model_get_component_handle()
asmi_model_get_component_entity_handle()
asmi_component_entity_handle_decompose()
asmi_check_model()
api_asm_prune_assembly_history()
asmi_entity_handle_list_get_live_entities()
asmi_model_save_entities()
asmi_cleanup()
asmi_model_cleanup()
asmi_model_cleanup()
asmi_model_cleanup_tree()
asmi_cleanup_handles()
asmi_model_cleanup_handles()
asmi_model_cleanup_handles()
asmi_cleanup_models()
asmi_model_cleanup_model()
asmi_model_cleanup_model()
api_asm_component_add_property()
api_asm_component_has_property()
asmi_component_suppress()
asmi_component_is_suppressed()
asmi_component_unsuppress()
asmi_component_has_physical_modifications()
asmi_component_hide()
asmi_component_is_hidden()
asmi_component_unhide()
asmi_component_has_hiding_modifications()
asmi_component_find_property()
asmi_component_find_next_property()
asmi_component_has_property_modifications()
asmi_property_remove()
api_asm_component_get_property_owner()
asmi_component_get_property_owners()
api_asm_model_get_owned_property_owners()
api_asm_model_find_components_with_property()
asmi_flatten_assembly()
api_initialize_blending()
api_terminate_blending()
api_blend_graph()
api_blend_seq()
api_complete_blends()
api_concl_blend_ss()
api_delete_blends()
api_delete_exp_blends()
api_do_one_blend_ss()
api_fix_blends()
api_init_blend_ss()
api_make_blend_cross_curve()
api_make_blend_sheet()
api_make_blend_wire()
api_set_const_chamfers()
api_set_angle_distance_chamfers()
api_set_const_rounds()
api_set_exp_const_chamfer()
api_set_exp_const_round()
api_set_exp_co_ro_ffbl_att()
api_set_exp_co_ro_fbl_att()
api_set_vblend()
api_set_vblend_auto()
api_set_vblend_autoblend()
api_smooth_edge_seq()
api_smooth_edges_to_curve()
api_blend_edges()
api_chamfer_edges()
api_chamfer_vertices()
api_chamfer_vertex()
api_chamfer_vertex()
api_make_flat_on_faces()
api_set_var_blends()
api_preview_blends()
api_detect_blends()
api_detect_chamfers()
api_blend_edge()
api_chamfer_edge()
api_is_blend_face()
api_set_blend_face()
api_get_lost_support()
api_set_lost_support()
vertex_blends()

Used As Parameter

end()
end()
end_entity_creation()
end_entity_creation2()
end_entity_modification()
end_entity_modification2()
api_part_note_state()
api_pm_note_state()
note_delta_state()
note_delta_state_regardless_of_level()
note_delta_state_nd()

Returned By : 1775 | Used As Parameter : 11

Related Functions

append()

GetPointStyle()

check_cvxty()

split_at_kinks()

tangent()

replace_tvertex_with_vertex()

replace_tedge_with_edge()

split_at_convexity_points()

==================================================
```

## Query: Where is BODY used?
```text
==================================================
            ACIS CODE ASSISTANT
==================================================

Query

Where is BODY used?

Context Reached Llm

```text
[GRAPH CONTEXT]
Entity
Class
BODY

Documentation
Represents a wire, sheet, or solid body. If you derive from BODY, the owner() method must still return NULL.
Role: A BODY models a wire, sheet, or solid body. A body may be several disjoint bodies treated as a collection of lumps. Lumps represent solids, sheets, and wires. In a manifold solid, every edge is adjacent to two faces. A nonmanifold solid may have edges that are adjacent to more than two faces. A nonmanifold solid may also have more than one set of faces at a vertex. Edges in a sheet may bound any number of faces. Edges of a wire do not bound any faces. A pure wire body contains wires, edges, coedges, and vertices, but no faces. Wires can represent isolated points, open or closed profiles, and general wireframe models that are unsurfaced, i.e., have no faces. Wires are attached as a component of a shell and are not directly attached to the body. A solid body is represented by the boundary of the region of space that is enclosed by a single lump. The lump is composed of one or more disjoint shells that contain no wires. The geometry of body is given in a local coordinate system. This relates to the universal one by a transformation stored with the body. Functions for traversing the topology are located in query.hxx . These are useful for generating lists of faces, edges, and vertices on other topological entities. Other functions of note include: get_body_box to retrieve or recalculate the bounding box of a body; point_in_body to determine the containment of a point versus a body; and raytest_body to determine the intersections of a ray with a body.
@see LUMP, TRANSFORM, WIRE, LUMP

Inherits
- ENTITY

Returned By
- containing_body
- get_body
- get_body_for_change
- get_body
- get_body_for_change
- tool
- blank
- sg_stitch_lofting_faces
- body
- GetBody
- GetBody
- BodyOfEntity
- BodyOfEdge
- body
- get_projected_wire_body
- make_wire
- make_wire
- make_wire
- make_wire
- unhook_wire
- get_second_body
- wire
- getWireList
- getBody
- get_sweep_to_body
- body
- get_owner_body


--------------------------------------------------

Entity
Function
body

Documentation
Returns a pointer to the containing BODY .

Returns
- ENTITY


--------------------------------------------------

Entity
Function
set_body_for_change

Documentation
should be used for setting the body

Returns
- void


--------------------------------------------------

Entity
Function
body

Documentation
return the BODY pointer

Returns
- ENTITY


--------------------------------------------------

Entity
Function
createBody

Documentation
Creates a body.
@param body body created.

Returns
- outcome


--------------------------------------------------

Entity
Function
get_body_for_change

Documentation
should be for changing the body attributes

Returns
- BODY


--------------------------------------------------

Entity
Function
GetTheBodyTransform

Documentation
Get the BODY transform

Returns
- DECL_WARP


--------------------------------------------------

Entity
Function
used

Returns
- logical


--------------------------------------------------

Entity
Function
operator*

Documentation
body.

Returns
- friend


--------------------------------------------------

Entity
Function
type_name

Documentation
Returns the string "body" .

Returns
- char


[QUESTION]
Where is BODY used?

[INSTRUCTIONS]
Query Intent: Navigation

Using ONLY the supplied Knowledge Graph context, summarize the retrieved documentation.
If a section cannot be supported by the retrieved documentation, omit that section entirely.
Preferred Adaptive Layout (if supported by evidence):

Answer



Location



Related Files



Related Components

Answer ONLY using the supplied graph context.
Treat Graph Relationships as first-class evidence.
If relationship information exists, incorporate it naturally into the explanation.
Do not invent relationships.
Do not infer missing graph edges.
If a relationship section is empty, omit it.
Every factual statement must be traceable to the supplied graph context.
Never use generic AI filler like "It is important for geometry."

```

Knowledge Graph Evidence

Primary Match

Class

BODY

Inherits

ENTITY

Returned By

containing_body()
get_body()
get_body_for_change()
get_body()
get_body_for_change()
tool()
blank()
sg_stitch_lofting_faces()
body()
GetBody()
GetBody()
BodyOfEntity()
BodyOfEdge()
body()
get_projected_wire_body()
make_wire()
make_wire()
make_wire()
make_wire()
unhook_wire()
get_second_body()
wire()
getWireList()
getBody()
get_sweep_to_body()
body()
get_owner_body()

Returned By : 27

Related Functions

body()

set_body_for_change()

createBody()

get_body_for_change()

GetTheBodyTransform()

used()

operator*()

type_name()

==================================================
```
