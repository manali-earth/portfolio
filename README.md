# JSON Portfolio Template

A reusable academic portfolio template built with only HTML, CSS, and vanilla JavaScript. It follows the reference site’s Wix-style visual language: pale sage navigation, full-width image hero, centered serif headings, white content sections, academic typography, photo gallery, and straightforward cards.

## Pages and homepage content

The homepage includes the same major content flow as the reference:

- Recent News
- Photo Gallery - Geography in Action
- Education and Experience
- Projects
- Journal Publications
- Contact

The top bar also opens dedicated pages, each its own folder with an `index.html`:

- `/my-story/`
- `/education-experience/`
- `/projects/`
- `/publications/`
- `/conferences/`
- `/leadership/`

Conferences and Leadership are kept as dedicated pages rather than homepage sections.

## Query-driven detail views

Every dedicated page supports a `?view=` query parameter. Examples:

```text
/projects/?view=urbanization-pattern
/publications/?view=urban-park-use
/conferences/?view=aag-2025
/leadership/?view=campus-sustainability
```

Cards and links generate these URLs automatically. `?view=overview` opens the page overview.

## Database structure

`database/database.json` is the routing index. It points to one JSON file per page, plus an `imageBase` value that every image path in the JSON files is resolved against:

```json
{
  "imageBase": "/database/photos/",
  "home": "/database/home.json",
  "myStory": "/database/my-story.json",
  "educationExperience": "/database/education-experience.json",
  "gisProjects": "/database/projects.json",
  "researchPublications": "/database/publications.json",
  "conferences": "/database/conferences.json",
  "leadership": "/database/leadership.json"
}
```

Every `image`/`heroImage` value inside the data JSON files (e.g. `"home/hero.jpg"`, `"projects/project-1.jpg"`) is a path *relative to `imageBase`* — never write the `imageBase` prefix into those files yourself. `app.js` resolves the final URL at render time via a single `img()` helper.

Edit the JSON files to create a different person's profile. Replace the image files in the relevant photo directories while keeping the same field names. The homepage's Contact section is driven by the `contact` object (`email`, `phone`, `location`) in `database/home.json`.

### Splitting the data into its own repo

Because every page JSON path and `imageBase` in `database.json` is resolved with a plain `fetch()`/`<img src>`, either can point at a different **absolute URL** instead of a local path — the website doesn't care whether its data is local or remote. This makes it possible to keep the website in one repo and the content (JSON + photos) in another:

1. Move everything currently under `database/` **except `database.json` itself** — i.e. `home.json`, `my-story.json`, `projects.json`, etc., and the whole `photos/` folder — into the second repo.
2. In the website repo, `database/` then contains only `database.json`, and you rewrite its values to point at the second repo's raw content, e.g. (GitHub raw URLs shown as an example):
   ```json
   {
     "imageBase": "https://raw.githubusercontent.com/<user>/portfolio-database/main/photos/",
     "home": "https://raw.githubusercontent.com/<user>/portfolio-database/main/home.json",
     "myStory": "https://raw.githubusercontent.com/<user>/portfolio-database/main/my-story.json",
     "educationExperience": "https://raw.githubusercontent.com/<user>/portfolio-database/main/education-experience.json",
     "gisProjects": "https://raw.githubusercontent.com/<user>/portfolio-database/main/projects.json",
     "researchPublications": "https://raw.githubusercontent.com/<user>/portfolio-database/main/publications.json",
     "conferences": "https://raw.githubusercontent.com/<user>/portfolio-database/main/conferences.json",
     "leadership": "https://raw.githubusercontent.com/<user>/portfolio-database/main/leadership.json"
   }
   ```
3. No changes to `app.js`, `index.html`, or any sub-page are needed — only `database.json`'s values change. You can also mix local and remote (e.g. keep `home.json` local but serve `imageBase` from a remote host), and any single `image` value can itself be a full `http(s)://` URL to bypass `imageBase` entirely for that one image.

Note that `database/database.json` itself is always fetched from the website's own `/database/database.json` — that one file has to stay in the website repo, since it's what tells the site where everything else lives.

**Every internal path — nav links, the `fetch('/database/database.json')` call in `app.js`, and the local defaults above — is root-relative (starts with `/`).** This matters because the dedicated pages live one folder deep (e.g. `/projects/index.html`); a path like `database/home.json` without the leading slash would resolve relative to `/projects/` and 404, instead of hitting `/database/home.json`. Keep new local paths root-relative if you extend the site.

This also assumes the site is served from the domain root (a custom domain, or a root deploy on a host like Netlify or Vercel). If you deploy to a GitHub Pages *project* site under a subpath (`username.github.io/repo-name/`), root-relative paths will need to be adjusted to include that subpath.

## Run locally

Because the pages load JSON with `fetch()`, use a local web server:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## HTML in database text

Any text in the database JSON can contain inline HTML such as `<br>`, `<b>`, `<i>`, `<a href="...">` or `<span>`. The site inserts it as HTML in every section (hero, news, gallery captions, timelines, project cards, detail pages, contact, page headings), so formatting can be changed from the admin panel without touching site code. Places that cannot hold markup (alt text, tooltips, the browser tab title) automatically get a tag-free version.
