# GitHub profile deployment

## 1. Create the special repository

Create a public repository named exactly:

```text
Foysal-A-Al/Foysal-A-Al
```

GitHub displays the root `README.md` from this repository on your profile.

## 2. Upload the package

Upload every file and keep the folder structure unchanged:

```text
README.md
assets/
.github/workflows/
profile-summary-card-output/
profile-3d-contrib/
dist/
scripts/
```

The package contains local animated fallbacks. Your profile therefore looks complete immediately, even before GitHub Actions generates live analytics.

## 3. Enable workflow write access

Open:

```text
Settings > Actions > General > Workflow permissions
```

Select **Read and write permissions**, then save.

## 4. Add one metrics token

The detailed metrics workflow needs a GitHub Personal Access Token. Create a classic token with:

```text
read:user
repo
```

Add it as a repository secret named:

```text
METRICS_TOKEN
```

The summary cards, 3D contribution landscape, and snake use the automatic `GITHUB_TOKEN`.

## 5. Run each workflow once

Open the Actions tab and manually run:

1. Detailed GitHub Metrics
2. GitHub Profile Summary Cards
3. GitHub Profile 3D Contributions
4. Contribution Snake

After the first successful runs, the local fallback panels are replaced by live account data.

## 6. Recommended pinned repositories

Pin the following six repositories in this order:

1. PsychoGraph-Net
2. Neurofusion-mental-health-AI
3. Origin-of-Human-Movement
4. PyEyesWeb
5. Predictive-Analytics-for-Psychological-Outcomes-with-Blockchain-Data-Integrity
6. Thesis-materials or Stress-analysis

## 7. Validate locally

```bash
python scripts/validate_profile.py
```

## Accuracy and safety notes

- Clinical projects are presented as research prototypes, not medical devices.
- Synthetic data limitations are kept visible in the linked repositories.
- Publication titles and citation counts are not invented. Google Scholar remains the live source.
- The banner and research visuals are committed SVG assets with internal CSS animation.
- The README contains no em dash characters.
