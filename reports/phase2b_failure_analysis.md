# Phase 2B Failure Analysis

## 1. Root Problem: ExternalClass Explosion
The explosion in ExternalClass nodes (from 28 to 135) is caused by the exact-string lookup strategy in `name_to_id`. When a class is declared as `MyClass`, it is mapped under that exact string. However, method implementations and inheritance declarations often use namespace prefixes (e.g., `Namespace::MyClass`) or template arguments (e.g., `MyClass<int>`). The strict dictionary lookup fails to match these variations, causing the script to incorrectly assume they are `ExternalClass` definitions.

### Sample Classes incorrectly classified as ExternalClass
- `shaded_triangle_set`
- `CATCGMVirtual`
- `CATCGMJournal`
- `to_char`
- `move_corner_result`
- `__releaser__CGM`
- `to_octet`
- `from_octet`
- `meshgems_real`
- `from_boolean`

## 2. Audit: Function Ingestion
- **Expected Total Functions:** 30833
- **Unique Functions Created:** 27379
- **Skipped Functions (Nodes Lost):** 3454
- **Duplicate IDs:** 1454
- **Missing/Malformed Signatures (estimated due to empty types):** 0

*Reason for skipped functions:* The parser sometimes extracts identically named functions in the same file with identical signatures (or failed parameter parsing resulting in empty signatures). Because the ID is hashed as `path::name::signature`, these overloads produce the exact same hash, overwriting each other.

## 3. Audit: Method Ingestion
- **Total Method Definitions Seen:** 6554
- **Unique Method Nodes Created:** 6486
- **Skipped Methods (Overload Collisions):** 68
- **Lookup/Class Resolution Failures:** 3192

## 4. Why Methods = 6486, HAS_METHOD = 3294
There are 6486 valid `Method` nodes created. However, because 3192 of these methods failed to resolve their parent class in the `name_to_id` dictionary (due to namespace/template mismatch), they were diverted to the `external_method_batch`. As a result, these 3192 methods established `HAS_METHOD` edges with newly minted `ExternalClass` nodes instead of proper internal `Class` nodes. If you measure the `HAS_METHOD` edges connecting proper internal classes to methods (e.g. `MATCH (c:Class)-[:HAS_METHOD]->(m)`), the count comes out to exactly 3294 (6486 total - 3192 misrouted = 3294 valid internal edges).

## 5. Recommended Fixes
1. **Implement Robust Name Normalization:** Strip namespace prefixes and template arguments when performing `class_name` lookups in `name_to_id` to ensure methods map correctly to their base classes.
2. **Include Line Numbers in Hash:** To prevent function/method overload loss, append the `line_number` to the `raw_id` generation logic (e.g., `f"{path}::{name}::{signature}::{line_number}"`).
