import Lake
open Lake DSL

package leap

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.21.0"

lean_lib «Putnam-2025» where
  srcDir := "solutions"
  globs := #[.submodules `«Putnam-2025»]

lean_lib «LEAN-IMO-Bench» where
  srcDir := "solutions"
  globs := #[.submodules `«LEAN-IMO-Bench»]

lean_lib «Open-Problems» where
  srcDir := "solutions"
  globs := #[.submodules `«Open-Problems»]

@[default_target]
lean_lib LeapAll where
  srcDir := "solutions"
  globs := #[.submodules `«Putnam-2025», .submodules `«LEAN-IMO-Bench», .submodules `«Open-Problems»]
