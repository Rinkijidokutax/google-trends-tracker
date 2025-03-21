# Setting Up GitHub Actions for Automated Reports

You can use GitHub Actions to automatically run the Google Trends Tracker and push reports to your repository. Follow these steps to set it up:

## Prerequisites

- Your repository should be set up on GitHub
- You'll need to store your email credentials as GitHub Secrets

## Setup Instructions

1. Create the following GitHub Secrets in your repository:
   - `EMAIL_SENDER`: Your email address
   - `EMAIL_PASSWORD`: Your email app password
   - `EMAIL_RECIPIENT`: Recipient's email address

2. Create a `.github/workflows` directory in your repository:

```bash
mkdir -p .github/workflows
```

3. Create a workflow file `.github/workflows/daily_report.yml`:

```yaml
name: Daily Google Trends Report

on:
  schedule:
    # Run at 8:00 UTC every day
    - cron: '0 8 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Create directories
        run: mkdir -p output logs
      
      - name: Create .env file
        run: |
          echo "EMAIL_SENDER=${{ secrets.EMAIL_SENDER }}" > .env
          echo "EMAIL_PASSWORD=${{ secrets.EMAIL_PASSWORD }}" >> .env
          echo "EMAIL_RECIPIENT=${{ secrets.EMAIL_RECIPIENT }}" >> .env
          echo "SMTP_SERVER=smtp.gmail.com" >> .env
          echo "SMTP_PORT=587" >> .env
          echo "REGION=US" >> .env
      
      - name: Generate report
        run: python src/main.py --type daily
      
      - name: Upload report as artifact
        uses: actions/upload-artifact@v3
        with:
          name: google-trends-report
          path: output/*.xlsx
          retention-days: 7
```

4. Create similar workflow files for weekly and monthly reports if desired.

## Accessing Reports

Reports will be stored as GitHub Artifacts for 7 days. You can download them from the Actions tab in your repository.

If you want to commit reports back to the repository, add these steps to your workflow:

```yaml
- name: Commit report to repository
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git add output/*.xlsx
    git commit -m "Add Google Trends report for $(date +'%Y-%m-%d')" || echo "No changes to commit"
    git push
```

## Running Manually

You can also trigger the workflow manually from the Actions tab in your GitHub repository.
