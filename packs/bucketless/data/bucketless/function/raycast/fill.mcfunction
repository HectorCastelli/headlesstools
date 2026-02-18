# Check if hit a source of water
execute if block ~ ~ ~ minecraft:water[level=0] run function bucketless:water/fill
# Check if hit any lava
execute if block ~ ~ ~ minecraft:lava run function bucketless:lava/fill
# Raycast further if we are still hitting air
execute if block ~ ~ ~ #minecraft:air positioned ^ ^ ^0.1 if entity @s[distance=..5] run function bucketless:raycast/fill