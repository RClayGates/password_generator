# import: std

# import: non-std

# import: local
import rc_cache
# from rc_logger import logger
from Gui import rc_gui

# const/global


# main
def main():
    app = rc_gui.PwgenApp(generate = rc_cache.generate_hashes, 
                          add = rc_cache.add_hash_components, 
                          remove = rc_cache.del_hash_components,
                          regen = rc_cache.update_hash_components)
    app.run()
    pass

# code blocks

# main-line logic
if __name__ == '__main__':
    main()