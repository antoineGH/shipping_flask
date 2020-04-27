import pycountry

# Coutries Selection
country_choices = []
for country in list(pycountry.countries):
    print(country.name)
    print(country.alpha_2)