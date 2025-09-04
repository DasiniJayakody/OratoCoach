# 🎯 Google Visibility Checklist for OratoCoach

## Phase 1: Deployment ✅

- [ ] Deploy to Railway or Heroku
- [ ] Get your deployed domain URL
- [ ] Test that your website works at the deployed URL

## Phase 2: Domain Configuration ✅

- [ ] Run `update_domain.bat` script
- [ ] Enter your actual deployed domain
- [ ] Verify sitemap.xml is updated
- [ ] Verify robots.txt is updated
- [ ] Commit and push changes to GitHub

## Phase 3: Google Search Console Setup ✅

- [ ] Go to [Google Search Console](https://search.google.com/search-console)
- [ ] Add your property (deployed domain)
- [ ] Verify ownership (DNS, HTML tag, or file upload)
- [ ] Submit your sitemap: `https://your-domain.com/sitemap.xml`
- [ ] Request indexing for your homepage

## Phase 4: SEO Optimization ✅

- [ ] Ensure all pages have proper meta titles
- [ ] Ensure all pages have meta descriptions
- [ ] Check that images have alt text
- [ ] Verify mobile responsiveness
- [ ] Test page loading speed

## Phase 5: Monitoring ✅

- [ ] Check Google Search Console for indexing status
- [ ] Monitor for any crawl errors
- [ ] Check search performance after 1-2 weeks
- [ ] Submit additional URLs for indexing if needed

## Expected Timeline:

- **Immediate**: Website deployed and accessible
- **1-7 days**: Google discovers your sitemap
- **1-4 weeks**: Pages appear in Google search results
- **4-8 weeks**: Full indexing and ranking

## Quick Commands:

```bash
# After deployment, update domain
./update_domain.bat

# Commit changes
git add .
git commit -m "Update domain configuration for Google visibility"
git push origin main

# Check deployment status
curl https://your-deployed-domain.com
```

## Troubleshooting:

- **Not indexed after 4 weeks**: Request indexing again in Search Console
- **Crawl errors**: Check your robots.txt and sitemap.xml
- **Slow indexing**: Submit sitemap multiple times
- **Domain verification issues**: Try different verification methods

## Success Indicators:

- ✅ Website accessible at deployed URL
- ✅ Sitemap submitted successfully in Search Console
- ✅ No crawl errors in Search Console
- ✅ Pages appear in Google search results
- ✅ "OratoCoach" search shows your website
