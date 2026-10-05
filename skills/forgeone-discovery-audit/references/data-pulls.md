# Data pulls — Phase 2 (bornée, token-économe)

Objectif : le trafic du prospect + le trafic des concurrents + la moyenne marché, en **~5 à 10 appels max**. Endpoints Labs (base de données) uniquement. **Jamais** de live SERP en boucle, jamais de sous-agents, jamais de fan-out. Si DataForSEO est absent, dégrader (SimilarWeb public, Ubersuggest gratuit, estimations SERP) et le dire.

## Mode SITE (le prospect a une URL)

1. **Trafic du prospect** — `dataforseo_labs_google_domain_rank_overview` (target = domaine du prospect). → trafic organique estimé (ETV), nb de mots-clés positionnés, valeur du trafic. *(1 appel)*
2. **Les vrais concurrents SEO** — `dataforseo_labs_google_competitors_domain` (target = prospect, `exclude_top_domains: true`, `limit: 8`). → la liste des domaines qui se disputent les mêmes requêtes (souvent différents des concurrents « business » que le prospect cite). *(1 appel)*
3. **Trafic des 3-4 meilleurs concurrents** — `dataforseo_labs_google_domain_rank_overview` sur chacun. → leur ETV. *(3-4 appels)*
4. *(optionnel, contexte)* **Volume des head terms** — `dataforseo_labs_google_keyword_overview` (batch de 2-5 mots-clés en un appel). → taille du gâteau. *(1 appel)*

**Total : ~6-7 appels.**

## Mode NO-SITE (pas encore de site)

1. **Identifier les leaders** — 1 SERP live sur le head term (`serp_organic_live_advanced`, `depth: 10`) OU `dataforseo_labs_google_serp_competitors` sur les seeds. → les domaines qui dominent. *(1 appel)*
2. **Trafic des 3-5 leaders** — `domain_rank_overview` sur chacun. *(3-5 appels)*
3. *(optionnel)* volume des head terms — `keyword_overview` batch. *(1 appel)*

**Total : ~5-7 appels.**

## Calculs à partir des pulls

- **Moyenne marché** (`target_traffic`) = moyenne de l'ETV des concurrents/leaders analysés.
- **Plafond** (`ceiling_traffic`) = le meilleur acteur.
- **Trafic prospect** (`current_traffic`) = ETV du prospect (mode site) ou `0` (no-site).
- Arrondir proprement pour l'affichage (ex. 4 512 → « ~4 500 »).

## Diagnostic site léger (Phase 3, mode site)

**1 seul appel** : `on_page_lighthouse` (CWV : LCP/CLS/INP + perf score) **ou** `on_page_instant_pages` (titres, H1, statut, indexabilité) sur la **home uniquement**. En tirer 3-5 points punchy. Compléter avec ce que les pulls SEO révèlent déjà (ex. « 0 mot-clé sur les requêtes transactionnelles »). Ne pas crawler le site.

## Discipline

- Capper tous les `limit`. Ne jamais boucler sans borne.
- Un seul passage : on ne re-pull pas.
- Noter le **nombre d'appels consommés** pour la réponse finale (transparence coût).
