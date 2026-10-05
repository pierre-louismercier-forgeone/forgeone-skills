# ForgeOne Skills

Skills Claude de l'équipe ForgeOne. Un dossier par skill dans `skills/`.

## Installer un skill

```bash
git clone https://github.com/pierre-louismercier-forgeone/forgeone-skills.git
cp -R forgeone-skills/skills/forgeone-discovery-audit ~/.claude/skills/
```

Puis relancer Claude Code ou l'app Claude.

## Skills disponibles

| Skill | Usage |
|---|---|
| `forgeone-discovery-audit` | Mini audit avant un appel de découverte : trafic vs concurrents, projection de ventes ou de devis, one pager HTML à partager en écran. Nécessite le connecteur DataForSEO et Python 3. |

## Mettre à jour

```bash
cd forgeone-skills && git pull
cp -R skills/forgeone-discovery-audit ~/.claude/skills/
```
