import argparse
from handler.proxy_handler import renew_proxy_list


def get_terminal_arguments():
    default_output = "./output/proxy_list.json"

    githubRepo = "https://github.com/nicolasSchirmer/proxy-scrap3r"
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="A simple proxy list scraper tool:\n"
                    "Github repository: " + githubRepo)

    parser.add_argument('-jf', dest="json_file_output", required=False,
                        help="Json file output path. (it's optional)\n\n"
                             "Need to be a .json file.\n"
                             "The default is " + default_output + "\n",
                        type=str, default=default_output)

    return parser.parse_args()


if __name__ == '__main__':
    print("""
       ||||||  ||||||  |||||||  ||    ||  ||    ||
       ||  ||  ||  ||  ||   ||   ||  ||    ||  ||
       |||||   |||||   ||   ||     ||        ||
       ||      || |    ||   ||   ||  ||      ||
       ||      ||  ||  |||||||  ||    ||     ||
       ==========================================
        ===   +++  ]]]]   #   $$$ @@@@@  *****
         === +     ]]]   ###  $$$   @@@  *****
        ===   +++  ]  ] #  #  $   @@@@@  *   *
       ==========================================
       ---- A simple proxy list scraper tool ----
       ==========================================
       """)

    args = get_terminal_arguments()
    renew_proxy_list(args.json_file_output)
