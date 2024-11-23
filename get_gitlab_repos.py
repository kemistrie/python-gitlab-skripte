import warnings
import argparse
import gitlab
import urllib3

# SSL-Warnungen unterdrücken
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

def get_all_projects(gl, group_id):
    try:
        group = gl.groups.get(group_id)
        projects = group.projects.list(include_subgroups=True, all=True)
        print(f"\nProjekte in Gruppe {group.name} (ID: {group_id}) und Untergruppen:")
        print("-" * 50)
        for project in sorted(projects, key=lambda x: x.path_with_namespace):
            print(f"- {project.path_with_namespace}")
        print(f"\nGesamt: {len(projects)} Projekte gefunden")
    except gitlab.exceptions.GitlabAuthenticationError:
        print("Authentifizierung fehlgeschlagen: Ungültiger Token")
    except gitlab.exceptions.GitlabGetError:
        print(f"Fehler: Gruppe mit ID {group_id} nicht gefunden")
    except gitlab.exceptions.GitlabError as e:
        print(f"GitLab-spezifischer Fehler: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='GitLab Projekte auflisten')
    parser.add_argument('--url', required=True, help='GitLab URL')
    parser.add_argument('--group-id', required=True, type=int, help='Gruppen-ID')
    parser.add_argument('--token', required=True, help='OAuth Token')
    args = parser.parse_args()

    gl = gitlab.Gitlab(args.url, oauth_token=args.token, ssl_verify=False)
    try:
        gl.auth()
        get_all_projects(gl, args.group_id)
    except gitlab.exceptions.GitlabError as e:
        print(f"Verbindungsfehler: {str(e)}")

if __name__ == "__main__":
    main()
