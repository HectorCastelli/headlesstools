# Play effects
playsound minecraft:entity.generic.burn player @s ~ ~ ~ 1 1
particle smoke ~ ~ ~ ~ ~ ~ 1 10
# Boil the mainhand (priority) or the offhand
execute if items entity @s weapon.offhand *[minecraft:custom_data~{bucketless:true,full:true}] unless items entity @s weapon.mainhand *[minecraft:custom_data~{bucketless:true,full:true}] run item modify entity @s weapon.offhand bucketless:empty_water
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bucketless:true,full:true}] run item modify entity @s weapon.mainhand bucketless:empty_water