import redis
import random




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





r = redis.Redis(host='localhost', port=6379, db=0)

write_loader = RedisLoader()
write_loader.load_script(r, 'writefile.lua')
write_loader.get_script_instance()(keys=['buffermap', 'bufferlist'], args=[878979, 0])
