# Modèle Cost of Inaction + schéma du one-pager

Le cœur de l'arme. Objectif : un chiffre **tangible et défendable**, pas un chiffre en l'air.

## Le calcul

1. **Trafic actuel du prospect** (`current_traffic`) — DataForSEO, mode site. En no-site : `0`.
2. **La cible réaliste** (`target_traffic`) = la **moyenne marché** des concurrents analysés (défendable). On garde le **meilleur acteur** (`ceiling_traffic`) comme plafond à citer.
3. **Le delta** (`gap_traffic`) = `target_traffic − current_traffic` (jamais négatif ; si le prospect est déjà au-dessus de la moyenne, viser le meilleur acteur).
4. **La conversion en €** :
   - `missed_monthly = gap_traffic × conversion_rate × value_per_conversion`
   - `conversion_rate` : défaut **2 %** (e-com) ou **3 %** (lead gen services). Toujours affiché.
   - `value_per_conversion` : panier moyen (e-com) ou valeur/lead (services). Renseigné au call ou estimé.
5. **Le Cost of Inaction cumulé** : `coi_cumulative = missed_monthly × months_stagnant`.

> **Règle de prudence.** On chiffre le COI sur la **moyenne marché** (atteignable), pas sur le meilleur acteur (ça, c'est le plafond qu'on cite à l'oral). On affiche TOUJOURS les hypothèses (conversion %, valeur). Si `value_per_conversion` est inconnu, on sort le **delta trafic seul** et on laisse `[valeur/lead]` à remplir en live.

## Le recadrage d'objectif (cost of inaction, la partie orale)

Depuis la qualif, on a l'objectif chiffré du lead. Deux cas :
- **Objectif trop bas** vs marché → « Vos {objectif} sont un **premier palier** atteignable vite ; mais regardez : le marché montre qu'on peut viser bien plus haut. » (on élargit la vision → plus gros deal).
- **Objectif trop haut** vs marché → « Par rapport à ce que fait le marché, {objectif} est ambitieux ; on peut y aller par paliers. » (on se repositionne en expert, on ramène les pieds sur terre).

Dans les deux cas : on ancre le COI (« ce que ça coûte de ne rien faire ») et on transforme le flou en chiffre.

## Cas no-site (le prospect n'a pas de site)

Pas de `current_traffic` (= 0). On bascule sur le **potentiel** :
- Moyenne marché + meilleur acteur → « voilà le trafic (et le CA) que capte déjà ce marché ».
- Le COI devient : « chaque mois sans présence = ~{missed_monthly} € que le marché se partage sans vous ».
- Ouverture : « vous n'avez pas encore de site → c'est justement le moment de le construire pour la performance dès le départ » (on peut vendre le site + le SEO).

## Section « Ce que ce trafic représenterait » (projection de conversion)

Objectif : que le prospect se projette en ventes ou en demandes de devis, pas en visiteurs.

- **Règle d'or : on n'estime jamais le taux de conversion d'un concurrent.** Il n'est pas observable de l'extérieur. On applique le **même taux** au prospect, à la moyenne marché et au meilleur acteur : on compare le trafic, pas la conversion.
- **Source du taux, par ordre de préférence :**
  1. `rate_source: "prospect"` : son taux réel, demandé pendant la découverte (ou lu dans son GA4 / Clarity). Meilleur chiffre : il ne peut pas le contester.
  2. `rate_source: "benchmark"` : une **fourchette** `rate_low` / `rate_mid` / `rate_high`, avec la source citée de chaque borne dans `sources`. Jamais un chiffre unique.
  3. Aucune source fiable : ne pas mettre `rate_mid`. Le one-pager affiche un emplacement « à renseigner pendant l'appel ». Ne jamais inventer un taux.
- `unit` : `"ventes"` (e-commerce) ou `"demandes de devis"` (services).
- `value_per_conversion` optionnel : ajoute le montant en € (calculé sur `rate_mid`).
- Les 3 lignes (prospect, moyenne marché, meilleur acteur) sont reprises de `competitors` via leur `role`.

```json
"conversion_projection": {
  "rate_source": "benchmark",
  "rate_low": 0.01, "rate_mid": 0.02, "rate_high": 0.03,
  "sources": "Source des bornes : [à citer].",
  "unit": "demandes de devis",
  "value_per_conversion": 1500
}
```

## Schéma `data.json` (consommé par build_onepager.py)

```json
{
  "prospect": "Kiko",
  "url": "kiko.fr",
  "mode": "site",
  "market": "e-commerce cosmétique — France",
  "date": "2026-07-25",
  "coi": {
    "current_traffic": 1200,
    "target_traffic": 4500,
    "ceiling_traffic": 9000,
    "gap_traffic": 3300,
    "conversion_rate": 0.02,
    "value_per_conversion": 45,
    "value_label": "panier moyen",
    "missed_monthly": 2970,
    "months_stagnant": 6,
    "coi_cumulative": 17820,
    "assumptions": "Conversion 2 % (moyenne e-com) × panier 45 € — hypothèses à ajuster."
  },
  "competitors": [
    {"name": "ConcurrentX", "traffic": 9000, "role": "ceiling"},
    {"name": "ConcurrentY", "traffic": 5200},
    {"name": "ConcurrentZ", "traffic": 3400},
    {"name": "Moyenne marché", "traffic": 4500, "role": "avg"},
    {"name": "Kiko (vous)", "traffic": 1200, "role": "client"}
  ],
  "site_issues": [
    {"title": "Site lent sur mobile", "detail": "Chargement 4,2 s (seuil recommandé 2,5 s) → positions et conversions perdues."},
    {"title": "Invisible sur vos requêtes argent", "detail": "Aucune page positionnée sur « acheter … » — vous captez 0 intention d'achat."},
    {"title": "Pas de contenu de considération", "detail": "Vos concurrents ont des comparatifs qui captent avant vous."}
  ],
  "objective_reframe": "Votre objectif de 3 000 €/mois est un premier palier atteignable ; le marché montre un plafond bien plus haut.",
  "potential": "En atteignant la moyenne marché (~4 500 visiteurs/mois), vous viseriez ~2 970 €/mois de CA organique additionnel.",
  "next_step": "Un plan structuré (fondations → contenu → acquisition) pour combler ce delta."
}
```

- Champs numériques bruts (le script formate l'affichage).
- `role` sur un concurrent : `client` (le prospect), `avg` (moyenne marché), `ceiling` (le meilleur). Les autres sans `role`.
- `site_issues` : 3 à 5 max, titres punchy + détail compréhensible par un non-SEO. Vide en mode no-site.
- Ne jamais inventer un chiffre de trafic : s'il vient de DataForSEO, il est estimé — le one-pager le mentionne déjà en pied de page.
