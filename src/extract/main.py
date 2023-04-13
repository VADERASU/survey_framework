from extract import utils

if __name__ == "__main__":
    parser = utils.build_parser()
    args = parser.parse_args()
    dir = utils.check_args(args)
    metadata = utils.load_toml(dir)
