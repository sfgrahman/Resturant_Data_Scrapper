import httpx
import asyncio
import json
from typing import List, Dict
from parsel import Selector


def parse_company(resp: httpx.Response):
    sel = Selector(text=resp.text)
    xpath = lambda xp: sel.xpath(xp).get(default="").strip()
    open_hours = {}
    for day in sel.xpath('//th/p[contains(@class,"day-of-the-week")]'):
        name = day.xpath('text()').get().strip()
        value = day.xpath('../following-sibling::td//p/text()').get().strip()
        open_hours[name.lower()] = value
    return dict(
        name=xpath('//h1/text()'),
        website=xpath('//p[contains(text(),"Business website")]/following-sibling::p/a/text()'),
        phone=xpath('//p[contains(text(),"Phone number")]/following-sibling::p/text()'),
        address=xpath('//a[contains(text(),"Get Directions")]/../following-sibling::p/text()'),
        logo=xpath('//img[contains(@class,"businessLogo")]/@src'),
        claim_status="".join(sel.xpath('//span[span[contains(@class,"claim")]]/text()').getall()).strip().lower(),
        open_hours=open_hours
    )


async def scrape_yelp_companies(company_urls:List[str], session: httpx.AsyncClient) -> List[Dict]:
    """Scrape yelp company details from given yelp company urls"""
    responses = await asyncio.gather(*[
        session.get(url) for url in company_urls
    ])
    results = []
    for resp in responses:
        results.append(parse_company(resp))
    return results

BASE_HEADERS = {
    "authority": "www.yelp.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate",
}

async def run(url=[]):
    async with httpx.AsyncClient(headers=BASE_HEADERS, timeout=10.0) as session:
        data = await scrape_yelp_companies(url, session=session)
        #print(json.dumps(data, indent=2))
        return json.dumps(data, indent=2)

if __name__ == "__main__":
    asyncio.run(run(["https://www.yelp.com/biz/valerie-new-york"]))