# copykat.py
# Written by G.D. Wallters
# Freely released the code to recipe_scraper group
# 8 February, 2020
# =======================================================
from ._abstract import AbstractScraper
from ._utils import get_minutes, get_yields, normalize_string
from ._decorators import Decorators


class CopyKat(AbstractScraper):

    @classmethod
    def host(self):
        return 'copykat.com'

    @Decorators.schema_org_priority
    def title(self):
        return normalize_string(self.soup.find('h1').get_text())

    @Decorators.schema_org_priority
    def total_time(self):
        total_time = 0
        try:
            tt1 = self.soup.find(
                'span',
                {'class': "wprm-recipe-details wprm-recipe-details-hours wprm-recipe-total_time wprm-recipe-total_time-hours"}
            ).get_text()
        except Exception:
            tt1 = 0
        tt2 = self.soup.find(
            'span',
            {'class': 'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes'}
        ).get_text()
        if tt1:
            tt3 = (int(tt1)*60) + int(tt2)
            tt2 = get_minutes(tt3)
            if tt3 and (tt2 == 0):
                total_time = tt3
            else:
                total_time = tt2
        elif tt2:
            total_time = tt2
        return total_time

    @Decorators.schema_org_priority
    def yields(self):
        return get_yields(
            self.soup.find(
                'span',
                {'class': "wprm-recipe-servings-label"}
            ).parent.get_text()
        )

    @Decorators.schema_org_priority
    def image(self):
        image = self.soup.find(
            "div", {"class": "wprm-recipe-image wprm-block-image-rounded"})  # , 'src': True})
        lnk = image.find('a', href=True)
        if lnk:
            isrc = lnk['href']
        return isrc if image else None

    @Decorators.schema_org_priority
    def ingredients(self):
        ingredientsOuter = self.soup.findAll(
            'div',
            {'class': 'wprm-recipe-ingredient-group'}
        )

        ingGroup = []
        for ig in ingredientsOuter:
            try:
                header = ig.find('h4', {
                    'class': "wprm-recipe-group-name wprm-recipe-ingredient-group-name wprm-block-text-bold"}).text
            except Exception:
                header = None
            if header != None:
                ingGroup.append(header)
            ingredparts = ig.findAll('li')
            for i in ingredparts:
                x = normalize_string(i.get_text())
                ingGroup.append(x)
        return ingGroup

    @Decorators.schema_org_priority
    def instructions(self):
        instructions = self.soup.findAll(
            'div',
            {'class': 'wprm-recipe-instruction-group'})
        data = ""
        if len(instructions):
            for instruct in instructions:
                try:
                    header = instruct.find(
                        'h4',
                        {'class': 'wprm-recipe-group-name wprm-recipe-instruction-group-name wprm-block-text-bold'}).text
                except Exception:
                    header = None
                if header is not None:
                    data += header
                ins = instruct.findAll(
                    'div', {'class': 'wprm-recipe-instruction-text'})
                data += '\n'.join([
                    normalize_string(inst.text)
                    for inst in ins
                ])
            return data

    @Decorators.schema_org_priority
    def ratings(self):
        r1 = self.soup.find(
            'div',
            {'class': 'wprm-recipe-rating-details wprm-block-text-normal'}
        ).get_text()
        return r1

    def description(self):
        d = normalize_string(self.soup.find(
            'span',
            {'style': 'display: block;'}).text)

        return d if d else None
