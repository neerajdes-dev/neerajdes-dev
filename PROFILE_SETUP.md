# Premium Profile Setup

This profile is inspired by Resolvent's green-and-dark visual direction. Its decorative SVG graphics are custom artwork; they do not replace the official Resolvent logo.

## Go live

1. Review and merge the feature pull request.
2. Go to the **Actions** tab. Enable workflows if GitHub asks.
3. Open **Refresh GitHub profile contributions** and choose **Run workflow**.
4. Ensure the workflow has permission to write to the repository: **Settings → Actions → General → Workflow permissions** (where available).
5. View https://github.com/neerajdes-dev and check the animations, layout and project links.

The scheduled workflow runs each day and commits assets/contributions.svg only if it changed. Scheduled runs may be delayed or disabled after prolonged inactivity.

## Add a real portrait later

Provide a photograph you have permission to publish and replace the abstract monogram/hero design with a generated ASCII SVG. Do not commit private photographs unless you want them publicly visible.

## Edit text or styling

- README.md: profile content
- assets/hero.svg: headline and graphic
- assets/terminal.svg: professional information
- scripts/refresh_heatmap.py: contribution generator and palette
- .github/workflows/refresh-profile.yml: automated refresh schedule

### Limitations

GitHub may modify its contribution calendar HTML, requiring updates to the parser. The workflow exits with an error instead of silently committing an empty calendar.
