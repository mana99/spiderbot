
# Glassdoor

## Usage


In scrapy folder:

``` bash
# Company crawler
scrapy crawl company -a city="rotterdam" \
                     -a url="https://www.glassdoor.com/Reviews/rotterdam-reviews-SRCH_IL.0,9_IM1109.htm" \
                     -o "rotterdam.json"   
```
