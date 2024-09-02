#!/usr/bin/env bash

pip install -r requirements.txt

maturin build --release --sdist --no-default-features --features "poke-engine/gen4,poke-engine/last_used_move,poke-engine/damage_dealt" --out dist/gen4
maturin build --release --sdist --no-default-features --features "poke-engine/gen5,poke-engine/last_used_move,poke-engine/damage_dealt" --out dist/gen5
maturin build --release --sdist --no-default-features --features "poke-engine/gen6,poke-engine/last_used_move,poke-engine/damage_dealt" --out dist/gen6
maturin build --release --sdist --no-default-features --features "poke-engine/gen7,poke-engine/last_used_move,poke-engine/damage_dealt" --out dist/gen7
maturin build --release --sdist --no-default-features --features "poke-engine/gen8,poke-engine/last_used_move,poke-engine/damage_dealt" --out dist/gen8
