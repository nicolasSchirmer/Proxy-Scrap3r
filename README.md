# Proxy Scrap3r
> A simple proxy list scraper tool

## How to use

`$ git clone https://github.com/nicolasSchirmer/proxy-scrap3r.git`

`$ cd proxy-scrap3r`

`$ pip3 install -r requirements.txt`

`$ python3 proxy_scrap3r`

## Output

It will generate a `Json` file at `./output/proxy_list.json`

If you want to change the file path just add `-jf` to the command. Like so:

`$ pyrhon3 proxy_scrap3r -jf ./custom_output/custom_json.json`

## Object structure

```Json
{
  "ip": "proxy.ip.address.here",
  "port": "666",
  "type": "HTTP or HTTPS or SOCKS4 or SOCKS5",
  "country": "ANY",
  "google_able": true // if at the time of the proxy collecting, it's still working with google // can be false, true or null
}
```

## TODO

- Add support for Proxychains4 / Proxychains
- `txt` simple files
- Add more services

## Where is getting the proxys from?

- https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt ( HTTP proxies )
- https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt ( HTTPS proxies )
- https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt ( SOCKS4 proxies )
- https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt ( SOCKS5 proxies )
- https://www.proxyscan.io/api/proxy?format=json ( HTTP, HTTPS, SOCKS4, SOCKS5 proxies )
- https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt ( HTTP, HTTPS, SOCKS4, SOCKS5 proxies )

## Contribuitions

Please fell free to do so
