from utils import *

def get_plugins(server: jenkins.Jenkins) -> List[Dict]:
    return server.get_plugins()

def install_plugins(server: jenkins.Jenkins, plugins: List) -> None:
    for plugin in plugins:
        # https://review.opendev.org/c/jjb/python-jenkins/+/719059 (install plugins error resolved PR link).
        # To find the installed plugin path, we need to use the following command: pip show python-jenkins.
        server.install_plugin(plugin, include_dependencies=True)

def main():
    config = load_config('secrets/secret.json')
    server = connect_to_jenkins(config, skip_ssl_verification=False)
    install_plugins(server, config.get('plugins', []))

if __name__ == "__main__":
    main()