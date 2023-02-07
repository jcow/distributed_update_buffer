import redis
import random
import time




def sleep_and_log(t):
    print("sleeping for {}s".format(t))
    time.sleep(t)

class RedisLoader:

    def __init__(self):
        self._script_instance = None

    def load_script(self, r, filepath):
        script_contents = ""
        with open(filepath) as f:
            script_contents = f.read()

        self._script_instance = r.register_script(script_contents)

    def get_script_instance(self):
        return self._script_instance





r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

write_loader = RedisLoader()
write_loader.load_script(r, 'writefile.lua')

read_loader = RedisLoader()
read_loader.load_script(r, 'readfile.lua')

"""
Test 1 to see if overlapping makes sense
"""

print("Test 1")

write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[11111, 0])
write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[11111, 5])
write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[11111, 6])
write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[22222, 0])

write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[33333, 6])
write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[33333, 7])

sleep_and_log(2)

first_vals = read_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[10])

print(first_vals)
assert len(first_vals) == 2
assert first_vals[0] == '11111'
assert first_vals[1] == '22222'

sleep_and_log(6)
second_vals = read_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[10])

print(second_vals)
assert len(second_vals) == 1
assert second_vals[0] == '33333'



"""
Test 2 to see if the get parameter will return the correct max amount
"""

print("Test 2")

write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[11111, 0])
write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[22222, 0])
write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[33333, 0])
write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[44444, 0])
write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[55555, 0])

vals = read_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[3])
print(vals)
assert len(vals) == 3

vals = read_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[3])
print(vals)
assert len(vals) == 2
