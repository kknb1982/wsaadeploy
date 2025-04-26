#! /bin/bash

wget -q -O data/`country_slugs.json"` "https://www.gov.uk/api/content/foreign-travel-advice"
echo "Country data downloaded"
