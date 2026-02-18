# Check all full buckets that can still leak
execute as @a[predicate=bucketless:has_leaking] run function bucketless:leak/damage
# Check all full buckets that have leaked to the end
execute as @a[predicate=bucketless:has_leaked] run function bucketless:leak/break
