# Reset advancement for detection
advancement revoke @s only bucketless:try_use_full
scoreboard players list @s
# Check if we can empty it
execute if entity @s[scores={use_cooldown_count=0}] if items entity @s weapon.* *[minecraft:custom_data~{bucketless:true,full:true}] at @s anchored eyes positioned ^ ^ ^0.1 run function bucketless:raycast/empty
# Reset the cooldown if needed
execute if entity @s[scores={use_cooldown_count=..0}] run function bucketless:cooldown/apply
scoreboard players list @s