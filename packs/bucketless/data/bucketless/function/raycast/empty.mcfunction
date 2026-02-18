# Check if hit a replaceable block, excluding lava
execute unless block ~ ~ ~ #minecraft:air unless block ~ ~ ~ minecraft:lava unless block ~ ~ ~ minecraft:lava_cauldron run function bucketless:water/place
# Check if hit any lava
execute if block ~ ~ ~ minecraft:lava run function bucketless:lava/use
execute if block ~ ~ ~ minecraft:lava_cauldron run function bucketless:lava/use
# Raycast further if we are still hitting air
execute if block ~ ~ ~ #minecraft:air positioned ^ ^ ^0.1 if entity @s[distance=..5] run function bucketless:raycast/empty