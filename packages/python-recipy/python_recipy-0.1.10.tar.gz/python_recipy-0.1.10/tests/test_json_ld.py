import unittest

from recipy.json_ld import recipe_from_json


class TestJsonLd(unittest.TestCase):
    def test_recipe_from_json(self):
        recipe_json = '''{
    "@context": "http://schema.org",
    "@type": [
        "Recipe"
    ],
    "headline": "Onigiri (Japanese Rice Balls)",
    "datePublished": "2019-04-03T23:43:59.000-04:00",
    "dateModified": "2023-10-13T16:46:33.163-04:00",
    "author": [
        {
            "@type": "Person",
            "name": "Li Shu"
        }
    ],
    "description": "This onigiri recipe is fun to make for Japanese bento boxes! You can put almost anything in these rice balls; try salmon or tuna with mayonnaise.",
    "image": {
        "@type": "ImageObject",
        "url": "https://www.allrecipes.com/thmb/RFpigljvRaJmCKYloZ9t2p3i-VA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/140422-onigiri-japanese-rice-balls-ddmfs-Beauty-3x4-1-aa650c90910247d086e22c57b8402367.jpg",
        "height": 1125,
        "width": 1500
    },
    "publisher": {
        "@type": "Organization",
        "name": "Allrecipes",
        "url": "https://www.allrecipes.com",
        "logo": {
            "@type": "ImageObject",
            "url": "https://www.allrecipes.com/thmb/Z9lwz1y0B5aX-cemPiTgpn5YB0k=/112x112/filters:no_upscale():max_bytes(150000):strip_icc()/allrecipes_logo_schema-867c69d2999b439a9eba923a445ccfe3.png",
            "width": 112,
            "height": 112
        },
        "brand": "Allrecipes",
        "publishingPrinciples": "https://www.allrecipes.com/about-us-6648102#toc-editorial-guidelines",
        "sameAs": [
            "https://www.facebook.com/allrecipes",
            "https://www.instagram.com/allrecipes/",
            "https://www.pinterest.com/allrecipes/",
            "https://www.tiktok.com/@allrecipes",
            "https://www.youtube.com/user/allrecipes/videos",
            "https://twitter.com/Allrecipes",
            "https://flipboard.com/@Allrecipes",
            "https://en.wikipedia.org/wiki/Allrecipes.com",
            "http://linkedin.com/company/allrecipes.com"
        ]
    },
    "name": "Onigiri (Japanese Rice Balls)",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.4",
        "ratingCount": "57"
    },
    "cookTime": "PT20M",
    "nutrition": {
        "@type": "NutritionInformation",
        "calories": "744 kcal",
        "carbohydrateContent": "159 g",
        "fiberContent": "6 g",
        "proteinContent": "14 g",
        "saturatedFatContent": "1 g",
        "sodiumContent": "160 mg",
        "sugarContent": "1 g",
        "fatContent": "3 g",
        "unsaturatedFatContent": "0 g"
    },
    "prepTime": "PT20M",
    "recipeCategory": [],
    "recipeCuisine": [
        "Japanese"
    ],
    "recipeIngredient": [
        "4 cups uncooked short-grain white rice",
        "5.5 cups water, divided",
        "0.25 teaspoon salt",
        "0.25 cup bonito shavings (dry fish flakes)",
        "2 sheets nori (dry seaweed), cut into 1/2-inch strips",
        "2 tablespoons sesame seeds"
    ],
    "recipeInstructions": [
        {
            "@type": "HowToStep",
            "text": "Wash rice in a mesh strainer until water runs clear. Combine washed rice and 4 1/2 cups water in a saucepan. Bring to a boil over high heat, stirring occasionally. Reduce heat to low; cover, and simmer rice until water is absorbed, 15 to 20 minutes. Let rice rest for 15 minutes to continue to steam and become tender. Allow cooked rice to cool."
        },
        {
            "@type": "HowToStep",
            "image": [
                {
                    "@type": "ImageObject",
                    "url": "https://www.allrecipes.com/thmb/sH25jrIxiw6XuKU76nOxvk7ykHo=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/140422-onigiri-japanese-rice-balls-ddmfs-Step-01-2d34fe4ac4794d05927d30fefdbb6e87.jpg"
                }
            ],
            "text": "Combine remaining 1 cup water with salt in a small bowl; use to dampen hands before handling rice. Divide cooked rice into 8 equal portions. Use one portion of rice for each onigiri."
        },
        {
            "@type": "HowToStep",
            "image": [
                {
                    "@type": "ImageObject",
                    "url": "https://www.allrecipes.com/thmb/rGIO6D04HQRbWb5AtwLuqdfEKb4=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/140422-onigiri-japanese-rice-balls-ddmfs-Step-03-6e9a66aa42bc45438c6a5f4d8b373c49.jpg"
                }
            ],
            "text": "Divide one portion of rice in two. Create a dimple in rice and fill with a heaping teaspoon of bonito flakes. Cover with remaining portion of rice and press lightly to enclose filling inside rice ball. Gently press rice to shape into a triangle; wrap with a strip of nori and sprinkle with sesame seeds. Repeat with remaining portions of rice."
        }
    ],
    "recipeYield": [
        "4"
    ],
    "totalTime": "PT60M",
    "review": [
        {
            "@type": "Review",
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": "4"
            },
            "author": {
                "@type": "Person",
                "name": "elyssa"
            },
            "reviewBody": "very simple, i love making these either to snack on or for a dinner. my only change is i make a solution of white vinegar, about a cup, and 2 table spoons of sugar, and mix this with the rice before i begin. It adds just the right amount of flavor to the rice, so its not so over whelming. after adding the vinegar, just wet you hands and shape like always :D"
        },
        {
            "@type": "Review",
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": "5"
            },
            "author": {
                "@type": "Person",
                "name": "Allrecipes Member"
            },
            "reviewBody": "delicious worth an hour. my kids loved them sooooo much",
            "datePublished": "2023-11-22T18:40:42.166Z"
        }
    ]
}'''
        recipe = recipe_from_json(recipe_json)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.title, "Onigiri (Japanese Rice Balls)")
        self.assertEqual(recipe.description,
                         "This onigiri recipe is fun to make for Japanese bento boxes! You can put almost anything in these rice balls; try salmon or tuna with mayonnaise.")
        self.assertEqual(len(recipe.ingredient_groups), 1)
        self.assertEqual(recipe.ingredient_groups[0].ingredients, [
            "4 cups uncooked short-grain white rice",
            "5 1⁄2 cups water, divided",
            "1⁄4 teaspoon salt",
            "1⁄4 cup bonito shavings (dry fish flakes)",
            "2 sheets nori (dry seaweed), cut into 1⁄2-inch strips",
            "2 tablespoons sesame seeds"
        ])
        self.assertEqual(len(recipe.instruction_groups), 1)
        self.assertEqual(len(recipe.instruction_groups[0].instructions), 3)
        self.assertEqual(
            recipe.instruction_groups[0].instructions[0],
            "Wash rice in a mesh strainer until water runs clear. Combine washed rice and 4 1⁄2 cups water in a saucepan. Bring to a boil over high heat, stirring occasionally. Reduce heat to low; cover, and simmer rice until water is absorbed, 15 to 20 minutes. Let rice rest for 15 minutes to continue to steam and become tender. Allow cooked rice to cool."
        )
        self.assertEqual(recipe.rating.value, 4.4)
        self.assertEqual(recipe.rating.count, 57)
        self.assertEqual(len(recipe.reviews), 2)
        self.assertEqual(recipe.reviews[0].author, "elyssa")
        self.assertEqual(recipe.reviews[0].rating, 4.0)
        self.assertEqual(recipe.reviews[0].body,
                         "very simple, i love making these either to snack on or for a dinner. my only change is i make a solution of white vinegar, about a cup, and 2 table spoons of sugar, and mix this with the rice before i begin. It adds just the right amount of flavor to the rice, so its not so over whelming. after adding the vinegar, just wet you hands and shape like always :D")
        self.assertEqual(recipe.meta.prep_time_minutes, 20)
        self.assertEqual(recipe.meta.cook_time_minutes, 20)
        self.assertEqual(recipe.meta.total_time_minutes, 60)
        self.assertEqual(recipe.meta.recipe_yield, "4")
        self.assertEqual(recipe.image_urls[0],
                         "https://www.allrecipes.com/thmb/RFpigljvRaJmCKYloZ9t2p3i-VA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/140422-onigiri-japanese-rice-balls-ddmfs-Beauty-3x4-1-aa650c90910247d086e22c57b8402367.jpg")

    # def test_recipe_from_json(self):
    #     failures = []
    #     success_count = 0
    #
    #     for json_file in Path(__file__).parent.glob('test_data/*.json'):
    #         with open(json_file, 'r') as f:
    #             recipe = recipe_from_json(f.read())
    #             if recipe is None:
    #                 failures.append(json_file)
    #             else:
    #                 success_count += 1
    #
    #     failed_count = len(failures)
    #     print(f"Success: {success_count}")
    #     print(f"Failed: {failed_count}")
    #
    #     if failures:
    #         print("Failures:")
    #         for failure in failures:
    #             if isinstance(failure, tuple):
    #                 print(f" - {failure[0]}: Exception: {failure[1]}")
    #             else:
    #                 print(f" - {failure}")
    #
    #     self.assertEqual(failed_count, 0)


if __name__ == '__main__':
    unittest.main()
