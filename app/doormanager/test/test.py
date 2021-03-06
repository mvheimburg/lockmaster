import os, sys
import yaml




def main():

    cfg = None
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_dir, "config.yaml")
    with open(path, 'r') as stream:
        cfg = yaml.load(stream, Loader=yaml.FullLoader)


    print(cfg)


# Tests
if __name__ == '__main__':
    main()
