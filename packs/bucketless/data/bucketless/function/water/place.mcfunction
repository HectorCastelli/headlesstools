execute positioned ^ ^ ^ align xyz run setblock ~ ~ ~ minecraft:water
# Empty the mainhand (priority) or the offhand
execute if items entity @s weapon.offhand *[minecraft:custom_data~{bucketless:true,full:true}] unless items entity @s weapon.mainhand *[minecraft:custom_data~{bucketless:true,full:true}] run item modify entity @s weapon.offhand bucketless:empty_water
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bucketless:true,full:true}] run item modify entity @s weapon.mainhand bucketless:empty_water