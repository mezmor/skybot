from util import hook, http

"""
def google(symbols, timeout=None):
    symbols = list(symbols)
    url = "http://finance.google.com/finance/info?client=ig&q=%s" % ",".join(urllib.quote(symbol) for symbol in symbols)
    f = urllib2.urlopen(url)
    try:
        data = f.read()
        data = data.split("\n")
        if data[0] != "" or data[1] != "// [":
            return "bad market data for %r: %r" % (url, data)

        data = "[" + "\n".join(data[2:])
        j = json.loads(data, encoding="iso-8859-1")
        if len(j) != len(symbols):
            return "some symbols are invalid"

        result = {}
        for symbol, data in zip(symbols, j):
            last_trade_price = decimal(data["l_fix"])
            result[symbol] = Stock(symbol, symbol, None, None, last_trade_price, json.dumps(data))
        return result
    finally:
        f.close()
"""

@hook.command
def stock(inp):
    '''.stock <symbol> -- gets stock information'''

    url = ('http://query.yahooapis.com/v1/public/yql?format=json&'
           'env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys')

    parsed = http.get_json(url, q='select * from yahoo.finance.quotes '
                           'where symbol in ("%s")' % inp)  # heh, SQLI

    quote = parsed['query']['results']['quote']

    # if we dont get a company name back, the symbol doesn't match a company
    if quote['Change'] is None:
        return "unknown ticker symbol %s" % inp

    price = float(quote['LastTradePriceOnly'])
    change = float(quote['Change'])
    if quote['Open'] and quote['Bid'] and quote['Ask']:
        open_price = float(quote['Open'])
        bid = float(quote['Bid'])
        ask = float(quote['Ask'])
        if price < bid:
            price = bid
        elif price > ask:
            price = ask
        change = price - open_price
        quote['LastTradePriceOnly'] = "%.2f" % price
        quote['Change'] = ("+%.2f" % change) if change >= 0 else change

    if change < 0:
        quote['color'] = "5"
    else:
        quote['color'] = "3"

    quote['PercentChange'] = 100 * change / (price - change)

    ret = "%(Name)s - %(LastTradePriceOnly)s "                   \
          "\x03%(color)s%(Change)s (%(PercentChange).2f%%)\x03 "        \
          "Day Range: %(DaysRange)s " \
          "MCAP: %(MarketCapitalization)s" % quote

    return ret

