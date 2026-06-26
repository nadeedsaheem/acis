# Method Collision Report

## Method Overloads Collapsed
The following methods share the same `file_path::class_name::method_name` identifier but have different signatures (overloads). Neo4j MERGE collapsed them into single nodes.

### Class: `SPAposition` | Method: `operator*`
- **File Path:** `include/position.hxx`
- **Overload Count:** 7
- **Signatures:**
  - `operator*(SPAposition const &, double)`
  - `operator*(SPAposition const &, SPAunit_vector const &)`
  - `operator*(SPAunit_vector const &, SPAposition const &)`
  - `operator*(SPAmatrix const &, SPAposition const &)`
  - `operator*(SPAposition const &, SPAmatrix const &)`
  - `operator*(SPAposition const &, SPAtransf const &)`
  - `operator*(SPAposition const &, SPAtransf const *)`

### Class: `CATFillDictionary` | Method: `CATFillDictionary`
- **File Path:** `include/CATFillDictionary.h`
- **Overload Count:** 6
- **Signatures:**
  - `CATFillDictionary(const char *, const char *, CATSysCreationFunc, CATSysConditionFunc_t)`
  - `CATFillDictionary(const GUID &, const CATMetaClass *)`
  - `CATFillDictionary(const CATMetaClass *, const CATMetaClass *, CATSysCreationFunc, CATSysConditionFunc_t, int)`
  - `CATFillDictionary(const char *, _Tz*(* )(_Ty*))`
  - `CATFillDictionary(const char *, const char *, const char *)`
  - `CATFillDictionary(const CATMetaClass *, const CATMetaClass *, const char *, CATSysCreationFunc)`

### Class: `CATFillDictionary` | Method: `Register`
- **File Path:** `include/CATFillDictionary.h`
- **Overload Count:** 6
- **Signatures:**
  - `Register(const char *, const char *, CATSysCreationFunc, CATSysConditionFunc)`
  - `Register(const GUID &, const CATMetaClass *)`
  - `Register(CATMetaClass *, CATMetaClass *, CATSysCreationFunc, CATSysConditionFunc, int)`
  - `Register(const char *, CATSysCreatCommandFunc)`
  - `Register(const char *, const char *, const char *)`
  - `Register(CATMetaClass *, const CATMetaClass *, const char *, CATSysCreationFunc)`

### Class: `DS_abs_vec` | Method: `Assign_into`
- **File Path:** `include/dsabvec.hxx`
- **Overload Count:** 6
- **Signatures:**
  - `Assign_into(DS_multi_banded_vec &, EQ_FLAG)`
  - `Assign_into(DS_multi_banded_vec &, double, EQ_FLAG)`
  - `Assign_into(DS_block_vec &, EQ_FLAG)`
  - `Assign_into(DS_block_vec &, double, EQ_FLAG)`
  - `Assign_into(DS_abcd_vec &, EQ_FLAG)`
  - `Assign_into(DS_abcd_vec &, double, EQ_FLAG)`

### Class: `DS_link_cstrn` | Method: `DS_name`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 6
- **Signatures:**
  - `DS_name(bndry_flag)`
  - `DS_name(bndry_flag)`
  - `DS_name(bndry_flag)`
  - `DS_name(bndry_flag)`
  - `DS_name(bndry_flag)`
  - `DS_name(bndry_flag)`

### Class: `rgb_color` | Method: `rgb_color`
- **File Path:** `include/rgbcolor.hxx`
- **Overload Count:** 5
- **Signatures:**
  - `rgb_color()`
  - `rgb_color(double, double, double)`
  - `rgb_color(double [ 3 ])`
  - `rgb_color(int)`
  - `rgb_color(int)`

### Class: `PARAMARR` | Method: `PARAMARR`
- **File Path:** `include/af_ladut.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `PARAMARR()`
  - `PARAMARR(int, double, unsigned)`
  - `PARAMARR(double *, int, double, unsigned)`
  - `PARAMARR(PARAMARR const &)`

### Class: `rat_bipoly_vec` | Method: `operator*`
- **File Path:** `include/bipoly.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `operator*(rat_bipoly const &, rat_bipoly_vec const &)`
  - `operator*(rat_bipoly const &, rat_bipoly_vec const &)`
  - `operator*(rat_bipoly_vec const &, rat_bipoly const &)`
  - `operator*(rat_bipoly_vec const &, rat_bipoly_vec const &)`

### Class: `CATBaseUnknown_var` | Method: `CATBaseUnknown_var`
- **File Path:** `include/CATBaseUnknown_var.h`
- **Overload Count:** 4
- **Signatures:**
  - `CATBaseUnknown_var()`
  - `CATBaseUnknown_var(CATBaseUnknown_var&&)`
  - `CATBaseUnknown_var(CATBaseUnknown *)`
  - `CATBaseUnknown_var(const CATBaseUnknown_var &)`

### Class: `Iterator` | Method: `Iterator`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 4
- **Signatures:**
  - `Iterator(value_type*)`
  - `Iterator(CATMshMeshContainer&)`
  - `Iterator(CATMshMeshContainer&, index_type)`
  - `Iterator(CATMshTagSystem&, const CATMshTag, unsigned int)`

### Class: `Iterator` | Method: `operator++`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 4
- **Signatures:**
  - `operator++()`
  - `operator++(int)`
  - `operator++()`
  - `operator++()`

### Class: `CATMathPoint` | Method: `CATMathPoint`
- **File Path:** `include/CATMathPoint.h`
- **Overload Count:** 4
- **Signatures:**
  - `CATMathPoint()`
  - `CATMathPoint(const double, const double, const double)`
  - `CATMathPoint(const double [])`
  - `CATMathPoint(const CATMathPoint &)`

### Class: `CATMathVector` | Method: `CATMathVector`
- **File Path:** `include/CATMathVector.h`
- **Overload Count:** 4
- **Signatures:**
  - `CATMathVector()`
  - `CATMathVector(const double, const double, const double)`
  - `CATMathVector(const double [])`
  - `CATMathVector(const CATMathVector &)`

### Class: `LOPT_EDGE_cvty` | Method: `lopt_calc_convexity`
- **File Path:** `include/cvty.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `lopt_calc_convexity(SPAunit_vector const &, SPAunit_vector const &, SPAunit_vector const &, double const, double const &, double const &, double const &, logical &)`
  - `lopt_calc_convexity(EDGE *, double const, double const &, logical &, logical, logical)`
  - `lopt_calc_convexity(COEDGE *, double const, double const &, logical &)`
  - `lopt_calc_convexity(double const &, COEDGE *, double const)`

### Class: `DS_row_matrix` | Method: `Assign_from`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `Assign_from(const DS_row_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Assign_from(const DS_row_matrix &, double, DS_abs_vec::EQ_FLAG)`
  - `Assign_from(const DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Assign_from(const DS_abs_matrix &, double, DS_abs_vec::EQ_FLAG)`

### Class: `DS_row_matrix` | Method: `Lmult`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `Lmult(const DS_clm_matrix &, DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Lmult(const DS_abs_vec &, DS_abs_vec &, DS_abs_vec::EQ_FLAG)`
  - `Lmult(const DS_abs_matrix &, DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Lmult(const DS_row_matrix &, DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`

### Class: `DS_clm_matrix` | Method: `Assign_from`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `Assign_from(const DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Assign_from(const DS_abs_matrix &, double, DS_abs_vec::EQ_FLAG)`
  - `Assign_from(const DS_clm_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Assign_from(const DS_clm_matrix &, double, DS_abs_vec::EQ_FLAG)`

### Class: `DS_abs_vec` | Method: `Dotprod`
- **File Path:** `include/dsabvec.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `Dotprod(const DS_abs_vec &)`
  - `Dotprod(const DS_multi_banded_vec &)`
  - `Dotprod(const DS_block_vec &)`
  - `Dotprod(const DS_abcd_vec &)`

### Class: `DS_block_vec` | Method: `operator=`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `operator=(const DS_block_vec &)`
  - `operator=(double)`
  - `operator=(const DS_abs_vec &)`
  - `operator=(const DS_multi_banded_vec &)`

### Class: `DS_block_vec` | Method: `operator+=`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `operator+=(const DS_block_vec &)`
  - `operator+=(double)`
  - `operator+=(const DS_abs_vec &)`
  - `operator+=(const DS_multi_banded_vec &)`

### Class: `DS_multi_banded_vec` | Method: `Assign_into`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `Assign_into(DS_multi_banded_vec &, EQ_FLAG)`
  - `Assign_into(DS_multi_banded_vec &, double, EQ_FLAG)`
  - `Assign_into(DS_block_vec &, EQ_FLAG)`
  - `Assign_into(DS_block_vec &, double, EQ_FLAG)`

### Class: `RenderingObject` | Method: `insert_polyline_3d`
- **File Path:** `include/gen_rendobj.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `insert_polyline_3d(int, const float [], logical, const rgb_color &)`
  - `insert_polyline_3d(int, const SPAposition [], logical, const rgb_color &)`
  - `insert_polyline_3d(int, const float [], logical)`
  - `insert_polyline_3d(int, const SPAposition [], logical)`

### Class: `SPAinterval` | Method: `operator-`
- **File Path:** `include/interval.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `operator-(SPAinterval const &)`
  - `operator-(SPAinterval const &, SPAinterval const &)`
  - `operator-(SPAinterval const &, double)`
  - `operator-(double, SPAinterval const &)`

### Class: `option_header` | Method: `option_header`
- **File Path:** `include/option.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `option_header(char const *, int)`
  - `option_header(char const *, double)`
  - `option_header(char const *, char const *)`
  - `option_header()`

### Class: `option_header` | Method: `set`
- **File Path:** `include/option.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `set(int)`
  - `set(double)`
  - `set(char const *)`
  - `set(option_value const &)`

### Class: `option_header` | Method: `push`
- **File Path:** `include/option.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `push(int)`
  - `push(double)`
  - `push(char const *)`
  - `push(option_value const &)`

### Class: `rat_poly_vec` | Method: `rat_poly_vec`
- **File Path:** `include/poly.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `rat_poly_vec()`
  - `rat_poly_vec(poly_vec const &)`
  - `rat_poly_vec(poly_vec const &, polynomial const &)`
  - `rat_poly_vec(rat_poly_vec const &)`

### Class: `GRID` | Method: `add_clashes`
- **File Path:** `include/spd3rtn.hxx`
- **Overload Count:** 4
- **Signatures:**
  - `add_clashes(CHORDS &, int, int, int, int)`
  - `add_clashes(int const&, int const&, int const&, int const&, int const&, int const&, int const&, int const&, logical const&, logical const&)`
  - `add_clashes(CHORDS &, int, int, int, int, SPAposition &)`
  - `add_clashes(SPApar_pos &, SPApar_pos &, SPApar_box &, SPApar_box &)`

### Class: `CATSysConditionFunc_t` | Method: `CATSysConditionFunc_t`
- **File Path:** `include/CATFillDictionary.h`
- **Overload Count:** 3
- **Signatures:**
  - `CATSysConditionFunc_t(CATSysConditionFunc)`
  - `CATSysConditionFunc_t(decltype(nullptr))`
  - `CATSysConditionFunc_t(PFuncCondition)`

### Class: `CATMshBaseTag` | Method: `CATMshBaseTag`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 3
- **Signatures:**
  - `CATMshBaseTag()`
  - `CATMshBaseTag(const unsigned int)`
  - `CATMshBaseTag(const CATMshBaseTag&)`

### Class: `CATMshVertex` | Method: `CATMshVertex`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 3
- **Signatures:**
  - `CATMshVertex()`
  - `CATMshVertex(const CATMshVertexIndex&, const double (& )[3])`
  - `CATMshVertex(const CATMshVertexIndex&, const double (& )[3], const CATMshTag&)`

### Class: `Iterator` | Method: `operator*`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 3
- **Signatures:**
  - `operator*()`
  - `operator*()`
  - `operator*()`

### Class: `Iterator` | Method: `operator==`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 3
- **Signatures:**
  - `operator==(const Iterator&)`
  - `operator==(const Iterator&)`
  - `operator==(const Iterator&)`

### Class: `Iterator` | Method: `operator!=`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 3
- **Signatures:**
  - `operator!=(const Iterator&)`
  - `operator!=(const Iterator&)`
  - `operator!=(const Iterator&)`

### Class: `CATMshElement` | Method: `CATMshElement`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 3
- **Signatures:**
  - `CATMshElement()`
  - `CATMshElement(const Type, const CATMshElementIndex&, const CATMshVertexIndex (& )[maxNumberOfVertices])`
  - `CATMshElement(const Type, const Orientation, const CATMshElementIndex&, const CATMshVertexIndex (& )[maxNumberOfVertices], const CATMshTag&)`

### Class: `CATMathVector` | Method: `operator-`
- **File Path:** `include/CATMathVector.h`
- **Overload Count:** 3
- **Signatures:**
  - `operator-(const CATMathPoint &, const CATMathPoint &)`
  - `operator-(const CATMathVector &, const CATMathVector &)`
  - `operator-(const CATMathVector &)`

### Class: `CGMReleasable_uptr` | Method: `CGMReleasable_uptr`
- **File Path:** `include/CGMReleasable_uptr.h`
- **Overload Count:** 3
- **Signatures:**
  - `CGMReleasable_uptr()`
  - `CGMReleasable_uptr(CGMClassType *)`
  - `CGMReleasable_uptr(CGMReleasable_uptr &&)`

### Class: `DS_abs_matrix` | Method: `Set_row`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Set_row(int, double)`
  - `Set_row(int, const DS_abs_vec &)`
  - `Set_row(int, const DS_abs_vec &, double)`

### Class: `DS_abs_matrix` | Method: `Pluseq_row`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Pluseq_row(int, double)`
  - `Pluseq_row(int, const DS_abs_vec &)`
  - `Pluseq_row(int, const DS_abs_vec &, double)`

### Class: `DS_abs_matrix` | Method: `Set_clm`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Set_clm(int, double)`
  - `Set_clm(int, const DS_abs_vec &)`
  - `Set_clm(int, const DS_abs_vec &, double)`

### Class: `DS_abs_matrix` | Method: `Pluseq_clm`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Pluseq_clm(int, double)`
  - `Pluseq_clm(int, const DS_abs_vec &)`
  - `Pluseq_clm(int, const DS_abs_vec &, double)`

### Class: `DS_abs_matrix` | Method: `Lmult`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Lmult(const DS_abs_matrix &, DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Lmult(const DS_row_matrix &, DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Lmult(const DS_abs_vec &, DS_abs_vec &, DS_abs_vec::EQ_FLAG)`

### Class: `DS_row_matrix` | Method: `Set_row`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Set_row(int, double)`
  - `Set_row(int, const DS_abs_vec &)`
  - `Set_row(int, const DS_abs_vec &, double)`

### Class: `DS_row_matrix` | Method: `Pluseq_row`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Pluseq_row(int, double)`
  - `Pluseq_row(int, const DS_abs_vec &)`
  - `Pluseq_row(int, const DS_abs_vec &, double)`

### Class: `DS_clm_matrix` | Method: `Set_clm`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Set_clm(int, double)`
  - `Set_clm(int, const DS_abs_vec &)`
  - `Set_clm(int, const DS_abs_vec &, double)`

### Class: `DS_clm_matrix` | Method: `Pluseq_clm`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Pluseq_clm(int, double)`
  - `Pluseq_clm(int, const DS_abs_vec &)`
  - `Pluseq_clm(int, const DS_abs_vec &, double)`

### Class: `DS_clm_matrix` | Method: `Lmult`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Lmult(const DS_abs_matrix &, DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Lmult(const DS_abs_vec &, DS_abs_vec &, DS_abs_vec::EQ_FLAG)`
  - `Lmult(const DS_row_matrix &, DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`

### Class: `DS_block_clm_matrix` | Method: `Set_row`
- **File Path:** `include/dsbcmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Set_row(int, double)`
  - `Set_row(int, const DS_abs_vec &)`
  - `Set_row(int, const DS_abs_vec &, double)`

### Class: `DS_block_clm_matrix` | Method: `Pluseq_row`
- **File Path:** `include/dsbcmat.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Pluseq_row(int, double)`
  - `Pluseq_row(int, const DS_abs_vec &)`
  - `Pluseq_row(int, const DS_abs_vec &, double)`

### Class: `DS_block_vec` | Method: `DS_block_vec`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `DS_block_vec(int, int)`
  - `DS_block_vec(const DS_block_vec &)`
  - `DS_block_vec(const DS_abs_vec &)`

### Class: `DS_block_vec` | Method: `operator-=`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `operator-=(const DS_block_vec &)`
  - `operator-=(const DS_abs_vec &)`
  - `operator-=(const DS_multi_banded_vec &)`

### Class: `DS_block_vec` | Method: `Overwrite`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Overwrite(const DS_block_vec &, double)`
  - `Overwrite(const DS_abs_vec &, double)`
  - `Overwrite(const DS_multi_banded_vec &, double)`

### Class: `DS_block_vec` | Method: `Pluseq`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Pluseq(const DS_block_vec &, double)`
  - `Pluseq(const DS_abs_vec &, double)`
  - `Pluseq(const DS_multi_banded_vec &, double)`

### Class: `DS_block_vec` | Method: `Minuseq`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Minuseq(const DS_block_vec &, double)`
  - `Minuseq(const DS_abs_vec &, double)`
  - `Minuseq(const DS_multi_banded_vec &, double)`

### Class: `DS_block_vec` | Method: `Dotprod`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Dotprod(const DS_abs_vec &)`
  - `Dotprod(const DS_block_vec &)`
  - `Dotprod(const DS_multi_banded_vec &)`

### Class: `DS_crv_cstrn` | Method: `B`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `B()`
  - `B(int)`
  - `B(int, int)`

### Class: `DS_mbvec_row_matrix` | Method: `Set_clm`
- **File Path:** `include/dsmbrmt.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Set_clm(int, double)`
  - `Set_clm(int, const DS_abs_vec &)`
  - `Set_clm(int, const DS_abs_vec &, double)`

### Class: `DS_mbvec_row_matrix` | Method: `Pluseq_clm`
- **File Path:** `include/dsmbrmt.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Pluseq_clm(int, double)`
  - `Pluseq_clm(int, const DS_abs_vec &)`
  - `Pluseq_clm(int, const DS_abs_vec &, double)`

### Class: `DS_multi_banded_vec` | Method: `DS_multi_banded_vec`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `DS_multi_banded_vec(int, int)`
  - `DS_multi_banded_vec(const DS_multi_banded_vec &)`
  - `DS_multi_banded_vec(const DS_abs_vec &)`

### Class: `DS_multi_banded_vec` | Method: `operator=`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `operator=(const DS_multi_banded_vec &)`
  - `operator=(double)`
  - `operator=(const DS_abs_vec &)`

### Class: `DS_multi_banded_vec` | Method: `operator+=`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `operator+=(double)`
  - `operator+=(const DS_abs_vec &)`
  - `operator+=(const DS_multi_banded_vec &)`

### Class: `DS_multi_banded_vec` | Method: `Dotprod`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `Dotprod(const DS_abs_vec &)`
  - `Dotprod(const DS_multi_banded_vec &)`
  - `Dotprod(const DS_block_vec &)`

### Class: `DS_zone` | Method: `DS_zone`
- **File Path:** `include/dszone.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `DS_zone(DS_ZONE, int, int, int, int *, int *)`
  - `DS_zone(DS_ZONE, int, int, int, int *, int *, int *)`
  - `DS_zone(DS_zone &)`

### Class: `DS_poly_zone` | Method: `DS_poly_zone`
- **File Path:** `include/dszone.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `DS_poly_zone(const DS_poly_zone &)`
  - `DS_poly_zone(DS_dmod *)`
  - `DS_poly_zone(DS_dbl_block&, DS_dbl_block&, DS_dmod*)`

### Class: `area_property` | Method: `operator*`
- **File Path:** `include/faceprop.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `operator*(double, area_property const &)`
  - `operator*(area_property const &, double)`
  - `operator*(area_property const &, SPAtransf const &)`

### Class: `PickEvent` | Method: `PickEvent`
- **File Path:** `include/gen_pick.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `PickEvent()`
  - `PickEvent(int, int, int, window_handle)`
  - `PickEvent(int, int, int, window_handle, unsigned int)`

### Class: `RenderingObject` | Method: `insert_text`
- **File Path:** `include/gen_rendobj.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `insert_text(const SPAposition&, const char*, const rgb_color &)`
  - `insert_text(const SPAposition&, const char*, const rgb_color &, text_alignment_type)`
  - `insert_text(const SPAposition&, const char*)`

### Class: `SPAinterval` | Method: `operator+`
- **File Path:** `include/interval.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `operator+(SPAinterval const &, SPAinterval const &)`
  - `operator+(SPAinterval const &, double)`
  - `operator+(double, SPAinterval const &)`

### Class: `const_iterator` | Method: `const_iterator`
- **File Path:** `include/iscmpicksub.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `const_iterator()`
  - `const_iterator(list_node *)`
  - `const_iterator(const iterator &)`

### Class: `mass_property` | Method: `operator*`
- **File Path:** `include/massprop.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `operator*(double, mass_property const &)`
  - `operator*(mass_property const &, double)`
  - `operator*(mass_property const &, SPAtransf const &)`

### Class: `param_string` | Method: `param_string`
- **File Path:** `include/parm_str.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `param_string(const param_string&)`
  - `param_string()`
  - `param_string(const char*)`

### Class: `param_string` | Method: `operator+=`
- **File Path:** `include/parm_str.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `operator+=(char)`
  - `operator+=(const char*)`
  - `operator+=(const param_string&)`

### Class: `rat_poly_vec` | Method: `operator*`
- **File Path:** `include/poly.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `operator*(rat_poly const &, rat_poly_vec const &)`
  - `operator*(rat_poly_vec const &, rat_poly const &)`
  - `operator*(rat_poly_vec const &, rat_poly_vec const &)`

### Class: `point_face_containment` | Method: `sg_point_in_face`
- **File Path:** `include/sgquertn.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `sg_point_in_face(SPAposition const &, FACE*, SPAtransf const&, SPApar_pos const&, logical, int)`
  - `sg_point_in_face(SPAposition const &, FACE*, SPAtransf const&, SPApar_pos const&, SPAposition const&, point_face_containment, logical, int)`
  - `sg_point_in_face(SPAposition const &, FACE const *, SPAtransf const &, surface const &, ENTITY *&, SPApar_pos const &, SPApar_pos &)`

### Class: `CHORDS` | Method: `CHORDS`
- **File Path:** `include/spd3rtn.hxx`
- **Overload Count:** 3
- **Signatures:**
  - `CHORDS(SPAposition*, int, int, int, int, int)`
  - `CHORDS(SPAposition &, SPAposition &)`
  - `CHORDS(SPAposition&, SPAposition&, int, int, int, int)`

### Class: `acis_scm_entity_mgr_factory` | Method: `acis_scm_entity_mgr_factory`
- **File Path:** `include/acis_scm_entity_mgr_factory.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `acis_scm_entity_mgr_factory()`
  - `acis_scm_entity_mgr_factory(const VOID_LIST&)`

### Class: `ADM_acis_seg_callback` | Method: `ADM_acis_seg_callback`
- **File Path:** `include/adm_acis_seg_cb.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `ADM_acis_seg_callback(const ADM_acis_seg_callback&)`
  - `ADM_acis_seg_callback()`

### Class: `asm_info` | Method: `asm_info`
- **File Path:** `include/asm_api.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `asm_info()`
  - `asm_info(asm_model const*)`

### Class: `asm_info` | Method: `end`
- **File Path:** `include/asm_api.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `end(outcome, asm_event_type)`
  - `end(outcome, asm_event_type, asm_event_info*)`

### Class: `bipolynomial` | Method: `operator-`
- **File Path:** `include/bipoly.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator-(bipolynomial const &)`
  - `operator-(bipolynomial const &, bipolynomial const &)`

### Class: `rat_bipoly_vec` | Method: `operator/`
- **File Path:** `include/bipoly.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator/(rat_bipoly_vec const &, rat_bipoly const &)`
  - `operator/(rat_bipoly_vec const &, rat_bipoly const &)`

### Class: `rat_bipoly_vec` | Method: `operator-`
- **File Path:** `include/bipoly.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator-(rat_bipoly_vec const &)`
  - `operator-(rat_bipoly_vec const &, rat_bipoly_vec const &)`

### Class: `support_entity_dlist` | Method: `support_entity_dlist`
- **File Path:** `include/bl_att.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `support_entity_dlist(support_entity *)`
  - `support_entity_dlist(const support_entity_dlist &)`

### Class: `v_bl_contact_pt` | Method: `v_bl_contact_pt`
- **File Path:** `include/bl_cntct.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `v_bl_contact_pt(SVEC const *)`
  - `v_bl_contact_pt(v_bl_contact_pt const &)`

### Class: `SPAinterval` | Method: `operator%`
- **File Path:** `include/box.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator%(SPAunit_vector const &, SPAbox const &)`
  - `operator%(SPAbox const &, SPAunit_vector const &)`

### Class: `Entity_List_Iterator` | Method: `operator++`
- **File Path:** `include/bs_util.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator++()`
  - `operator++(int)`

### Class: `Node_Wrapper` | Method: `Node_Wrapper`
- **File Path:** `include/bs_util.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Node_Wrapper()`
  - `Node_Wrapper(HH_GlobalNode *)`

### Class: `Node_Sorter` | Method: `Node_Sorter`
- **File Path:** `include/bs_util.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Node_Sorter()`
  - `Node_Sorter(HH_GlobalNode *, HH_GlobalNode *)`

### Class: `NodePair` | Method: `NodePair`
- **File Path:** `include/bs_util.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `NodePair()`
  - `NodePair(HH_GlobalNode *)`

### Class: `HH_Wrapper` | Method: `HH_Wrapper`
- **File Path:** `include/bs_util.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `HH_Wrapper()`
  - `HH_Wrapper(void *)`

### Class: `CATCollecRoot` | Method: `CATCollecRoot`
- **File Path:** `include/CATCollecRoot.h`
- **Overload Count:** 2
- **Signatures:**
  - `CATCollecRoot()`
  - `CATCollecRoot(const CATCollecRoot&)`

### Class: `CATMshTag` | Method: `CATMshTag`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `CATMshTag()`
  - `CATMshTag(const unsigned int)`

### Class: `CATMshIndex` | Method: `CATMshIndex`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `CATMshIndex()`
  - `CATMshIndex(const unsigned int)`

### Class: `CATMshVertexIndex` | Method: `CATMshVertexIndex`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `CATMshVertexIndex()`
  - `CATMshVertexIndex(const unsigned int)`

### Class: `CATMshElementIndex` | Method: `CATMshElementIndex`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `CATMshElementIndex()`
  - `CATMshElementIndex(const unsigned int)`

### Class: `CATMshDomainIndex` | Method: `CATMshDomainIndex`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `CATMshDomainIndex()`
  - `CATMshDomainIndex(const unsigned int)`

### Class: `CATMshTopoFaceIndex` | Method: `CATMshTopoFaceIndex`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `CATMshTopoFaceIndex()`
  - `CATMshTopoFaceIndex(const unsigned int)`

### Class: `CATMshTopoEdgeIndex` | Method: `CATMshTopoEdgeIndex`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `CATMshTopoEdgeIndex()`
  - `CATMshTopoEdgeIndex(const unsigned int)`

### Class: `CATMshTopoVertexIndex` | Method: `CATMshTopoVertexIndex`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `CATMshTopoVertexIndex()`
  - `CATMshTopoVertexIndex(const unsigned int)`

### Class: `ConstIterator` | Method: `operator++`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `operator++()`
  - `operator++(int)`

### Class: `CATMshElement` | Method: `begin`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `begin()`
  - `begin()`

### Class: `CATMshElement` | Method: `end`
- **File Path:** `include/CATIMshMesh.h`
- **Overload Count:** 2
- **Signatures:**
  - `end()`
  - `end()`

### Class: `om_guard` | Method: `om_guard`
- **File Path:** `include/CATMacForIUnknown.h`
- **Overload Count:** 2
- **Signatures:**
  - `om_guard()`
  - `om_guard()`

### Class: `CATMathPoint` | Method: `GetCoord`
- **File Path:** `include/CATMathPoint.h`
- **Overload Count:** 2
- **Signatures:**
  - `GetCoord(double &, double &, double &)`
  - `GetCoord(double [])`

### Class: `CATMathPoint` | Method: `SetCoord`
- **File Path:** `include/CATMathPoint.h`
- **Overload Count:** 2
- **Signatures:**
  - `SetCoord(const double, const double, const double)`
  - `SetCoord(const double [])`

### Class: `CATMathPoint` | Method: `operator*`
- **File Path:** `include/CATMathPoint.h`
- **Overload Count:** 2
- **Signatures:**
  - `operator*(const double, const CATMathPoint &)`
  - `operator*(const CATMathPoint &, const double)`

### Class: `CATMathVector` | Method: `GetCoord`
- **File Path:** `include/CATMathVector.h`
- **Overload Count:** 2
- **Signatures:**
  - `GetCoord(double &, double &, double &)`
  - `GetCoord(double [])`

### Class: `CATMathVector` | Method: `SetCoord`
- **File Path:** `include/CATMathVector.h`
- **Overload Count:** 2
- **Signatures:**
  - `SetCoord(const double, const double, const double)`
  - `SetCoord(const double [])`

### Class: `CATMathVector` | Method: `operator*`
- **File Path:** `include/CATMathVector.h`
- **Overload Count:** 2
- **Signatures:**
  - `operator*(const double, const CATMathVector &)`
  - `operator*(const CATMathVector &, const double)`

### Class: `CGMMeshGeometry` | Method: `CGMMeshGeometry`
- **File Path:** `include/CGMMeshGeometry.h`
- **Overload Count:** 2
- **Signatures:**
  - `CGMMeshGeometry()`
  - `CGMMeshGeometry(CATULONG64)`

### Class: `Bar` | Method: `Bar`
- **File Path:** `include/CGMMeshGeometry.h`
- **Overload Count:** 2
- **Signatures:**
  - `Bar()`
  - `Bar(Node, Node)`

### Class: `cmdstack` | Method: `cmdstack`
- **File Path:** `include/cmdstack.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `cmdstack(int)`
  - `cmdstack(cmdstack *)`

### Class: `pt_cvty_info` | Method: `compute_pt_cvty_info`
- **File Path:** `include/compcvty.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `compute_pt_cvty_info(EDGE *, double, logical)`
  - `compute_pt_cvty_info(COEDGE *, double, logical)`

### Class: `pt_cvty_info` | Method: `compute_start_pt_cvty_info`
- **File Path:** `include/compcvty.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `compute_start_pt_cvty_info(EDGE *, logical)`
  - `compute_start_pt_cvty_info(COEDGE *, logical)`

### Class: `pt_cvty_info` | Method: `compute_mid_pt_cvty_info`
- **File Path:** `include/compcvty.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `compute_mid_pt_cvty_info(EDGE *, logical)`
  - `compute_mid_pt_cvty_info(COEDGE *, logical)`

### Class: `pt_cvty_info` | Method: `compute_end_pt_cvty_info`
- **File Path:** `include/compcvty.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `compute_end_pt_cvty_info(EDGE *, logical)`
  - `compute_end_pt_cvty_info(COEDGE *, logical)`

### Class: `ed_cvty_info` | Method: `compute_ed_cvty_info`
- **File Path:** `include/compcvty.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `compute_ed_cvty_info(EDGE *, logical, logical, SPAinterval const &)`
  - `compute_ed_cvty_info(COEDGE *, logical, logical, SPAinterval const &)`

### Class: `ContainerTable` | Method: `lookupInTable`
- **File Path:** `include/comp_handle_typ.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `lookupInTable(int, int)`
  - `lookupInTable(void *, int)`

### Class: `use_counted_box` | Method: `use_counted_box`
- **File Path:** `include/container.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `use_counted_box()`
  - `use_counted_box(SPAbox*)`

### Class: `use_counted_ver_box` | Method: `use_counted_ver_box`
- **File Path:** `include/container.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `use_counted_ver_box()`
  - `use_counted_ver_box(SPAbox*)`

### Class: `use_counted_par_box` | Method: `use_counted_par_box`
- **File Path:** `include/container.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `use_counted_par_box()`
  - `use_counted_par_box(SPApar_box*)`

### Class: `DS_abs_matrix` | Method: `DS_abs_matrix`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_abs_matrix(TYPE_ID, int, int)`
  - `DS_abs_matrix(const DS_abs_matrix &)`

### Class: `DS_abs_matrix` | Method: `operator=`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator=(const DS_abs_matrix &)`
  - `operator=(double)`

### Class: `DS_abs_matrix` | Method: `operator+=`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator+=(const DS_abs_matrix &)`
  - `operator+=(double)`

### Class: `DS_abs_matrix` | Method: `operator-=`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator-=(const DS_abs_matrix &)`
  - `operator-=(double)`

### Class: `DS_abs_matrix` | Method: `Assign_from`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Assign_from(const DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Assign_from(const DS_abs_matrix &, double, DS_abs_vec::EQ_FLAG)`

### Class: `DS_abs_matrix` | Method: `Rmult`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Rmult(const DS_abs_matrix &, DS_abs_matrix &, DS_abs_vec::EQ_FLAG)`
  - `Rmult(const DS_abs_vec &, DS_abs_vec &, DS_abs_vec::EQ_FLAG)`

### Class: `DS_row_matrix` | Method: `DS_row_matrix`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_row_matrix(TYPE_ID, int, int)`
  - `DS_row_matrix(const DS_row_matrix &)`

### Class: `DS_row_matrix` | Method: `Row`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Row(int)`
  - `Row(int)`

### Class: `DS_row_matrix` | Method: `operator=`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator=(const DS_abs_matrix &)`
  - `operator=(double)`

### Class: `DS_row_matrix` | Method: `operator+=`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator+=(const DS_abs_matrix &)`
  - `operator+=(double)`

### Class: `DS_clm_matrix` | Method: `DS_clm_matrix`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_clm_matrix(TYPE_ID, int, int)`
  - `DS_clm_matrix(const DS_clm_matrix &)`

### Class: `DS_clm_matrix` | Method: `Clm`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Clm(int)`
  - `Clm(int)`

### Class: `DS_clm_matrix` | Method: `operator=`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator=(const DS_abs_matrix &)`
  - `operator=(double)`

### Class: `DS_clm_matrix` | Method: `operator+=`
- **File Path:** `include/dsabmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator+=(const DS_abs_matrix &)`
  - `operator+=(double)`

### Class: `DS_abs_vec` | Method: `DS_abs_vec`
- **File Path:** `include/dsabvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_abs_vec(TYPE_ID, int)`
  - `DS_abs_vec(const DS_abs_vec&)`

### Class: `DS_abs_vec` | Method: `Largest_elem`
- **File Path:** `include/dsabvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Largest_elem()`
  - `Largest_elem(const DS_int_block&)`

### Class: `DS_abs_vec` | Method: `operator=`
- **File Path:** `include/dsabvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator=(const DS_abs_vec &)`
  - `operator=(double)`

### Class: `DS_abs_vec` | Method: `operator+=`
- **File Path:** `include/dsabvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator+=(const DS_abs_vec &)`
  - `operator+=(double)`

### Class: `DS_abs_vec` | Method: `operator-=`
- **File Path:** `include/dsabvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator-=(const DS_abs_vec &)`
  - `operator-=(double)`

### Class: `DS_abs_vec` | Method: `Assign_from`
- **File Path:** `include/dsabvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Assign_from(const DS_abs_vec &, EQ_FLAG)`
  - `Assign_from(const DS_abs_vec &, double, EQ_FLAG)`

### Class: `DS_block_clm_matrix` | Method: `DS_block_clm_matrix`
- **File Path:** `include/dsbcmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_block_clm_matrix(int, int)`
  - `DS_block_clm_matrix(const DS_block_clm_matrix &)`

### Class: `DS_block_clm_matrix` | Method: `operator()`
- **File Path:** `include/dsbcmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator()(int, int)`
  - `operator()(int, int)`

### Class: `DS_block_clm_matrix` | Method: `Clm`
- **File Path:** `include/dsbcmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Clm(int)`
  - `Clm(int)`

### Class: `DS_block_vec` | Method: `operator[]`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator[](int)`
  - `operator[](int)`

### Class: `DS_block_vec` | Method: `Assign_from`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Assign_from(const DS_abs_vec &, EQ_FLAG)`
  - `Assign_from(const DS_abs_vec &, double, EQ_FLAG)`

### Class: `DS_block_vec` | Method: `Assign_into`
- **File Path:** `include/dsblvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Assign_into(DS_block_vec &, EQ_FLAG)`
  - `Assign_into(DS_block_vec &, double, EQ_FLAG)`

### Class: `DS_cstrn` | Method: `DS_cstrn`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_cstrn(DS_CST, int, DS_CSTRN_SRC, void *, void *, int, int, int, int, double, DS_dmod  *, DS_cstrn *, DS_dmod  *, DS_cstrn *)`
  - `DS_cstrn(DS_cstrn &)`

### Class: `DS_pt_cstrn` | Method: `DS_pt_cstrn`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_pt_cstrn(DS_dmod       *, DS_dmod  *, DS_CSTRN_SRC, void     *, double   *, double   *, double   *, double   *, double   *, double   *, double   *, double   *, double   *, double   *, int, double, double, int, int, DS_cstrn *)`
  - `DS_pt_cstrn(DS_pt_cstrn &)`

### Class: `DS_pt_cstrn` | Method: `Domain_pt`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_pt()`
  - `Domain_pt(int)`

### Class: `DS_pt_cstrn` | Method: `Domain_dir`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_dir(DS_CST_PT_INDEX         // in : which domain_dir to return)`
  - `Domain_dir(DS_CST_PT_INDEX         // in : which domain_dir to return, int)`

### Class: `DS_pt_cstrn` | Method: `Cstrn_val`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Cstrn_val(DS_CST_PT_INDEX         // in : which cstrn_val to return)`
  - `Cstrn_val(DS_CST_PT_INDEX          // in : which cstrn_val to return, int)`

### Class: `DS_pt_cstrn` | Method: `Image_pt`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Image_pt(DS_CST_PT_INDEX         // in : which image_pt to return)`
  - `Image_pt(DS_CST_PT_INDEX         // in : which image_pt to return, int)`

### Class: `DS_pt_cstrn` | Method: `Cstrn_def`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Cstrn_def(DS_CST_PT_INDEX         // in : which cstrn_def to return)`
  - `Cstrn_def(DS_CST_PT_INDEX         // in : which cstrn_def to return, int)`

### Class: `DS_pt_cstrn` | Method: `Image_old`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Image_old(DS_CST_PT_INDEX        // in : which image_old to return)`
  - `Image_old(DS_CST_PT_INDEX        // in : which image_old to return, int)`

### Class: `DS_crv_cstrn` | Method: `DS_crv_cstrn`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_crv_cstrn(Spatial_abs_hurler &, DS_enforcement_mechanism* &, DS_dmod  *, DS_dmod  *, DS_pfunc *, DS_pfunc *, DS_pfunc *, DS_pfunc *, void (* )          // opt: func to calc curve C and W pt vals
     (void *src_data,             // in : app defined data
      double s,                   // in : edge s param value
      double *C,                  // out: surface C, void *, DS_CSTRN_SRC                // in : records cstrn origin. oneof:, int, double *, int, double, int, DS_cstrn *)`
  - `DS_crv_cstrn(DS_crv_cstrn &        // in : object being copied)`

### Class: `DS_crv_cstrn` | Method: `Image_pt_count`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Image_pt_count(int, int)`
  - `Image_pt_count()`

### Class: `DS_crv_cstrn` | Method: `Dof_map`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Dof_map()`
  - `Dof_map(int)`

### Class: `DS_crv_cstrn` | Method: `Seg_elem`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seg_elem()`
  - `Seg_elem(int)`

### Class: `DS_crv_cstrn` | Method: `Src_C_bas`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src_C_bas()`
  - `Src_C_bas(int, int)`

### Class: `DS_crv_cstrn` | Method: `Seg_bnds`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seg_bnds()`
  - `Seg_bnds(int)`

### Class: `DS_crv_cstrn` | Method: `Seg_bnds_W`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seg_bnds_W()`
  - `Seg_bnds_W(int)`

### Class: `DS_crv_cstrn` | Method: `Src_s_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src_s_pts()`
  - `Src_s_pts(int)`

### Class: `DS_crv_cstrn` | Method: `Src_W_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src_W_pts()`
  - `Src_W_pts(int)`

### Class: `DS_crv_cstrn` | Method: `Src_Wn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src_Wn_pts()`
  - `Src_Wn_pts(int)`

### Class: `DS_crv_cstrn` | Method: `Src_Wnn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src_Wnn_pts()`
  - `Src_Wnn_pts(int)`

### Class: `DS_crv_cstrn` | Method: `Out_W_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Out_W_pts()`
  - `Out_W_pts(int)`

### Class: `DS_crv_cstrn` | Method: `Out_Wn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Out_Wn_pts()`
  - `Out_Wn_pts(int)`

### Class: `DS_crv_cstrn` | Method: `Out_Wnn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Out_Wnn_pts()`
  - `Out_Wnn_pts(int)`

### Class: `DS_crv_cstrn` | Method: `Seg_bnd_W_size`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seg_bnd_W_size(int, int)`
  - `Seg_bnd_W_size()`

### Class: `DS_crv_cstrn` | Method: `Image_pts_size`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Image_pts_size(int, int, int)`
  - `Image_pts_size()`

### Class: `DS_crv_cstrn` | Method: `Domain_pts_size`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_pts_size(int, int, int)`
  - `Domain_pts_size()`

### Class: `DS_crv_cstrn` | Method: `Build_L_Lc_row`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Build_L_Lc_row(DS_dmod *, DS_symeq *, int)`
  - `Build_L_Lc_row(DS_dmod *, DS_eqns *, int)`

### Class: `DS_link_cstrn` | Method: `DS_link_cstrn`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_link_cstrn(DS_enforcement_mechanism* &, DS_dmod *, DS_dmod *, DS_pfunc *, DS_pfunc *, DS_pfunc *, DS_pfunc *, DS_pfunc *, DS_pfunc *, DS_pfunc *, DS_pfunc *, void (* )           // opt : func to calc curve C and W pt vals
    (void *src_data,               // in : app defined data
     double s,                     // in : edge s param value
     double *C,                    // out: surface C, void *, void *, DS_CSTRN_SRC, int, double *, double *, int, int, DS_cstrn *, DS_cstrn *, SPA_DM_flipped_state)`
  - `DS_link_cstrn(DS_link_cstrn &       // in : object being copied)`

### Class: `DS_link_cstrn` | Method: `Image_pt_count`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Image_pt_count(int, int)`
  - `Image_pt_count()`

### Class: `DS_link_cstrn` | Method: `Gauss_pt_count`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Gauss_pt_count(int)`
  - `Gauss_pt_count()`

### Class: `DS_link_cstrn` | Method: `Segment_pt_count`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Segment_pt_count(int, int)`
  - `Segment_pt_count(int)`

### Class: `DS_link_cstrn` | Method: `C1_dof_map`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `C1_dof_map()`
  - `C1_dof_map(int)`

### Class: `DS_link_cstrn` | Method: `Cn1_dof_map`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Cn1_dof_map()`
  - `Cn1_dof_map(int)`

### Class: `DS_link_cstrn` | Method: `C2_dof_map`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `C2_dof_map()`
  - `C2_dof_map(int)`

### Class: `DS_link_cstrn` | Method: `Cn2_dof_map`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Cn2_dof_map()`
  - `Cn2_dof_map(int)`

### Class: `DS_link_cstrn` | Method: `Cnn2_dof_map`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Cnn2_dof_map()`
  - `Cnn2_dof_map(int)`

### Class: `DS_link_cstrn` | Method: `Dmesh_C_map`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Dmesh_C_map()`
  - `Dmesh_C_map(int)`

### Class: `DS_link_cstrn` | Method: `Seg1_bnds`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seg1_bnds()`
  - `Seg1_bnds(int)`

### Class: `DS_link_cstrn` | Method: `Seg2_bnds`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seg2_bnds()`
  - `Seg2_bnds(int)`

### Class: `DS_link_cstrn` | Method: `Seg1_bnds_W`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seg1_bnds_W()`
  - `Seg1_bnds_W(int)`

### Class: `DS_link_cstrn` | Method: `Seg2_bnds_W`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seg2_bnds_W()`
  - `Seg2_bnds_W(int)`

### Class: `DS_link_cstrn` | Method: `Src1_s_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src1_s_pts()`
  - `Src1_s_pts(int, int (bndry_flag))`

### Class: `DS_link_cstrn` | Method: `Src2_s_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src2_s_pts()`
  - `Src2_s_pts(int, int (bndry_flag))`

### Class: `DS_link_cstrn` | Method: `Src1_W_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src1_W_pts()`
  - `Src1_W_pts(int)`

### Class: `DS_link_cstrn` | Method: `Src2_W_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src2_W_pts()`
  - `Src2_W_pts(int)`

### Class: `DS_link_cstrn` | Method: `Src1_Wn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src1_Wn_pts()`
  - `Src1_Wn_pts(int)`

### Class: `DS_link_cstrn` | Method: `Src2_Wn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src2_Wn_pts()`
  - `Src2_Wn_pts(int)`

### Class: `DS_link_cstrn` | Method: `Src1_Wnn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src1_Wnn_pts()`
  - `Src1_Wnn_pts(int)`

### Class: `DS_link_cstrn` | Method: `Src2_Wnn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Src2_Wnn_pts()`
  - `Src2_Wnn_pts(int)`

### Class: `DS_link_cstrn` | Method: `Out1_W_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Out1_W_pts()`
  - `Out1_W_pts(int)`

### Class: `DS_link_cstrn` | Method: `Out2_W_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Out2_W_pts()`
  - `Out2_W_pts(int)`

### Class: `DS_link_cstrn` | Method: `Out1_Wn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Out1_Wn_pts()`
  - `Out1_Wn_pts(int)`

### Class: `DS_link_cstrn` | Method: `Out2_Wn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Out2_Wn_pts()`
  - `Out2_Wn_pts(int)`

### Class: `DS_link_cstrn` | Method: `Out1_Wnn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Out1_Wnn_pts()`
  - `Out1_Wnn_pts(int)`

### Class: `DS_link_cstrn` | Method: `Out2_Wnn_pts`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Out2_Wnn_pts()`
  - `Out2_Wnn_pts(int)`

### Class: `DS_link_cstrn` | Method: `Seg_bnd_W_size`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seg_bnd_W_size(int, int)`
  - `Seg_bnd_W_size()`

### Class: `DS_link_cstrn` | Method: `Image_pts_size`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Image_pts_size(int, int, int)`
  - `Image_pts_size()`

### Class: `DS_link_cstrn` | Method: `Domain_pts_size`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_pts_size(int, int, int)`
  - `Domain_pts_size()`

### Class: `DS_link_cstrn` | Method: `Compare_d_with_CX`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Compare_d_with_CX(double &)`
  - `Compare_d_with_CX(double *, int)`

### Class: `DS_link_cstrn` | Method: `Build_dmesh_Cd_row`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Build_dmesh_Cd_row(int, int, int, DS_eqns*)`
  - `Build_dmesh_Cd_row(int, int, int *, int, int, int *, DS_eqns *, int)`

### Class: `DS_area_cstrn` | Method: `DS_area_cstrn`
- **File Path:** `include/dscstrn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_area_cstrn(DS_dmod       *, DS_CSTRN_SRC // in : records cstrn origin. oneof:, void     *, int, DS_zone  *, int, DS_cstrn *)`
  - `DS_area_cstrn(DS_area_cstrn &)`

### Class: `DS_dmesh` | Method: `DS_dmesh`
- **File Path:** `include/dsdmesh.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_dmesh(DS_dmod *, int)`
  - `DS_dmesh(DS_dmesh &)`

### Class: `DS_mlink` | Method: `DS_mlink`
- **File Path:** `include/dsdmesh.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_mlink(DS_dmesh *, DS_dmod  *, DS_dmod  *, DS_link_cstrn *, DS_mlink *)`
  - `DS_mlink(DS_mlink &)`

### Class: `DS_dmod` | Method: `DS_dmod`
- **File Path:** `include/dsdmod.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_dmod(DS_DMO, int, int, DS_pfunc *, double, double, double, double, double)`
  - `DS_dmod(DS_dmod &, int)`

### Class: `DS_dmod` | Method: `Seam`
- **File Path:** `include/dsdmod.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Seam()`
  - `Seam(int)`

### Class: `DS_dsurf` | Method: `DS_dsurf`
- **File Path:** `include/dsdmod.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_dsurf(DS_pfunc *, int, int, double, double, double, double, double, double, double, double, double, double, double)`
  - `DS_dsurf(DS_dsurf &, int)`

### Class: `DS_dcurv` | Method: `DS_dcurv`
- **File Path:** `include/dsdmod.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_dcurv(DS_pfunc *, int, int, double, double, double, double, double, double, double)`
  - `DS_dcurv(DS_dcurv &, int)`

### Class: `DS_face_model_pair` | Method: `DS_face_model_pair`
- **File Path:** `include/dsfmarr.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_face_model_pair(FACE*, ATTRIB_DSMODEL*)`
  - `DS_face_model_pair(const DS_face_model_pair &)`

### Class: `DS_GENBLK_CONTAINER` | Method: `DS_GENBLK_CONTAINER`
- **File Path:** `include/dsgenblk.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_GENBLK_CONTAINER(int, int)`
  - `DS_GENBLK_CONTAINER(DS_GENBLK_CONTAINER const &)`

### Class: `DS_GENBLK_CONTAINER` | Method: `operator[]`
- **File Path:** `include/dsgenblk.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator[](int)`
  - `operator[](int)`

### Class: `DS_GENBLK_CONTAINER` | Method: `Insert`
- **File Path:** `include/dsgenblk.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Insert(int, int)`
  - `Insert(int, int, DS_GENBLK_CLASS const &)`

### Class: `DS_GENBLK_CONTAINER` | Method: `Need`
- **File Path:** `include/dsgenblk.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Need(int)`
  - `Need(int, Exact_flag)`

### Class: `DS_GENBLK_CONTAINER` | Method: `Grow`
- **File Path:** `include/dsgenblk.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Grow(int)`
  - `Grow(int, Exact_flag)`

### Class: `DS_load` | Method: `DS_load`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_load(DS_dmod*, DS_LDS, double, int, DS_load *)`
  - `DS_load(DS_load &)`

### Class: `DS_pt_press` | Method: `DS_pt_press`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_pt_press(DS_dmod *, double, DS_pfunc *, int, double *, int, DS_load *)`
  - `DS_pt_press(DS_pt_press &)`

### Class: `DS_pt_press` | Method: `Image_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Image_pt()`
  - `Image_pt(int)`

### Class: `DS_pt_press` | Method: `Image_dir`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Image_dir()`
  - `Image_dir(int)`

### Class: `DS_pt_press` | Method: `Domain_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_pt()`
  - `Domain_pt(int)`

### Class: `DS_dyn_load` | Method: `DS_dyn_load`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_dyn_load(DS_dmod *, double, double, double, int, int, DS_load *)`
  - `DS_dyn_load(DS_dyn_load &)`

### Class: `DS_dist_press` | Method: `DS_dist_press`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_dist_press(DS_dmod*, double, int, int, double *, double *, int, DS_load *)`
  - `DS_dist_press(DS_dist_press &)`

### Class: `DS_dist_press` | Method: `Domain_min`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_min()`
  - `Domain_min(int)`

### Class: `DS_dist_press` | Method: `Domain_max`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_max()`
  - `Domain_max(int)`

### Class: `DS_vector_load` | Method: `DS_vector_load`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_vector_load(DS_dmod *, double, DS_pfunc *, double *, int, DS_load *)`
  - `DS_vector_load(DS_vector_load &)`

### Class: `DS_vector_load` | Method: `Image_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Image_pt(int)`
  - `Image_pt(int, int)`

### Class: `DS_attractor` | Method: `DS_attractor`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_attractor(DS_dmod *, double, DS_pfunc *, double *, int, int, DS_load *)`
  - `DS_attractor(DS_attractor &)`

### Class: `DS_spring` | Method: `DS_spring`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_spring(DS_dmod *, double, DS_pfunc *, double *, double *, int, int, DS_load *)`
  - `DS_spring(DS_spring &)`

### Class: `DS_spring` | Method: `Surf_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Surf_pt()`
  - `Surf_pt(int)`

### Class: `DS_spring` | Method: `Surf_dir`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Surf_dir()`
  - `Surf_dir(int)`

### Class: `DS_spring` | Method: `Def_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Def_pt()`
  - `Def_pt(int)`

### Class: `DS_spring` | Method: `Free_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Free_pt()`
  - `Free_pt(int)`

### Class: `DS_spring` | Method: `Domain_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_pt()`
  - `Domain_pt(int)`

### Class: `DS_spring_set` | Method: `DS_spring_set`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_spring_set(DS_dmod *, double, DS_pfunc *, int, double *, double *, int, DS_load *)`
  - `DS_spring_set(DS_spring_set &)`

### Class: `DS_spring_set` | Method: `Domain_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_pt()`
  - `Domain_pt(int)`

### Class: `DS_spring_set` | Method: `Surf_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Surf_pt()`
  - `Surf_pt(int)`

### Class: `DS_spring_set` | Method: `Def_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Def_pt()`
  - `Def_pt(int)`

### Class: `DS_spring_set` | Method: `Free_pt`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Free_pt()`
  - `Free_pt(int)`

### Class: `DS_spring_set` | Method: `Pos_basis`
- **File Path:** `include/dsload.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Pos_basis()`
  - `Pos_basis(int)`

### Class: `DS_lueqns` | Method: `DS_lueqns`
- **File Path:** `include/dslueqns.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_lueqns(int, int, int, int, int)`
  - `DS_lueqns(const DS_lueqns &)`

### Class: `DS_lueqns` | Method: `A`
- **File Path:** `include/dslueqns.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `A()`
  - `A(int, int)`

### Class: `DS_lueqns` | Method: `B`
- **File Path:** `include/dslueqns.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `B()`
  - `B(int, int)`

### Class: `DS_lueqns` | Method: `C`
- **File Path:** `include/dslueqns.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `C()`
  - `C(int, int)`

### Class: `DS_lueqns` | Method: `D`
- **File Path:** `include/dslueqns.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `D()`
  - `D(int, int)`

### Class: `DS_lueqns` | Method: `L`
- **File Path:** `include/dslueqns.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `L(int)`
  - `L(int, int, int)`

### Class: `DS_lueqns` | Method: `Lc`
- **File Path:** `include/dslueqns.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Lc()`
  - `Lc(int)`

### Class: `DS_lueqns` | Method: `X`
- **File Path:** `include/dslueqns.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `X()`
  - `X(int, int)`

### Class: `DS_row_mat` | Method: `DS_row_mat`
- **File Path:** `include/dsmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_row_mat(int, int)`
  - `DS_row_mat(DS_row_mat &)`

### Class: `DS_row_mat` | Method: `Vec_size`
- **File Path:** `include/dsmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Vec_size(int, int)`
  - `Vec_size()`

### Class: `DS_col_mat` | Method: `DS_col_mat`
- **File Path:** `include/dsmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_col_mat(int, int)`
  - `DS_col_mat(DS_col_mat &)`

### Class: `DS_col_mat` | Method: `Vec_size`
- **File Path:** `include/dsmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Vec_size(int, int)`
  - `Vec_size()`

### Class: `DS_diag_mat` | Method: `DS_diag_mat`
- **File Path:** `include/dsmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_diag_mat(int)`
  - `DS_diag_mat(DS_diag_mat &)`

### Class: `DS_diag_mat` | Method: `Size`
- **File Path:** `include/dsmat.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Size(int)`
  - `Size()`

### Class: `DS_mbvec_row_matrix` | Method: `DS_mbvec_row_matrix`
- **File Path:** `include/dsmbrmt.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_mbvec_row_matrix(int, int)`
  - `DS_mbvec_row_matrix(const DS_mbvec_row_matrix &)`

### Class: `DS_mbvec_row_matrix` | Method: `Row`
- **File Path:** `include/dsmbrmt.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Row(int)`
  - `Row(int)`

### Class: `DS_multi_banded_vec` | Method: `Largest_elem`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Largest_elem()`
  - `Largest_elem(const DS_int_block&)`

### Class: `DS_multi_banded_vec` | Method: `operator-=`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator-=(const DS_abs_vec &)`
  - `operator-=(const DS_multi_banded_vec &)`

### Class: `DS_multi_banded_vec` | Method: `Pluseq`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Pluseq(const DS_abs_vec &, double)`
  - `Pluseq(const DS_multi_banded_vec &, double, double)`

### Class: `DS_multi_banded_vec` | Method: `Assign_from`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Assign_from(const DS_abs_vec &, EQ_FLAG)`
  - `Assign_from(const DS_abs_vec &, double, EQ_FLAG)`

### Class: `DS_multi_banded_vec` | Method: `Min`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Min(int)`
  - `Min(int)`

### Class: `DS_multi_banded_vec` | Method: `Max`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Max(int)`
  - `Max(int)`

### Class: `DS_multi_banded_vec` | Method: `Offset`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Offset(int)`
  - `Offset(int)`

### Class: `DS_multi_banded_vec` | Method: `Raise_band_max`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Raise_band_max(int, int)`
  - `Raise_band_max(int, int, double)`

### Class: `DS_multi_banded_vec` | Method: `Lower_band_min`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Lower_band_min(int, int)`
  - `Lower_band_min(int, int, double)`

### Class: `DS_multi_banded_vec` | Method: `Insert_band`
- **File Path:** `include/dsmbvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Insert_band(int, int)`
  - `Insert_band(int, int, double)`

### Class: `DS_reduce_event` | Method: `DS_reduce_event`
- **File Path:** `include/dsrdlog.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_reduce_event()`
  - `DS_reduce_event(int, int, double, int)`

### Class: `DS_row_reducer` | Method: `Apply_log`
- **File Path:** `include/dsreduc.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Apply_log(DS_abs_matrix &)`
  - `Apply_log(DS_abs_vec &)`

### Class: `DS_row_reducer` | Method: `Zero_event`
- **File Path:** `include/dsreduc.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Zero_event(int)`
  - `Zero_event(int, int, double)`

### Class: `DS_qsort_data` | Method: `DS_qsort_data`
- **File Path:** `include/dsstdef.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_qsort_data(double, int)`
  - `DS_qsort_data(DS_qsort_data &)`

### Class: `DS_zone` | Method: `Total_dof_list`
- **File Path:** `include/dszone.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Total_dof_list()`
  - `Total_dof_list(int)`

### Class: `DS_zone` | Method: `Local_dof_list`
- **File Path:** `include/dszone.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Local_dof_list()`
  - `Local_dof_list(int)`

### Class: `DS_zone` | Method: `Elem_list`
- **File Path:** `include/dszone.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Elem_list()`
  - `Elem_list(int)`

### Class: `DS_rect_zone` | Method: `DS_rect_zone`
- **File Path:** `include/dszone.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `DS_rect_zone(DS_pfunc *, double *, double *)`
  - `DS_rect_zone(DS_rect_zone &)`

### Class: `DS_rect_zone` | Method: `Domain_min`
- **File Path:** `include/dszone.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_min(DM_dbl_array&)`
  - `Domain_min()`

### Class: `DS_rect_zone` | Method: `Domain_max`
- **File Path:** `include/dszone.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Domain_max(DM_dbl_array&)`
  - `Domain_max()`

### Class: `HASH_ENTRY_TYPE` | Method: `HASH_ENTRY_TYPE`
- **File Path:** `include/entstch_stitch.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `HASH_ENTRY_TYPE()`
  - `HASH_ENTRY_TYPE(DATA_TYPE*, KEY_TYPE*, logical)`

### Class: `epd_output` | Method: `epd_output`
- **File Path:** `include/epd_output_list_type.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `epd_output()`
  - `epd_output(SPAposition, double, param_info)`

### Class: `area_property` | Method: `operator-`
- **File Path:** `include/faceprop.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator-(area_property const &)`
  - `operator-(area_property const &, area_property const &)`

### Class: `free_list_states` | Method: `get_state_of_all_free_lists`
- **File Path:** `include/freelist.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `get_state_of_all_free_lists()`
  - `get_state_of_all_free_lists()`

### Class: `GC_Wrapper` | Method: `get`
- **File Path:** `include/gc_wrapped.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `get()`
  - `get()`

### Class: `RenderingObject` | Method: `insert_point`
- **File Path:** `include/gen_rendobj.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `insert_point(const SPAposition&, const rgb_color &)`
  - `insert_point(const SPAposition&)`

### Class: `RenderingObject` | Method: `insert_entity`
- **File Path:** `include/gen_rendobj.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `insert_entity(ENTITY*, const SPAtransf *, const rgb_color &)`
  - `insert_entity(ENTITY*, const SPAtransf *)`

### Class: `RenderingObject` | Method: `insert_curve`
- **File Path:** `include/gen_rendobj.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `insert_curve(CURVE*, SPAparameter, SPAparameter, const SPAtransf*, const rgb_color &)`
  - `insert_curve(CURVE*, SPAparameter, SPAparameter, const SPAtransf&)`

### Class: `RenderingObject` | Method: `insert_shaded_triangle_set`
- **File Path:** `include/gen_rendobj.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `insert_shaded_triangle_set(shaded_triangle_set<float> const&)`
  - `insert_shaded_triangle_set(shaded_triangle_set<double> const&)`

### Class: `SchemeView` | Method: `CreateRenderingObject`
- **File Path:** `include/gen_view.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `CreateRenderingObject()`
  - `CreateRenderingObject(RenderingObject*)`

### Class: `SchemeView` | Method: `draw_polyline_3d`
- **File Path:** `include/gen_view.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `draw_polyline_3d(int, const float [], logical)`
  - `draw_polyline_3d(int, const SPAposition [], logical)`

### Class: `unstable_pair` | Method: `unstable_pair`
- **File Path:** `include/hsurf.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `unstable_pair(const unstable_pair &)`
  - `unstable_pair(SURFACE *, SURFACE *)`

### Class: `unstable_pair` | Method: `first`
- **File Path:** `include/hsurf.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `first()`
  - `first()`

### Class: `unstable_pair` | Method: `second`
- **File Path:** `include/hsurf.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `second()`
  - `second()`

### Class: `HH_Unstable_SurfSnap` | Method: `get_matching_nodes`
- **File Path:** `include/hsurf.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `get_matching_nodes(SURFACE*, ENTITY_LIST &)`
  - `get_matching_nodes(const HH_SurfSnap *, ENTITY_LIST &)`

### Class: `HH_Unstable_SurfSnap` | Method: `HH_Unstable_SurfSnap`
- **File Path:** `include/hsurf.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `HH_Unstable_SurfSnap()`
  - `HH_Unstable_SurfSnap(SURFACE *)`

### Class: `SPAinterval` | Method: `operator*`
- **File Path:** `include/interval.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator*(SPAinterval const &, double)`
  - `operator*(double, SPAinterval const &)`

### Class: `iterator` | Method: `iterator`
- **File Path:** `include/iscmpicksub.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `iterator()`
  - `iterator(list_node *)`

### Class: `iterator` | Method: `operator==`
- **File Path:** `include/iscmpicksub.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator==(const iterator &)`
  - `operator==(const list_node *)`

### Class: `reverse_iterator` | Method: `reverse_iterator`
- **File Path:** `include/iscmpicksub.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `reverse_iterator()`
  - `reverse_iterator(list_node *)`

### Class: `reverse_iterator` | Method: `operator==`
- **File Path:** `include/iscmpicksub.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator==(const reverse_iterator &)`
  - `operator==(const list_node *)`

### Class: `const_iterator` | Method: `operator==`
- **File Path:** `include/iscmpicksub.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator==(const const_iterator &)`
  - `operator==(const list_node *)`

### Class: `ISCMPickSubscriberPTR_List` | Method: `begin`
- **File Path:** `include/iscmpicksub.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `begin()`
  - `begin()`

### Class: `ISCMPickSubscriberPTR_List` | Method: `end`
- **File Path:** `include/iscmpicksub.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `end()`
  - `end()`

### Class: `skin_face_border_extractor` | Method: `skin_face_border_extractor`
- **File Path:** `include/isgskin.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `skin_face_border_extractor()`
  - `skin_face_border_extractor(FACE *)`

### Class: `list_stream` | Method: `list_stream`
- **File Path:** `include/list_stream.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `list_stream(list_stream_options*)`
  - `list_stream(const list_stream&)`

### Class: `LOPT_ENTRY` | Method: `LOPT_ENTRY`
- **File Path:** `include/lopt_hash.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `LOPT_ENTRY(LOPT_ENTRY *, void *, void *)`
  - `LOPT_ENTRY()`

### Class: `mass_property` | Method: `operator-`
- **File Path:** `include/massprop.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator-(mass_property const &, mass_property const &)`
  - `operator-(mass_property const &)`

### Class: `SPAposition` | Method: `operator*`
- **File Path:** `include/matrix.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator*(SPAmatrix const &, SPAposition const &)`
  - `operator*(SPAposition const &, SPAmatrix const &)`

### Class: `SPAinterval` | Method: `operator%`
- **File Path:** `include/param.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator%(SPApar_dir const &, SPApar_box const &)`
  - `operator%(SPApar_box const &, SPApar_dir const &)`

### Class: `param_string` | Method: `set`
- **File Path:** `include/parm_str.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `set(const char*, unsigned)`
  - `set(const char*)`

### Class: `param_string` | Method: `operator=`
- **File Path:** `include/parm_str.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator=(const char*)`
  - `operator=(const param_string&)`

### Class: `phlv5_edge` | Method: `phlv5_edge`
- **File Path:** `include/phlv5_edge.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `phlv5_edge()`
  - `phlv5_edge(EDGE*, BODY*, FACE*, phlv5_segment*, float *, int, int, int, int)`

### Class: `phlv5_segment` | Method: `phlv5_segment`
- **File Path:** `include/phlv5_seg.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `phlv5_segment()`
  - `phlv5_segment(SPAinterval const&, Phlv5SegSta, Phlv5SegVis)`

### Class: `rat_poly_vec` | Method: `operator-`
- **File Path:** `include/poly.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator-(rat_poly_vec const &)`
  - `operator-(rat_poly_vec const &, rat_poly_vec const &)`

### Class: `SPAposition` | Method: `operator+`
- **File Path:** `include/position.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator+(SPAposition const &, SPAvector const &)`
  - `operator+(SPAvector const &, SPAposition const &)`

### Class: `safe_base` | Method: `address`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `address(const void*, int)`
  - `address(void)`

### Class: `safe_function_type` | Method: `safe_function_type`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `safe_function_type(const type)`
  - `safe_function_type(const safe_function_type<type>&)`

### Class: `safe_function_type` | Method: `operator&`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator&()`
  - `operator&()`

### Class: `safe_function_type` | Method: `operator=`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator=(const type&)`
  - `operator=(const safe_function_type<type>&)`

### Class: `safe_floating_type` | Method: `safe_floating_type`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `safe_floating_type(const type)`
  - `safe_floating_type(const safe_floating_type<type>&)`

### Class: `safe_floating_type` | Method: `operator=`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator=(const type&)`
  - `operator=(const safe_floating_type<type>&)`

### Class: `safe_floating_type` | Method: `operator++`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator++()`
  - `operator++(int)`

### Class: `safe_floating_type` | Method: `operator--`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator--()`
  - `operator--(int)`

### Class: `safe_integral_type` | Method: `safe_integral_type`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `safe_integral_type(const type&)`
  - `safe_integral_type(const safe_integral_type<type>&)`

### Class: `safe_integral_type` | Method: `operator=`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator=(const type&)`
  - `operator=(const safe_integral_type<type>&)`

### Class: `safe_pointer_type` | Method: `safe_pointer_type`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `safe_pointer_type(type*)`
  - `safe_pointer_type(const safe_pointer_type<type>&)`

### Class: `safe_pointer_type` | Method: `operator&`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator&()`
  - `operator&()`

### Class: `safe_pointer_type` | Method: `operator=`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator=(type*)`
  - `operator=(const safe_pointer_type<type> &)`

### Class: `safe_pointer_type` | Method: `operator++`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator++()`
  - `operator++(int)`

### Class: `safe_pointer_type` | Method: `operator--`
- **File Path:** `include/safe.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator--()`
  - `operator--(int)`

### Class: `restore_progress_data` | Method: `restore_progress_data`
- **File Path:** `include/savres.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `restore_progress_data()`
  - `restore_progress_data(FileInterface *, restore_data *)`

### Class: `scm_shared_ptr` | Method: `scm_shared_ptr`
- **File Path:** `include/scm_shrd_ptr.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `scm_shared_ptr(T*)`
  - `scm_shared_ptr(const scm_shared_ptr<T>&)`

### Class: `scm_shared_ptr` | Method: `operator*`
- **File Path:** `include/scm_shrd_ptr.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator*()`
  - `operator*()`

### Class: `scm_shared_ptr` | Method: `get`
- **File Path:** `include/scm_shrd_ptr.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `get()`
  - `get()`

### Class: `scm_shared_ptr` | Method: `operator->`
- **File Path:** `include/scm_shrd_ptr.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator->()`
  - `operator->()`

### Class: `SPAposition_cloud` | Method: `read_position_cloud_from_file`
- **File Path:** `include/SPAposition_cloud.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `read_position_cloud_from_file(FILE*)`
  - `read_position_cloud_from_file(const char*)`

### Class: `DerivedFromSPAUseCounted_sptr` | Method: `DerivedFromSPAUseCounted_sptr`
- **File Path:** `include/SPAUseCounted.h`
- **Overload Count:** 2
- **Signatures:**
  - `DerivedFromSPAUseCounted_sptr(DerivedFromSPAUseCounted*)`
  - `DerivedFromSPAUseCounted_sptr()`

### Class: `DerivedFromSPAUseCounted_sptr` | Method: `operator*`
- **File Path:** `include/SPAUseCounted.h`
- **Overload Count:** 2
- **Signatures:**
  - `operator*()`
  - `operator*()`

### Class: `DerivedFromSPAUseCounted_sptr` | Method: `operator->`
- **File Path:** `include/SPAUseCounted.h`
- **Overload Count:** 2
- **Signatures:**
  - `operator->()`
  - `operator->()`

### Class: `DerivedFromSPAUseCounted_sptr` | Method: `get`
- **File Path:** `include/SPAUseCounted.h`
- **Overload Count:** 2
- **Signatures:**
  - `get()`
  - `get()`

### Class: `subGrid` | Method: `subGrid`
- **File Path:** `include/spd3rtn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `subGrid()`
  - `subGrid(int, int, int, int, GRID *)`

### Class: `subGrid` | Method: `intersects`
- **File Path:** `include/spd3rtn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `intersects(CHORDS &, SPAbox const &, double const &, clash_check_type const &, logical&)`
  - `intersects(subGrid*, double const&, logical&)`

### Class: `summary_bs3_surface` | Method: `summary_bs3_surface`
- **File Path:** `include/spldef.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `summary_bs3_surface(int, double*, int, double*)`
  - `summary_bs3_surface(const summary_bs3_surface&)`

### Class: `bs3_surface` | Method: `bs3_surface_proc`
- **File Path:** `include/sps3srtn.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `bs3_surface_proc(SPAinterval&, SPAinterval&, pt_eval_fn_t, vec_eval_fn_t, vec_eval_fn_t, vec_eval_fn_t, void*, double)`
  - `bs3_surface_proc(int, double*, int, double*, pt_eval_fn_t, vec_eval_fn_t, vec_eval_fn_t, vec_eval_fn_t, void*, double, int, int&)`

### Class: `bezier_segment` | Method: `eval`
- **File Path:** `include/sw_common.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `eval(double, SPAvector &)`
  - `eval(double, SPAposition &)`

### Class: `spiral_display` | Method: `display_entities`
- **File Path:** `include/test_utl.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `display_entities(ENTITY*, logical, double)`
  - `display_entities(ENTITY_LIST&, logical, double)`

### Class: `acis_test_unit` | Method: `handle_entity`
- **File Path:** `include/test_utl.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `handle_entity(outcome const&, ENTITY*, int, logical, double)`
  - `handle_entity(ENTITY*, int, logical, double)`

### Class: `acis_test_unit` | Method: `handle_entities`
- **File Path:** `include/test_utl.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `handle_entities(outcome const&, ENTITY_LIST&, int*, int, logical, double)`
  - `handle_entities(ENTITY_LIST&, int*, int, logical, double)`

### Class: `Node_Pair` | Method: `Node_Pair`
- **File Path:** `include/tganasnp.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `Node_Pair()`
  - `Node_Pair(HH_GNode *)`

### Class: `SPAposition` | Method: `operator*`
- **File Path:** `include/unitvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator*(SPAposition const &, SPAunit_vector const &)`
  - `operator*(SPAunit_vector const &, SPAposition const &)`

### Class: `SPAunit_vector` | Method: `operator*`
- **File Path:** `include/unitvec.hxx`
- **Overload Count:** 2
- **Signatures:**
  - `operator*(SPAunit_vector const &, SPAtransf const &)`
  - `operator*(SPAunit_vector const &, SPAtransf const *)`

### Class: `vgl_Bitmap` | Method: `vgl_Bitmap`
- **File Path:** `include/vgl/bitmap.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_Bitmap(void)`
  - `vgl_Bitmap(void)`

### Class: `vgl_DataBuf` | Method: `vgl_DataBuf`
- **File Path:** `include/vgl/databuf.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_DataBuf(void)`
  - `vgl_DataBuf(void)`

### Class: `vgl_DFile` | Method: `vgl_DFile`
- **File Path:** `include/vgl/dfile.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_DFile(void)`
  - `vgl_DFile(void)`

### Class: `vgl_Direct3DDev` | Method: `vgl_Direct3DDev`
- **File Path:** `include/vgl/direct3ddev.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_Direct3DDev(void)`
  - `vgl_Direct3DDev(void)`

### Class: `vgl_DList` | Method: `vgl_DList`
- **File Path:** `include/vgl/dlist.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_DList(void)`
  - `vgl_DList(void)`

### Class: `vgl_DMap` | Method: `vgl_DMap`
- **File Path:** `include/vgl/dmap.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_DMap(void)`
  - `vgl_DMap(void)`

### Class: `vgl_DOpt` | Method: `vgl_DOpt`
- **File Path:** `include/vgl/dopt.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_DOpt(void)`
  - `vgl_DOpt(void)`

### Class: `vgl_DrawFun` | Method: `vgl_DrawFun`
- **File Path:** `include/vgl/drawfun.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_DrawFun(void)`
  - `vgl_DrawFun(void)`

### Class: `vgl_DrawIPC` | Method: `vgl_DrawIPC`
- **File Path:** `include/vgl/drawipc.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_DrawIPC(void)`
  - `vgl_DrawIPC(void)`

### Class: `vgl_DTee` | Method: `vgl_DTee`
- **File Path:** `include/vgl/dtee.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_DTee(void)`
  - `vgl_DTee(void)`

### Class: `vgl_FBuffer` | Method: `vgl_FBuffer`
- **File Path:** `include/vgl/fbuffer.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_FBuffer(void)`
  - `vgl_FBuffer(void)`

### Class: `vgl_GDIDev` | Method: `vgl_GDIDev`
- **File Path:** `include/vgl/gdidev.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_GDIDev(void)`
  - `vgl_GDIDev(void)`

### Class: `vgl_IActor` | Method: `vgl_IActor`
- **File Path:** `include/vgl/iactor.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_IActor(void)`
  - `vgl_IActor(void)`

### Class: `vgl_OpenGLDev` | Method: `vgl_OpenGLDev`
- **File Path:** `include/vgl/opengldev.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_OpenGLDev(void)`
  - `vgl_OpenGLDev(void)`

### Class: `vgl_OpenGLDev` | Method: `BestVisualX`
- **File Path:** `include/vgl/opengldev.h`
- **Overload Count:** 2
- **Signatures:**
  - `BestVisualX(Visual**)`
  - `BestVisualX(void**)`

### Class: `vgl_Pixelmap` | Method: `vgl_Pixelmap`
- **File Path:** `include/vgl/pixelmap.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_Pixelmap(void)`
  - `vgl_Pixelmap(void)`

### Class: `vgl_Popup` | Method: `vgl_Popup`
- **File Path:** `include/vgl/popup.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_Popup(void)`
  - `vgl_Popup(void)`

### Class: `vgl_Quadric` | Method: `vgl_Quadric`
- **File Path:** `include/vgl/quadric.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_Quadric(void)`
  - `vgl_Quadric(void)`

### Class: `vgl_RasFont` | Method: `vgl_RasFont`
- **File Path:** `include/vgl/rasfont.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_RasFont(void)`
  - `vgl_RasFont(void)`

### Class: `vgl_RendBuf` | Method: `vgl_RendBuf`
- **File Path:** `include/vgl/rendbuf.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_RendBuf(void)`
  - `vgl_RendBuf(void)`

### Class: `vgl_SVGDev` | Method: `vgl_SVGDev`
- **File Path:** `include/vgl/svgdev.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_SVGDev(void)`
  - `vgl_SVGDev(void)`

### Class: `vgl_Texture` | Method: `vgl_Texture`
- **File Path:** `include/vgl/texture.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_Texture(void)`
  - `vgl_Texture(void)`

### Class: `vgl_X11Dev` | Method: `vgl_X11Dev`
- **File Path:** `include/vgl/x11dev.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_X11Dev(void)`
  - `vgl_X11Dev(void)`

### Class: `vgl_X11Dev` | Method: `BestVisualX`
- **File Path:** `include/vgl/x11dev.h`
- **Overload Count:** 2
- **Signatures:**
  - `BestVisualX(Visual**)`
  - `BestVisualX(void**)`

### Class: `vgl_Xfm` | Method: `vgl_Xfm`
- **File Path:** `include/vgl/xfm.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_Xfm(void)`
  - `vgl_Xfm(void)`

### Class: `vgl_Xfmstack` | Method: `vgl_Xfmstack`
- **File Path:** `include/vgl/xfmstack.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_Xfmstack(void)`
  - `vgl_Xfmstack(void)`

### Class: `vgl_ZBuffer` | Method: `vgl_ZBuffer`
- **File Path:** `include/vgl/zbuffer.h`
- **Overload Count:** 2
- **Signatures:**
  - `vgl_ZBuffer(void)`
  - `vgl_ZBuffer(void)`

