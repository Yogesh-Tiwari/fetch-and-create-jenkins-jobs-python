from utils import *

def get_plugins(server: jenkins.Jenkins) -> List[Dict]:
    return server.get_plugins()

def install_plugins(server: jenkins.Jenkins, plugins: List) -> None:
    for plugin in plugins:
        # (python-jenkins version 1.8.2) Edit the files specified in the PR to resolve the issue with installing plugins: https://review.opendev.org/c/jjb/python-jenkins/+/719059.
        # To find the installed plugin path, we need to use the following command: "pip show python-jenkins" and refer to Location in the output.
        server.install_plugin(plugin, include_dependencies=True)

def main():
    config = load_config('secrets/secret.json')
    server = connect_to_jenkins(config, skip_ssl_verification=False)
    install_plugins(server, config.get('plugins', []))

if __name__ == "__main__":
    main()