"""Apply grades.json to the built film with the HyperFrames media-treatment tool. Run after build_film.py."""
import json, subprocess, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g = json.load(open(os.path.join(root, 'grades.json')))
for name, look in g.items():
    sel = ', '.join(f'#v-{k}' for k in look['shots'])
    r = subprocess.run(['npx', 'hyperframes', 'media-treatment', '--selector', sel, '--grading', json.dumps(look['grading']), '--apply', '--json'],
                       cwd=os.path.join(root, 'film'), capture_output=True, text=True)
    d = json.loads(r.stdout[r.stdout.index('{'):])
    print(name, 'ok' if d.get('ok') else d, 'clips:', d.get('count'))
