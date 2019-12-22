from lxml import html,etree
import requests
import re
import json
import csv
import click

def write_in_json(filename,trend_info):
    f = open(filename,'w')
    f.write(json.dumps(trend_info))
    f.close()

def write_in_csv(filename,trend_info):
    headers = ['title','path_url','description','searches']
    with open(filename,'w') as f:
        writer = csv.DictWriter(f,headers)
        writer.writeheader()
        writer.writerow(trend_info)


@click.command()
@click.option("--trendurl",default="https://www.ebay.com/trending",help="Enter the ebay trending URL")
@click.option("--filename",default="output.json",help="Enter the filename either in csv/json")
def scrape(trendurl,filename):
    resp = requests.get(url=trendurl,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'})
    main_container = html.fromstring(html=resp.text)
    main_tree = main_container.xpath("//div[contains(@class,'trending-item')]")
    all_trend = []
    for tree in main_tree:
        trend_info = {
        "title": tree.xpath(".//h2/a/text()"),
        "path_url": tree.xpath(".//h2[@class='title']/a/@href"),
        "description": tree.xpath(".//p[@class='description']/text()"),
        "searches": tree.xpath(".//strong[@class='number']/text()".strip())
        }
        all_trend.append(trend_info)
        
    file_ext = filename.split('.')[1]
    if file_ext == "csv":
        write_in_csv(filename,all_trend)
    elif file_ext == "json":
        write_in_json(filename,all_trend)
    else:
        print("Enter filename in either csv or json format.")

if __name__ == "__main__":
    scrape()