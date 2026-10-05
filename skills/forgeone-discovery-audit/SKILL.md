---
name: forgeone-discovery-audit
description: >-
  Mini-audit SEO express AVANT un call de vente/discovery ForgeOne. Léger et token-économe
  (l'inverse de l'Audit Croissance 360) : on arrive au call avec une petite preuve concrète
  créée en analysant le site du prospect (ce qui ne va pas), son marché et ses concurrents,
  pour ancrer le Cost of Inaction / ROI. Calcule le delta de trafic vs les meilleurs acteurs
  du marché + une estimation du CA manqué, confronte le prospect à ses concurrents, et sort
  UN one-pager HTML screen-shareable pendant l'appel. Gère deux cas : le prospect a un site,
  ou il n'en a pas encore (moyennes marché + potentiel, ouverture pour vendre un site).
  Use when PL/le commercial veut « un mini-audit avant un call », « un audit discovery »,
  « préparer un call de vente », « le Cost of Inaction d'un lead », « confronter un prospect à
  ses concurrents », ou avant un rendez-vous de closing. Français par défaut. Nécessite DataForSEO ;
  dégrade sur le web public si absent.
---

# ForgeOne — Discovery Audit (mini-audit pré-call)

Une arme de vente, pas un livrable client. En quelques minutes et **peu de tokens**, on arrive au call avec une **preuve tangible** qui rend le SEO palpable et ancre le **Cost of Inaction** :

> « Les meilleurs de votre marché font X de trafic/mois. Vous êtes à Y. Ce delta, converti, c'est ~Z €/mois — et ça fait N mois que ça dure. »

Ce n'est **pas** l'[Audit Croissance 360](../forgeone-audit-360/SKILL.md). C'est sa version **discovery** : shallow, rapide, bon marché, orientée closing. Le 360, c'est ce qu'on vend *après*.

---

## Philosophie (à ne jamais oublier)

- **Léger et borné.** Objectif : ~5 à 10 appels DataForSEO **maximum**, endpoints Labs (base de données) uniquement, pas de live SERP en boucle, **aucun sous-agent, aucun fan-out**. Si ça devient lourd, c'est qu'on fait le 360 par erreur.
- **Une preuve, pas un rapport.** Le but est UN chiffre choc (le COI) + UN benchmark concurrents + 3-5 points qui clochent. Rien de plus.
- **Honnête et défendable.** Le trafic est estimé (DataForSEO), on le dit. Les hypothèses de conversion/panier sont affichées. On ne survend pas un chiffre qu'on ne peut pas tenir.
- **Confronter aux concurrents.** C'est le levier émotionnel n°1 en call (« qu'est-ce que font mes concurrents ? »). Toujours nommer 2-4 concurrents réels.

---

## Inputs

Demander/collecter le minimum. Ce qui manque, on l'infère et on l'étiquette.

| Champ | Notes |
|-------|-------|
| `prospect` | Nom du lead / de la marque. |
| `url` | Site du prospect — **ou `aucun`** s'il n'a pas encore de site (cas Qibi). |
| `market` | Niche + pays/langue (ex. « miel protéiné sportifs, France »). |
| `competitors` | 2-4 concurrents (noms + domaines) si connus ; sinon on les découvre. |
| `value_per_conversion` | € par lead OU panier moyen (AOV). Si inconnu : demander au commercial, ou estimer + flaguer. |
| `conversion_rate` | Son taux réel (à demander en découverte) en priorité ; sinon une fourchette sourcée ; sinon vide (jamais inventé). Voir `references/coi-model.md`, section projection de conversion. |
| `months_stagnant` | Depuis combien de temps le lead stagne en SEO (sorti de la qualif). Défaut 6. |
| `objective` | L'objectif chiffré que le lead s'est fixé (pour le recadrer vs le marché). |

Si `value_per_conversion` est vraiment introuvable → sortir le **delta de trafic seul** et laisser un emplacement `[valeur/lead]` à remplir en live.

---

## Workspace

Sortie unique sur le Desktop :

```
~/Desktop/Discovery-{prospect-slug}/
  data.json            les chiffres collectés + le calcul COI
  Discovery-{prospect}.html   le one-pager screen-shareable
```

---

## Pipeline (4 phases courtes)

```
PHASE 1  Cadrage        prospect, marché, concurrents, valeur économique, mode site/no-site
PHASE 2  Pull data      DataForSEO borné : trafic prospect + trafic concurrents + moyenne marché
PHASE 3  Diagnostic+COI 3-5 points site (si site) + calcul Cost of Inaction (delta trafic + €)
PHASE 4  One-pager      build_onepager.py → Discovery-{prospect}.html
```

Lire `references/data-pulls.md` (Phase 2) et `references/coi-model.md` (Phase 3) au moment de ces phases.

### Phase 1 — Cadrage
Normaliser les inputs. Déterminer le **mode** : `site` (le prospect a une URL) ou `no-site` (il n'en a pas). Confirmer la valeur économique (`value_per_conversion`) — c'est elle qui rend le COI tangible.

### Phase 2 — Pull data (borné)
Lire `references/data-pulls.md`. Résumé :
- **Mode site :** `dataforseo_labs_google_domain_rank_overview` sur le domaine du prospect (trafic organique estimé + nb mots-clés). `dataforseo_labs_google_competitors_domain` pour trouver les vrais concurrents SEO. Puis `domain_rank_overview` sur **3-4 concurrents** (les meilleurs). C'est tout pour le trafic.
- **Mode no-site :** identifier 3-5 leaders du marché (SERP sur le head term + `competitors_domain`), puis `domain_rank_overview` sur chacun.
- Optionnel (contexte) : volume du/des head terms via `dataforseo_labs_google_keyword_overview` (1 appel groupé).
- **Moyenne marché** = moyenne du trafic des concurrents analysés (entre le plus gros et les plus petits).
Écrire les chiffres bruts dans `data.json`.

### Phase 3 — Diagnostic site + Cost of Inaction
Lire `references/coi-model.md`.
- **Diagnostic (mode site uniquement, léger) :** 1 appel `on_page_lighthouse` OU `on_page_instant_pages` sur la home → sortir **3 à 5 points qui clochent**, punchy et compréhensibles par un non-SEO (ex. « site lent : 4,2 s de chargement », « invisible sur vos requêtes argent », « pas de pages qui répondent aux questions d'achat »). Pas d'audit technique exhaustif.
- **COI :** appliquer le modèle (delta trafic × conversion × valeur → CA manqué/mois → × mois stagnants = COI cumulé). Recadrer l'objectif du lead vs le marché.
- **Projection de conversion :** remplir `conversion_projection` (taux réel du prospect, sinon fourchette sourcée, sinon vide). Même taux pour le prospect et les concurrents, jamais un taux « estimé » par concurrent. Le one-pager en tire les ventes ou demandes de devis par mois.
Écrire le tout dans `data.json`.

### Phase 4 — One-pager
Assembler `data.json` (schéma dans `references/coi-model.md`) puis :
```bash
python3 scripts/build_onepager.py ~/Desktop/Discovery-{prospect-slug}
```
Vérifier qu'il s'ouvre. C'est LE support à partager en écran pendant le call.

---

## Réponse finale

Retourner :
- Le chemin du one-pager + du `data.json`.
- Le **chiffre COI** (CA manqué/mois + cumulé) et les hypothèses utilisées.
- Le trafic prospect vs top concurrents vs moyenne marché.
- Les 3-5 points qui clochent (ou, en no-site, le potentiel).
- Le nb d'appels DataForSEO consommés (discipline de coût).
- Une phrase de transition prête pour le call (le « pitch » du COI).

---

## Après le call

Si le lead signe → on enchaîne sur l'**Audit Croissance 360** (le vrai livrable payé). Le discovery-audit est la bande-annonce ; le 360 est le film.
