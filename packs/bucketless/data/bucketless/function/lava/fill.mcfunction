# Play effects
playsound minecraft:entity.generic.burn player @s ~ ~ ~ 1 1
particle smoke ~ ~ ~ ~ ~ ~ 1 30
# Burn the mainhand (priority) or the offhand
execute if items entity @s weapon.offhand *[minecraft:custom_data~{bucketless:true,burn:true}] unless items entity @s weapon.mainhand *[minecraft:custom_data~{bucketless:true,burn:true}] run item replace entity @s weapon.offhand with minecraft:coal
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bucketless:true,burn:true}] run item replace entity @s weapon.mainhand with minecraft:coal