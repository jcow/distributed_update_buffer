-- if the map already has as key, then skip
if redis.call('HEXISTS', KEYS[1], ARGV[1]) == 0 then

    -- get time in seconds
    local t = redis.call('TIME')[1]

    -- add to the redis set
    redis.call('HSET', KEYS[1], ARGV[1], t + tonumber(ARGV[2]))

    -- add to the processing list
    redis.call('RPUSH', KEYS[2], ARGV[1])

    -- return 1 if added
    return 1
end

-- return 0 if not added
return 0
