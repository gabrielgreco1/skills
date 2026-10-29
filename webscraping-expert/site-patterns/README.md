# Site Patterns

**Scope:** Playbooks for recognizable site stacks. When the target uses a known technology, you can skip a lot of reverse-engineering by following the documented pattern.

Each file follows the same skeleton: **When you see this** → **How it works** → **Pattern / code** → **Gotchas** → **Related**.

## Files

| File | Recognize by |
|---|---|
| `arcgis-feature-server.md` | Path contains `/arcgis/rest/services/<service>/{FeatureServer,MapServer}/<N>/query`, response `{features:[{attributes,geometry}], exceededTransferLimit}`. |
| `aspnet-webforms.md` | URL ends in `.aspx`, hidden `__VIEWSTATE` field, `__doPostBack` JS function, control IDs like `ctl00$Main$...` |
| `ckan-dkan.md` | Endpoints `/api/3/action/{package_search,package_show,datastore_search}`, envelope `{success, result:{results,count}}`. Footer mentions CKAN/DKAN. |
| `datatables-server-side.md` | POST with `draw/start/length/columns[N][data]`, response `{draw, recordsTotal, recordsFiltered, data:[...]}`. |
| `embedded-bi-dashboard.md` | Public BI embeds (Power BI `app.powerbi.com/view?r=`, Tableau Public, Looker Studio, Metabase). Canvas + virtualized DOM + binary query payload. |
| `geojson-bbox-map-portal.md` | Custom spatial API queried by bounding box, returning GeoJSON features; discover its schema from map requests. |
| `graphql.md` | POST to `/graphql` (or `/api/graphql`, `/query`) with body containing `query`/`variables`/`operationName` or `extensions.persistedQuery`. HTTP 200 + `{"data": ..., "errors": [...]}` shape. |
| `legacy-cms.md` | ColdFusion (`.cfm`), classic ASP (`.asp`), JSP (`.jsp`), or any portal returning `HTTP 200 + "Error"` page on invalid sessions. |
| `nextjs-app-router-rsc.md` | `self.__next_f.push([...])` in HTML, or requests with `RSC: 1` + `Accept: text/x-component`. React Server Component flight data — the modern Next.js shape (vs Pages Router `__NEXT_DATA__`). |
| `natural-for-ajax.md` | `/servlet/easynat-app`, Natural page HTML, and `/servlet/Connector` POSTs with `SESSIONID`, `XML`, and `STAMP`; stateful priming and length-prefixed event streams. |
| `odata.md` | `$metadata`, `$filter`/`$select`/`$top`/`$skip`, envelope `{"value":[...],"@odata.nextLink":...}` (v4) or `{"d":{"results":...}}` (v2/v3). Stats offices (CBS). |
| `paginated-facet-search-api.md` | Endpoint with `rows/start`, `refine.<field>=<value>`, response `{records, nhits, facet_groups}`. Hard offset cap (~10k) → slice by facet. OpenDataSoft Explore. |
| `pxweb.md` | Path `/api/v1/<lang>/...` at a statistics bureau; POST a variable selection, get JSON-stat back. StatFi / SCB / SSB (Nordic offices). |
| `salesforce-experience-cloud.md` | URL contains `.my.site.com` or `/s/sfsites/aura`, `aura.context` in request body, `x-sfdc-*` headers |
| `sdmx-jsonstat.md` | Statistics-office APIs. Response is `{dimension, size, value}` (JSON-stat) or `{dataSets, structure}` (SDMX-JSON); query by dimension filter not row offset. OECD / Eurostat / ECB. |
| `spa-frameworks.md` | React/Next/Vue/Svelte app. Look for `__NEXT_DATA__`, `__INITIAL_STATE__`, `__APOLLO_STATE__`, `__NUXT__` in the page source. |
| `tableau-public.md` | `bootstrapSession` requests, `tsConfigContainer`, canvas charts. Bootstrap a session in-browser, hand off to `tableauscraper`, enumerate filters. |
| `templated-cms-schema-drift.md` | Same CMS template deployed across many instances — field names drift per instance even when layout is identical. |
