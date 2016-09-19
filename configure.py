import yaml

config_dir = "config"

def main():
    parse()


def parse():
    try:
        left_index = int(raw_input('Enter index of left camera: '))
    except ValueError:
        print "Please enter a number."

    try:
        right_index = int(raw_input('Enter index of right camer: '))
    except ValueError:
        print "Please enter a number."

    generate_yaml(left_index, right_index)


def generate_yaml(left_ix, right_ix):
    settings = {
            'left-index': left_ix,
            'right-index': right_ix
            }
    with open(config_dir + '/profile.yml', 'w') as file:
        yaml.dump(settings, file, default_flow_style=False)

if __name__ == "__main__":
    main()
