local totalToGrab = tonumber(ARGV[1])
local retv = {}
local counter = 0

-- return nothing if the list has nothing in it
if redis.call('LLEN', KEYS[2]) == 0 then
    return retv
end

-- get time in seconds
local t = redis.call('TIME')[1]

-- loop until we either hit a timestamp that's too new or we hit the max values
while(true)
do

    -- break if the list has nothing in it
    if redis.call('LLEN', KEYS[2]) == 0 then
        break
    end

    -- look at first item in the list
    local listHeadValue = redis.call('LRANGE', KEYS[2], 0, 0)[1]

    -- see if the timestamp of the value is <= then the current time
    if redis.call('HGET', KEYS[1], listHeadValue) <= t then

        -- see if the item exists in the map, it should unless there was an error on write
        if redis.call('HEXISTS', KEYS[1], listHeadValue) == 1 then

            -- set the item in the return value
            retv[counter + 1] = listHeadValue

            -- remove from list
            redis.call('LPOP', KEYS[2])

            -- remove from map
            redis.call('HDEL', KEYS[1], listHeadValue)

        -- if it's not in the map there was a write error, but this shouldn't lock up processing and we'll just throw this away
        else
            -- remove from list
            redis.call('LPOP', KEYS[2])

            -- remove from map
            redis.call('HDEL', KEYS[1], listHeadValue)
        end

    -- otherwise, break out
    else
        break
    end

    counter = counter + 1

    -- break if we've hit the max amount of items
    if counter == totalToGrab then
        break
    end

end

return retv
