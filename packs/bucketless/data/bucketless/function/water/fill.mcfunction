# Replace target block with air
setblock ~ ~ ~ minecraft:air
# Fill the mainhand (priority) or the offhand with water
execute if items entity @s weapon.offhand *[minecraft:custom_data~{bucketless:true,full:false}] unless items entity @s weapon.mainhand *[minecraft:custom_data~{bucketless:true,full:false}] run item modify entity @s weapon.offhand bucketless:fill_water
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bucketless:true,full:false}] run item modify entity @s weapon.mainhand bucketless:fill_water