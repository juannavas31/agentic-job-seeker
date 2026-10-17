# Alternatives to fetch jobs offers via HTTP APIs

Usually, the jobs portals do not provide any API to fetch jobs offers. An alternative is to use 3rd parties web scrappers or jobs aggregators, via rapidAPI.

This is a limited research on the available options to fetch jobs offers via a rapidapi.com 

Note: you need to register and see your dashboard at https://rapidapi.com/developer/authorization/default-application_xxxx, where the API-KEY is shown. 

## JSearch
JSearch by OpenWeb Ninja is a fast, reliable, and comprehensive jobs API. As the most comprehensive and maintained option available, JSearch empowers you to seamlessly access most-up-to-date job postings and salary information in real-time from Google for Jobs - the largest job aggregate on the web.

### Plan
- Basic: $0 for 200 requests/month
- Pro: $25 for 10,000 requests/month

Note: Each page (containing up to 10 results) returned by the API consumes one request credit.

The API provides the job offer data in two steps:
- Job search, to get the jobs offers matching the specified criteria, it returns a job-id per job
- Job details, to get the details for a job-id

Authorization: Gateway URl: rapidapi.com, { X-RapidAPI-Key: 'your api key' } 
Header: { X-RapidAPI-Host: 'jsearch.p.rapidapi.com' }

Start by subscribing to the free plan (done). 

## [LinkedIn jobs search](https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/linkedin-job-search-api)

High quality job listings from LinkedIn. Includes all relevant details like: Full job description, Company industry, number of followers, location, specialties, company description.

Our database indexes over 20,000 jobs every hour. Over 2 million jobs every week!

We offer a wide range of filters to narrow the results down: Job Title, Description, Location, Company, Remote.

10M+ AI-enriched LinkedIn jobs with Company info & Hourly refresh. Powered by Fantastic.jobs


### Plan
- Basic: $0, includes 250 jobs/month and 25 requests/month
- Pro: $45, includes 10,000 jobs/month and 5,000 requests/month

Note: a request contains by default a maximum of 100 jobs. It can be increased up to 1,000 jobs. 

Headers: { X-RapidAPI-Host: "linkedin-job-search-api.p.rapidapi.com" }


## [Glassdoor Real-Time](https://rapidapi.com/things4u-api4upro/api/glassdoor-real-time)
Real-time data, unofficial API glassdoor.com, search for jobs, explore company reviews, and analyze salary insights for better career decisions

### Plan
- Basic: $0, includes 200 requests/month
- Pro: $15, includes 15,000 requests/month

Header: { X-RapidAPI-Host: "glassdoor-real-time.p.rapidapi.com" }

## [Infojobs API](https://rapidapi.com/otomo-otomo-default/api/infojobs-api)
Extract job listings from Infojobs.net including detailed descriptions, salary information, company ratings, required skills, and job recommendations. Access Spain's leading employment marketplace programmatically


### Plan
- Basic: $0, includes 100 requests/month
- Pro: $15, includes 3,000 requests/moth

Header : { X-RapidAPI-Host: "infojobs-api.p.rapidapi.com" }


