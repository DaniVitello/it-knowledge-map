import yaml, sys
sys.path.insert(0, ".")
import registry
cfg = yaml.safe_load(open("config.yaml"))
cs = registry.load_concepts(cfg["vault_path"], cfg)
areas = sorted(set(c.area for c in cs))
for a in areas:
    count = sum(1 for c in cs if c.area == a)
    print(f"{a} | {count}")
