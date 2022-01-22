import shellinford


with open('app/stock_brand.fm') as f:
    lines = f.readlines()

fm = shellinford.FMIndex()
fm.build(lines, 'brand.fm')

fm.read('brand.fm')
fm.write('brand.fm')

