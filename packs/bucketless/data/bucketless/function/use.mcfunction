# Reset advancement for detection
advancement revoke @s only bucketless:try_use
# Check if we can fill it
execute if entity @s[scores={use_cooldown_count=0}] if items entity @s weapon.* *[minecraft:custom_data~{bucketless:true,full:false}] at @s anchored eyes positioned ^ ^ ^0.1 run function bucketless:raycast/fill
# Reset the cooldown if needed
execute if entity @s[scores={use_cooldown_count=0}] run function bucketless:cooldown/apply