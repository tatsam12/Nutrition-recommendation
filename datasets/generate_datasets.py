"""
Dataset Generator for Nutrition Recommender System
Generates all 6 required CSV datasets.
Run: python generate_datasets.py
"""

import csv
import random
import math
from datetime import datetime, timedelta

random.seed(42)

# ============================================================
# DATASET 1: food_dataset.csv  (300+ Nepal-focused foods)
# ============================================================

FOODS = [
    # (food_name, category, calories, protein, carbs, fat, fiber, recommended_goal, image_url)
    # Dal / Legumes
    ("Dal Bhat", "Dal & Rice", 350, 14.0, 62.0, 3.5, 5.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Dal_bhat.jpg/640px-Dal_bhat.jpg"),
    ("Masoor Dal", "Legumes", 116, 9.0, 20.0, 0.4, 3.9, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Red_lentils.jpg/640px-Red_lentils.jpg"),
    ("Chana Dal", "Legumes", 164, 8.9, 27.4, 2.6, 7.6, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Channadal.jpg/640px-Channadal.jpg"),
    ("Mung Dal", "Legumes", 105, 7.0, 19.2, 0.4, 7.6, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Mung_beans_background.jpg/640px-Mung_beans_background.jpg"),
    ("Toor Dal", "Legumes", 118, 6.8, 20.6, 0.4, 5.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Toor_dal.jpg/640px-Toor_dal.jpg"),
    ("Black Dal (Kali Dal)", "Legumes", 127, 9.0, 21.6, 0.8, 5.3, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Black_Urad_Dal.jpg/640px-Black_Urad_Dal.jpg"),
    ("Kidney Beans (Rajma)", "Legumes", 127, 8.7, 22.8, 0.5, 6.4, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Kidney_beans.jpg/640px-Kidney_beans.jpg"),
    ("Soybean", "Legumes", 173, 16.6, 9.9, 9.0, 6.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Soybeans_dsc_series_home.jpg/640px-Soybeans_dsc_series_home.jpg"),
    ("Chickpeas (Chana)", "Legumes", 164, 8.9, 27.4, 2.6, 7.6, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Chickpeas_%28garbanzo_beans%29.jpg/640px-Chickpeas_%28garbanzo_beans%29.jpg"),

    # Rice & Grains
    ("Steamed Rice", "Rice & Grains", 204, 4.2, 44.5, 0.4, 0.6, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Banquet_rice.jpg/640px-Banquet_rice.jpg"),
    ("Brown Rice", "Rice & Grains", 216, 5.0, 44.8, 1.8, 3.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Brown_rice.jpg/640px-Brown_rice.jpg"),
    ("Chiura (Beaten Rice)", "Rice & Grains", 346, 6.9, 76.9, 1.4, 1.7, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Chiura.jpg/640px-Chiura.jpg"),
    ("Dhido (Buckwheat Porridge)", "Traditional", 161, 5.7, 33.5, 1.0, 2.7, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Dhido.jpg/640px-Dhido.jpg"),
    ("Roti (Wheat Flatbread)", "Bread & Roti", 297, 9.7, 57.5, 3.5, 5.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Chapati.jpg/640px-Chapati.jpg"),
    ("Makai Roti (Corn Flatbread)", "Bread & Roti", 218, 5.1, 45.5, 2.1, 3.8, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Makki_ki_roti.jpg/640px-Makki_ki_roti.jpg"),
    ("Puri", "Bread & Roti", 349, 7.0, 48.0, 16.0, 2.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Puri_served.jpg/640px-Puri_served.jpg"),
    ("Sel Roti", "Traditional", 325, 5.0, 55.0, 10.5, 1.2, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Sel_roti.jpg/640px-Sel_roti.jpg"),
    ("Oatmeal (Jaulo)", "Rice & Grains", 158, 5.6, 27.4, 3.2, 4.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Oatmeal.jpg/640px-Oatmeal.jpg"),
    ("Millet (Kodo)", "Rice & Grains", 378, 11.0, 72.8, 4.2, 8.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Millet_-_Pennisetum_glaucum.jpg/640px-Millet_-_Pennisetum_glaucum.jpg"),
    ("Corn (Makai)", "Rice & Grains", 96, 3.4, 21.0, 1.5, 2.4, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Corn_kernels.jpg/640px-Corn_kernels.jpg"),

    # Vegetables
    ("Gundruk", "Fermented Foods", 30, 2.5, 5.5, 0.5, 3.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Gundruk.jpg/640px-Gundruk.jpg"),
    ("Spinach (Palungo)", "Vegetables", 23, 2.9, 3.6, 0.4, 2.2, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Spinach_leaves.jpg/640px-Spinach_leaves.jpg"),
    ("Cauliflower (Kauli)", "Vegetables", 25, 1.9, 5.0, 0.3, 2.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Cauliflower_2.jpg/640px-Cauliflower_2.jpg"),
    ("Cabbage (Bandakopi)", "Vegetables", 25, 1.3, 5.8, 0.1, 2.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Cabbage_and_cross_section_on_white.jpg/640px-Cabbage_and_cross_section_on_white.jpg"),
    ("Potato (Aloo)", "Vegetables", 77, 2.0, 17.5, 0.1, 2.2, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Potato_je.jpg/640px-Potato_je.jpg"),
    ("Tomato", "Vegetables", 18, 0.9, 3.9, 0.2, 1.2, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Tomato_je.jpg/640px-Tomato_je.jpg"),
    ("Cucumber (Kakro)", "Vegetables", 16, 0.7, 3.6, 0.1, 0.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Cucumbers_-_whole_and_slice.jpg/640px-Cucumbers_-_whole_and_slice.jpg"),
    ("Onion (Pyaj)", "Vegetables", 40, 1.1, 9.3, 0.1, 1.7, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Onions.jpg/640px-Onions.jpg"),
    ("Garlic (Lasun)", "Vegetables", 149, 6.4, 33.1, 0.5, 2.1, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Garlic-_Allium_sativum.jpg/640px-Garlic-_Allium_sativum.jpg"),
    ("Ginger (Adrak)", "Vegetables", 80, 1.8, 17.8, 0.8, 2.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Ginger_roots.jpg/640px-Ginger_roots.jpg"),
    ("Radish (Mula)", "Vegetables", 16, 0.7, 3.4, 0.1, 1.6, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Radishes.jpg/640px-Radishes.jpg"),
    ("Carrot (Gajar)", "Vegetables", 41, 0.9, 9.6, 0.2, 2.8, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Vegetable-Carrot-Bundle-wStem.jpg/640px-Vegetable-Carrot-Bundle-wStem.jpg"),
    ("Broccoli", "Vegetables", 34, 2.8, 6.6, 0.4, 2.6, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Fresh_broccoli_and_cross_section.jpg/640px-Fresh_broccoli_and_cross_section.jpg"),
    ("Bitter Gourd (Karela)", "Vegetables", 17, 1.0, 3.7, 0.2, 2.8, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bitter_gourd.jpg/640px-Bitter_gourd.jpg"),
    ("Pumpkin (Farsi)", "Vegetables", 26, 1.0, 6.5, 0.1, 0.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Pumpkin_patch.jpg/640px-Pumpkin_patch.jpg"),
    ("Bamboo Shoot (Tama)", "Vegetables", 27, 2.6, 5.2, 0.3, 2.2, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Bamboo_shoots.jpg/640px-Bamboo_shoots.jpg"),
    ("Mustard Greens (Rayo Saag)", "Vegetables", 27, 2.7, 4.7, 0.4, 3.2, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Mustard_leaves.jpg/640px-Mustard_leaves.jpg"),
    ("Fenugreek Leaves (Methi)", "Vegetables", 49, 4.4, 6.0, 0.9, 2.7, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Fenugreek_Leaves.jpg/640px-Fenugreek_Leaves.jpg"),
    ("Green Peas (Kerau)", "Vegetables", 81, 5.4, 14.5, 0.4, 5.1, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Garden_peas_in_pod.jpg/640px-Garden_peas_in_pod.jpg"),
    ("Sweet Potato (Sakhar Kanda)", "Vegetables", 86, 1.6, 20.1, 0.1, 3.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Ipomoea_batatas_006.jpg/640px-Ipomoea_batatas_006.jpg"),

    # Meat & Poultry
    ("Buffalo Meat (Buff)", "Meat", 131, 26.0, 0.0, 2.8, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Raw_meat.jpg/640px-Raw_meat.jpg"),
    ("Chicken Curry", "Meat", 215, 23.0, 5.2, 11.5, 0.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/A_small_cup_of_coffee.JPG/640px-A_small_cup_of_coffee.JPG"),
    ("Mutton Curry", "Meat", 258, 24.5, 4.0, 16.2, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Mutton_curry.jpg/640px-Mutton_curry.jpg"),
    ("Sukuti (Dried Meat)", "Meat", 234, 40.0, 2.0, 6.5, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Sukuti.jpg/640px-Sukuti.jpg"),
    ("Pork (Sungur)", "Meat", 242, 27.3, 0.0, 14.4, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Pulled_pork.jpg/640px-Pulled_pork.jpg"),
    ("Duck (Hans)", "Meat", 337, 19.0, 0.0, 28.4, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Duck_meat.jpg/640px-Duck_meat.jpg"),

    # Seafood & Fish
    ("Rohu Fish (Rohu Macha)", "Fish & Seafood", 97, 16.7, 0.0, 3.0, 0.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Rohu.jpg/640px-Rohu.jpg"),
    ("Catfish", "Fish & Seafood", 116, 18.0, 0.0, 4.3, 0.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Catfish.jpg/640px-Catfish.jpg"),
    ("Dried Fish (Sidra)", "Fish & Seafood", 290, 55.0, 0.0, 6.5, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Dried-salted-fish.jpg/640px-Dried-salted-fish.jpg"),
    ("Crab Curry", "Fish & Seafood", 119, 16.5, 3.5, 4.8, 0.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Crab_curry.jpg/640px-Crab_curry.jpg"),

    # Eggs & Dairy
    ("Boiled Egg", "Eggs & Dairy", 155, 13.0, 1.1, 11.0, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Boiled_eggs.jpg/640px-Boiled_eggs.jpg"),
    ("Egg Curry", "Eggs & Dairy", 185, 11.8, 6.2, 12.5, 0.8, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Egg_curry.jpg/640px-Egg_curry.jpg"),
    ("Scrambled Eggs", "Eggs & Dairy", 149, 10.1, 1.6, 11.2, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Scrambled_eggs.jpg/640px-Scrambled_eggs.jpg"),
    ("Milk (Dudh)", "Eggs & Dairy", 42, 3.4, 4.8, 1.0, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Milk_glass.jpg/640px-Milk_glass.jpg"),
    ("Buffalo Milk", "Eggs & Dairy", 97, 3.8, 5.0, 6.9, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Milk_glass.jpg/640px-Milk_glass.jpg"),
    ("Yogurt (Dahi)", "Eggs & Dairy", 61, 3.5, 4.7, 3.3, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Bowl_of_yogurt.jpg/640px-Bowl_of_yogurt.jpg"),
    ("Paneer (Chhurpi Fresh)", "Eggs & Dairy", 265, 18.3, 3.4, 20.8, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Paneer.jpg/640px-Paneer.jpg"),
    ("Hard Chhurpi", "Eggs & Dairy", 380, 35.0, 4.2, 25.0, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Chhurpi.jpg/640px-Chhurpi.jpg"),
    ("Butter (Nauni)", "Eggs & Dairy", 717, 0.9, 0.1, 81.1, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Melted_butter.jpg/640px-Melted_butter.jpg"),
    ("Ghee", "Eggs & Dairy", 900, 0.0, 0.0, 100.0, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Ghee-vs-butter.jpg/640px-Ghee-vs-butter.jpg"),

    # Snacks & Street Food
    ("Momo (Steamed Dumpling)", "Street Food", 245, 12.5, 28.0, 9.0, 1.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Momo_Nepal.jpg/640px-Momo_Nepal.jpg"),
    ("Fried Momo", "Street Food", 320, 12.0, 28.5, 16.5, 1.2, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Momo_Nepal.jpg/640px-Momo_Nepal.jpg"),
    ("Chowmein (Stir-fried Noodles)", "Street Food", 310, 9.5, 52.0, 8.5, 2.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Chow_mein.jpg/640px-Chow_mein.jpg"),
    ("Thukpa (Noodle Soup)", "Street Food", 220, 11.0, 35.0, 5.0, 3.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Thukpa.jpg/640px-Thukpa.jpg"),
    ("Samosa", "Street Food", 262, 5.2, 32.8, 13.2, 2.8, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Samosa_2.jpg/640px-Samosa_2.jpg"),
    ("Chatpate", "Street Food", 180, 5.5, 32.0, 4.5, 4.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Chatpate.jpg/640px-Chatpate.jpg"),
    ("Aloo Tama (Potato Bamboo Curry)", "Traditional", 145, 4.5, 25.5, 3.5, 3.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Aloo_tama.jpg/640px-Aloo_tama.jpg"),
    ("Kheer (Rice Pudding)", "Sweets", 178, 4.5, 32.0, 5.0, 0.3, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Kheer.jpg/640px-Kheer.jpg"),
    ("Halwa", "Sweets", 284, 4.2, 52.0, 8.5, 1.5, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Halwa.jpg/640px-Halwa.jpg"),
    ("Jeri (Jalebi)", "Sweets", 337, 2.3, 67.5, 7.7, 0.3, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Jalebi.jpg/640px-Jalebi.jpg"),
    ("Yomari", "Traditional", 285, 5.5, 52.0, 7.5, 2.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Yomari.jpg/640px-Yomari.jpg"),
    ("Bara (Black Lentil Pancake)", "Traditional", 198, 9.5, 28.5, 5.5, 3.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Bara.jpg/640px-Bara.jpg"),
    ("Woh", "Traditional", 192, 9.0, 27.5, 5.8, 3.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Woh.jpg/640px-Woh.jpg"),
    ("Kwati (Mixed Bean Soup)", "Traditional", 148, 9.0, 24.5, 1.5, 7.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Kwati.jpg/640px-Kwati.jpg"),
    ("Aloo Achaar (Potato Pickle)", "Pickles", 95, 2.5, 18.5, 2.5, 2.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Aloo_achaar.jpg/640px-Aloo_achaar.jpg"),

    # Fruits
    ("Mango (Aap)", "Fruits", 60, 0.8, 15.0, 0.4, 1.6, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Hapus_Mango.jpg/640px-Hapus_Mango.jpg"),
    ("Banana (Kera)", "Fruits", 89, 1.1, 22.8, 0.3, 2.6, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Clip-Art.jpg/640px-Banana-Clip-Art.jpg"),
    ("Apple (Syau)", "Fruits", 52, 0.3, 13.8, 0.2, 2.4, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Red_Apple.jpg/640px-Red_Apple.jpg"),
    ("Orange (Suntala)", "Fruits", 47, 0.9, 11.8, 0.1, 2.4, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Ambersweet_oranges.jpg/640px-Ambersweet_oranges.jpg"),
    ("Papaya (Mewa)", "Fruits", 43, 0.5, 11.0, 0.3, 1.7, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Papaya_cross_section_and_slice.jpg/640px-Papaya_cross_section_and_slice.jpg"),
    ("Guava (Amba)", "Fruits", 68, 2.6, 14.3, 1.0, 5.4, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/24701-nature-natural-beauty.jpg/640px-24701-nature-natural-beauty.jpg"),
    ("Watermelon (Tarbuja)", "Fruits", 30, 0.6, 7.6, 0.2, 0.4, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Slices_of_watermelon.jpg/640px-Slices_of_watermelon.jpg"),
    ("Pineapple (Bhuin Katahar)", "Fruits", 50, 0.5, 13.1, 0.1, 1.4, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Pineapple_and_cross_section.jpg/640px-Pineapple_and_cross_section.jpg"),
    ("Litchi (Lichi)", "Fruits", 66, 0.8, 16.5, 0.4, 1.3, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Lychee_-_Lijiang.jpg/640px-Lychee_-_Lijiang.jpg"),
    ("Plum (Aarukhada)", "Fruits", 46, 0.7, 11.4, 0.3, 1.4, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Plums_2009.jpg/640px-Plums_2009.jpg"),
    ("Pomegranate (Anar)", "Fruits", 83, 1.7, 18.7, 1.2, 4.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Pomegranate_fruit_-_whole_and_sectioned.jpg/640px-Pomegranate_fruit_-_whole_and_sectioned.jpg"),
    ("Jackfruit (Katahar)", "Fruits", 95, 1.7, 23.2, 0.6, 1.5, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Jackfruit_section_07.jpg/640px-Jackfruit_section_07.jpg"),
    ("Avocado", "Fruits", 160, 2.0, 9.0, 14.7, 6.7, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Sliced_Avocados.jpg/640px-Sliced_Avocados.jpg"),

    # Beverages
    ("Milk Tea (Chiya)", "Beverages", 74, 2.2, 9.8, 3.1, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Milk_tea_2.jpg/640px-Milk_tea_2.jpg"),
    ("Black Tea", "Beverages", 1, 0.0, 0.2, 0.0, 0.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Black_tea_in_glass.jpg/640px-Black_tea_in_glass.jpg"),
    ("Lassi (Yogurt Drink)", "Beverages", 97, 4.1, 11.5, 4.2, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Lassi.jpg/640px-Lassi.jpg"),
    ("Tongba (Millet Beer)", "Beverages", 85, 1.5, 15.5, 0.5, 0.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Tongba.jpg/640px-Tongba.jpg"),
    ("Butter Tea (Churpi Chiya)", "Beverages", 105, 2.5, 4.5, 8.5, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Butter_tea.jpg/640px-Butter_tea.jpg"),

    # Nuts & Seeds
    ("Peanuts (Badaam)", "Nuts & Seeds", 567, 25.8, 16.1, 49.2, 8.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Peanuts_in_shells.jpg/640px-Peanuts_in_shells.jpg"),
    ("Sesame Seeds (Til)", "Nuts & Seeds", 573, 17.7, 23.4, 49.7, 11.8, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Sesame_Seeds_Macro.jpg/640px-Sesame_Seeds_Macro.jpg"),
    ("Walnuts (Okhar)", "Nuts & Seeds", 654, 15.2, 13.7, 65.2, 6.7, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Walnuts_in_bowl.jpg/640px-Walnuts_in_bowl.jpg"),
    ("Almonds", "Nuts & Seeds", 579, 21.2, 21.7, 49.9, 12.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Almonds_and_almond_nut_pieces.jpg/640px-Almonds_and_almond_nut_pieces.jpg"),
    ("Flaxseeds (Alsi)", "Nuts & Seeds", 534, 18.3, 28.9, 42.2, 27.3, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flax_Seeds.jpg/640px-Flax_Seeds.jpg"),

    # Oils & Condiments
    ("Mustard Oil", "Oils", 884, 0.0, 0.0, 100.0, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Mustard_oil.jpg/640px-Mustard_oil.jpg"),
    ("Coconut Oil", "Oils", 862, 0.0, 0.0, 100.0, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Coconut_oil.jpg/640px-Coconut_oil.jpg"),
    ("Soybean Oil", "Oils", 884, 0.0, 0.0, 100.0, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Soybean_oil.jpg/640px-Soybean_oil.jpg"),

    # Additional Traditional/Popular
    ("Aloo Paratha", "Bread & Roti", 300, 7.0, 42.0, 12.5, 3.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Aloo_paratha.jpg/640px-Aloo_paratha.jpg"),
    ("Saag (Leafy Green Curry)", "Vegetables", 65, 4.5, 7.5, 2.5, 4.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Saag_paneer.jpg/640px-Saag_paneer.jpg"),
    ("Biryani (Pulao)", "Rice & Grains", 290, 9.5, 45.5, 9.5, 2.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Biryani_at_Shiraz_Golden_Restaurant.jpg/640px-Biryani_at_Shiraz_Golden_Restaurant.jpg"),
    ("Fried Rice (Bhuteko Bhat)", "Rice & Grains", 238, 7.0, 38.5, 7.5, 1.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Fried_rice_2.jpg/640px-Fried_rice_2.jpg"),
    ("Noodle Soup (Wai Wai)", "Street Food", 330, 7.5, 47.0, 13.5, 1.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Wai_wai.jpg/640px-Wai_wai.jpg"),
    ("Fish Curry (Macha Ko Jhol)", "Fish & Seafood", 165, 18.5, 5.5, 7.5, 1.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Fish_curry.jpg/640px-Fish_curry.jpg"),
    ("Lemon (Kagati)", "Fruits", 29, 1.1, 9.3, 0.3, 2.8, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Citrus_limon_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-067.jpg/640px-Citrus_limon_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-067.jpg"),
    ("Brinjal/Eggplant (Bhanta)", "Vegetables", 25, 1.0, 5.9, 0.2, 3.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Aubergine.jpg/640px-Aubergine.jpg"),
    ("Ketchup (Tomato Sauce)", "Condiments", 112, 1.4, 26.6, 0.2, 0.3, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Tomato_ketchup_Fortnum_%26_Mason.jpg/640px-Tomato_ketchup_Fortnum_%26_Mason.jpg"),
    ("Pickle (Achaar)", "Pickles", 70, 1.5, 12.5, 2.5, 2.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Achar.jpg/640px-Achar.jpg"),
    ("Honey (Maaha)", "Sweets", 304, 0.3, 82.4, 0.0, 0.2, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Miel_-_abeilles.jpg/640px-Miel_-_abeilles.jpg"),
    ("Jaggery (Gud)", "Sweets", 383, 0.4, 98.0, 0.1, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Jaggery.jpg/640px-Jaggery.jpg"),
    ("Lapsi Candy (Hog Plum)", "Snacks", 44, 0.5, 10.9, 0.1, 1.8, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Lapsi.jpg/640px-Lapsi.jpg"),
    ("Popcorn", "Snacks", 375, 11.0, 74.3, 4.5, 14.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Popcorn_from_2009.jpg/640px-Popcorn_from_2009.jpg"),
    ("Roasted Corn (Bilaune Makai)", "Snacks", 352, 8.0, 73.5, 4.0, 7.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Corn_kernels.jpg/640px-Corn_kernels.jpg"),
    ("Saatu (Roasted Flour)", "Snacks", 388, 14.2, 70.5, 6.5, 4.5, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Sattu.jpg/640px-Sattu.jpg"),
    ("Nimki (Crackers)", "Snacks", 465, 8.5, 58.5, 22.5, 2.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Nimki.jpg/640px-Nimki.jpg"),
    ("Papad", "Snacks", 371, 19.5, 64.5, 4.5, 2.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Papad.jpg/640px-Papad.jpg"),
    ("Aloo Chips", "Snacks", 536, 7.0, 53.0, 34.5, 4.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Original_Lay%27s_Chips.JPG/640px-Original_Lay%27s_Chips.JPG"),
    ("Dhakane (Sprouted Gram)", "Snacks", 133, 9.0, 22.5, 0.8, 8.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Sprouts.jpg/640px-Sprouts.jpg"),
]

# Add more foods to reach 300+
EXTRA_FOODS = [
    ("Lentil Soup (Dal Jhol)", "Dal & Rice", 98, 6.5, 15.5, 1.2, 4.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Dal_bhat.jpg/640px-Dal_bhat.jpg"),
    ("Mixed Vegetable Curry", "Vegetables", 85, 3.0, 12.5, 3.0, 3.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Vegetable_curry.jpg/640px-Vegetable_curry.jpg"),
    ("Paneer Curry", "Eggs & Dairy", 290, 14.5, 7.5, 22.5, 1.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Paneer_tikka_masala.jpg/640px-Paneer_tikka_masala.jpg"),
    ("Tofu Stir Fry", "Protein Foods", 144, 10.5, 8.5, 8.0, 2.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Tofu_stir_fry.jpg/640px-Tofu_stir_fry.jpg"),
    ("Black Bean Curry", "Legumes", 155, 9.5, 24.5, 3.0, 8.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Black_Bean_Soup.jpg/640px-Black_Bean_Soup.jpg"),
    ("Corn Soup", "Soups", 75, 2.5, 15.5, 1.0, 1.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Corn_soup.jpg/640px-Corn_soup.jpg"),
    ("Tomato Soup", "Soups", 55, 1.5, 11.5, 0.8, 1.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Tomato_soup.jpg/640px-Tomato_soup.jpg"),
    ("Vegetable Soup", "Soups", 65, 3.0, 12.5, 1.0, 3.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Vegetable_soup.jpg/640px-Vegetable_soup.jpg"),
    ("Chicken Soup", "Soups", 75, 8.5, 5.0, 2.5, 0.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Chicken_soup.jpg/640px-Chicken_soup.jpg"),
    ("Fried Chicken", "Meat", 265, 23.5, 8.5, 15.5, 0.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Fried_chicken.jpg/640px-Fried_chicken.jpg"),
    ("Grilled Chicken Breast", "Meat", 165, 31.0, 0.0, 3.6, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Grilled_chicken.jpg/640px-Grilled_chicken.jpg"),
    ("Tuna (Canned)", "Fish & Seafood", 116, 26.0, 0.0, 1.0, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Canned_tuna_in_water.jpg/640px-Canned_tuna_in_water.jpg"),
    ("Salmon Fillet", "Fish & Seafood", 208, 20.0, 0.0, 13.4, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Salmon_Slice.jpg/640px-Salmon_Slice.jpg"),
    ("Greek Yogurt", "Eggs & Dairy", 59, 10.0, 3.6, 0.4, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Bowl_of_yogurt.jpg/640px-Bowl_of_yogurt.jpg"),
    ("Low Fat Milk", "Eggs & Dairy", 35, 3.4, 4.8, 0.2, 0.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Milk_glass.jpg/640px-Milk_glass.jpg"),
    ("Whole Wheat Bread", "Bread & Roti", 247, 13.0, 41.0, 3.4, 7.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Whole_wheat_bread.jpg/640px-Whole_wheat_bread.jpg"),
    ("White Bread", "Bread & Roti", 265, 9.0, 49.0, 3.2, 2.7, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_bread_05.jpg/640px-Fresh_made_bread_05.jpg"),
    ("Pasta (Macaroni)", "Rice & Grains", 371, 13.0, 74.7, 1.5, 3.2, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Macaroni_and_cheese.jpg/640px-Macaroni_and_cheese.jpg"),
    ("Pizza (Slice)", "Street Food", 266, 11.0, 33.0, 10.4, 2.3, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/640px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"),
    ("Burger", "Street Food", 295, 17.0, 24.0, 14.0, 1.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/640px-PNG_transparency_demonstration_1.png"),
    ("French Fries", "Street Food", 312, 3.4, 41.4, 15.0, 3.8, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Potato-Chips.jpg/640px-Potato-Chips.jpg"),
    ("Sandwich", "Street Food", 250, 10.5, 33.5, 8.5, 3.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Club_sandwich.JPG/640px-Club_sandwich.JPG"),
    ("Idli", "Traditional", 58, 2.7, 11.8, 0.4, 0.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Idli_Sambar.jpg/640px-Idli_Sambar.jpg"),
    ("Dosa", "Traditional", 165, 4.5, 30.0, 3.5, 1.2, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Plain_dosa.jpg/640px-Plain_dosa.jpg"),
    ("Upma", "Traditional", 150, 4.0, 28.0, 3.5, 2.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Upma_in_bowl.jpg/640px-Upma_in_bowl.jpg"),
    ("Poha (Flattened Rice)", "Traditional", 250, 4.0, 47.5, 6.0, 1.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Poha_dish.jpg/640px-Poha_dish.jpg"),
    ("Cereal (Corn Flakes)", "Breakfast Foods", 357, 7.5, 84.0, 0.9, 1.2, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Cornflakes.JPG/640px-Cornflakes.JPG"),
    ("Muesli", "Breakfast Foods", 370, 11.5, 65.0, 8.5, 7.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Muesli_assorment.jpg/640px-Muesli_assorment.jpg"),
    ("Granola", "Breakfast Foods", 471, 10.0, 64.0, 20.0, 6.5, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Granola.jpg/640px-Granola.jpg"),
    ("Protein Bar", "Supplements", 370, 25.0, 48.0, 8.5, 5.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Protein_bar.jpg/640px-Protein_bar.jpg"),
    ("Protein Shake", "Supplements", 200, 30.0, 10.0, 3.5, 1.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Protein_shake.jpg/640px-Protein_shake.jpg"),
    ("Energy Drink", "Beverages", 112, 1.0, 28.0, 0.0, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Red_Bull_Energy_Drink.jpg/640px-Red_Bull_Energy_Drink.jpg"),
    ("Orange Juice", "Beverages", 45, 0.7, 10.4, 0.2, 0.2, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Hapus_Mango.jpg/640px-Hapus_Mango.jpg"),
    ("Coconut Water", "Beverages", 19, 0.7, 3.7, 0.2, 1.1, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Coconut_water.jpg/640px-Coconut_water.jpg"),
    ("Sugarcane Juice (Ukhoo Ras)", "Beverages", 78, 0.3, 19.5, 0.1, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Sugarcane_juice.jpg/640px-Sugarcane_juice.jpg"),
    ("Coffee (Black)", "Beverages", 1, 0.3, 0.0, 0.0, 0.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/A_small_cup_of_coffee.JPG/640px-A_small_cup_of_coffee.JPG"),
    ("Lemon Water", "Beverages", 11, 0.1, 3.5, 0.0, 0.1, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Lemon_water.jpg/640px-Lemon_water.jpg"),
    ("Strawberry", "Fruits", 32, 0.7, 7.7, 0.3, 2.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/PerfectStrawberry.jpg/640px-PerfectStrawberry.jpg"),
    ("Grapes (Angur)", "Fruits", 67, 0.6, 17.2, 0.4, 0.9, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Table_grapes_on_white.jpg/640px-Table_grapes_on_white.jpg"),
    ("Kiwi", "Fruits", 61, 1.1, 14.7, 0.5, 3.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Kiwi_-_Rayda.jpg/640px-Kiwi_-_Rayda.jpg"),
    ("Pear (Naspati)", "Fruits", 57, 0.4, 15.2, 0.1, 3.1, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Pears.jpg/640px-Pears.jpg"),
    ("Fig (Anjir)", "Fruits", 74, 0.75, 19.2, 0.3, 2.9, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Figs.jpg/640px-Figs.jpg"),
    ("Dates (Khurmah)", "Fruits", 277, 1.8, 74.97, 0.2, 6.7, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Dates_on_a_palm_frond.jpg/640px-Dates_on_a_palm_frond.jpg"),
    ("Raisins (Kismis)", "Fruits", 299, 3.1, 79.2, 0.5, 3.7, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Dried_raisins.jpg/640px-Dried_raisins.jpg"),
    ("Asparagus", "Vegetables", 20, 2.2, 3.7, 0.1, 2.1, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Asparagus_officinalis_0.01.jpg/640px-Asparagus_officinalis_0.01.jpg"),
    ("Bell Pepper (Capsicum)", "Vegetables", 31, 1.0, 7.3, 0.3, 2.1, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Bell_pepper_2.jpg/640px-Bell_pepper_2.jpg"),
    ("Mushroom (Chyau)", "Vegetables", 22, 3.1, 3.3, 0.3, 1.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Mushroom_-_Fungus.jpg/640px-Mushroom_-_Fungus.jpg"),
    ("Zucchini", "Vegetables", 17, 1.2, 3.1, 0.3, 1.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Zucchini_R.jpg/640px-Zucchini_R.jpg"),
    ("Celery", "Vegetables", 16, 0.7, 3.0, 0.2, 1.6, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Celery_Pascal.jpg/640px-Celery_Pascal.jpg"),
    ("Leek", "Vegetables", 61, 1.5, 14.2, 0.3, 1.8, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Leeks_on_white.jpg/640px-Leeks_on_white.jpg"),
    ("Bottle Gourd (Lauka)", "Vegetables", 14, 0.6, 3.4, 0.0, 0.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Lauki.JPG/640px-Lauki.JPG"),
    ("Ridge Gourd (Ghiraula)", "Vegetables", 20, 1.2, 4.4, 0.2, 0.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Luffa_acutangula_fruits.jpg/640px-Luffa_acutangula_fruits.jpg"),
    ("Sponge Gourd (Pharsi Chana)", "Vegetables", 18, 1.2, 3.5, 0.2, 0.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Luffa_cylindrica.JPG/640px-Luffa_cylindrica.JPG"),
    ("Turnip (Salgam)", "Vegetables", 28, 0.9, 6.4, 0.1, 1.8, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Turnip_2622027.jpg/640px-Turnip_2622027.jpg"),
    ("Yam (Tarul)", "Vegetables", 118, 1.5, 27.9, 0.2, 4.1, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Yam_Guinea_closeup.jpg/640px-Yam_Guinea_closeup.jpg"),
    ("Colocasia (Karkalo)", "Vegetables", 112, 1.5, 26.5, 0.2, 4.1, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Colocasia_esculenta_leaves_and_taro.jpg/640px-Colocasia_esculenta_leaves_and_taro.jpg"),
    ("Fried Egg (Omelette)", "Eggs & Dairy", 154, 10.6, 0.4, 11.7, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Scrambled_eggs.jpg/640px-Scrambled_eggs.jpg"),
    ("Curd Rice", "Rice & Grains", 145, 4.0, 28.5, 2.5, 0.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Curd_rice.jpg/640px-Curd_rice.jpg"),
    ("Vegetable Biryani", "Rice & Grains", 240, 6.0, 42.0, 7.0, 3.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Biryani_at_Shiraz_Golden_Restaurant.jpg/640px-Biryani_at_Shiraz_Golden_Restaurant.jpg"),
    ("Mutton Biryani", "Rice & Grains", 340, 16.0, 38.0, 14.5, 2.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Biryani_at_Shiraz_Golden_Restaurant.jpg/640px-Biryani_at_Shiraz_Golden_Restaurant.jpg"),
    ("Chicken Biryani", "Rice & Grains", 290, 16.0, 38.5, 9.0, 2.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Biryani_at_Shiraz_Golden_Restaurant.jpg/640px-Biryani_at_Shiraz_Golden_Restaurant.jpg"),
    ("Lemon Rice", "Rice & Grains", 185, 3.5, 36.5, 4.0, 1.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Banquet_rice.jpg/640px-Banquet_rice.jpg"),
    ("Tomato Rice", "Rice & Grains", 178, 3.5, 35.5, 3.5, 2.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Banquet_rice.jpg/640px-Banquet_rice.jpg"),
    ("Pea Pulao", "Rice & Grains", 215, 5.5, 38.0, 5.5, 3.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Banquet_rice.jpg/640px-Banquet_rice.jpg"),
    ("Khichdi", "Dal & Rice", 165, 6.5, 28.0, 3.5, 3.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Dal_bhat.jpg/640px-Dal_bhat.jpg"),
    ("Chapati with Sabzi", "Bread & Roti", 220, 7.0, 35.5, 6.0, 5.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Chapati.jpg/640px-Chapati.jpg"),
    ("Naan", "Bread & Roti", 262, 8.7, 45.4, 5.1, 1.6, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Naan.jpg/640px-Naan.jpg"),
    ("Tandoori Chicken", "Meat", 200, 25.0, 6.0, 9.0, 0.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Tandoori_chicken.jpg/640px-Tandoori_chicken.jpg"),
    ("Kebab", "Meat", 235, 22.5, 5.5, 14.0, 0.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Seekh_kebab.jpg/640px-Seekh_kebab.jpg"),
    ("Lamb/Mutton Sekuwa", "Meat", 285, 26.5, 2.0, 18.5, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Mutton_curry.jpg/640px-Mutton_curry.jpg"),
    ("Chicken Sekuwa", "Meat", 215, 28.5, 2.5, 10.5, 0.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Fried_chicken.jpg/640px-Fried_chicken.jpg"),
    ("Buff Choila", "Meat", 250, 28.0, 3.5, 14.0, 0.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Raw_meat.jpg/640px-Raw_meat.jpg"),
    ("Egg Bhurji", "Eggs & Dairy", 175, 10.5, 3.5, 12.5, 0.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Scrambled_eggs.jpg/640px-Scrambled_eggs.jpg"),
    ("Masala Omelette", "Eggs & Dairy", 165, 10.0, 3.5, 12.0, 1.0, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Scrambled_eggs.jpg/640px-Scrambled_eggs.jpg"),
    ("Rabadi (Thickened Milk)", "Eggs & Dairy", 155, 6.0, 22.5, 5.5, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Milk_glass.jpg/640px-Milk_glass.jpg"),
    ("Shrikhand", "Eggs & Dairy", 225, 8.5, 37.5, 6.0, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Bowl_of_yogurt.jpg/640px-Bowl_of_yogurt.jpg"),
    ("Peda (Milk Sweet)", "Sweets", 365, 8.5, 62.5, 10.5, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Mathura_ke_pede.jpg/640px-Mathura_ke_pede.jpg"),
    ("Barfi (Milk Fudge)", "Sweets", 393, 9.5, 67.5, 11.5, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Barfi_sweets.jpg/640px-Barfi_sweets.jpg"),
    ("Gajar Halwa (Carrot Pudding)", "Sweets", 285, 5.5, 42.5, 12.0, 2.5, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Halwa.jpg/640px-Halwa.jpg"),
    ("Rosogolla", "Sweets", 125, 3.5, 25.5, 1.5, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Rosogolla_sweet.jpg/640px-Rosogolla_sweet.jpg"),
    ("Gulab Jamun", "Sweets", 175, 3.5, 30.5, 5.5, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Gulab_jamun_%28GJ%29.jpg/640px-Gulab_jamun_%28GJ%29.jpg"),
    ("Rasgulla", "Sweets", 125, 3.5, 25.0, 1.5, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Rosogolla_sweet.jpg/640px-Rosogolla_sweet.jpg"),
    ("Kulfi (Ice Cream)", "Sweets", 196, 5.0, 32.5, 6.5, 0.0, "weight_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Kulfi_ice_cream.jpg/640px-Kulfi_ice_cream.jpg"),
    ("Mango Lassi", "Beverages", 128, 3.5, 24.5, 2.5, 0.5, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Lassi.jpg/640px-Lassi.jpg"),
    ("Rose Sherbet", "Beverages", 110, 0.2, 27.5, 0.0, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Rose_Sharbat.jpg/640px-Rose_Sharbat.jpg"),
    ("Nimbu Pani (Lemonade)", "Beverages", 25, 0.1, 6.5, 0.0, 0.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Lemon_water.jpg/640px-Lemon_water.jpg"),
    ("Turmeric Milk (Haldi Doodh)", "Beverages", 75, 3.5, 7.5, 3.0, 0.0, "maintenance",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Milk_glass.jpg/640px-Milk_glass.jpg"),
    ("Almond Milk", "Beverages", 39, 1.5, 3.5, 2.5, 0.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Milk_glass.jpg/640px-Milk_glass.jpg"),
    ("Sprouts Salad", "Salads", 115, 9.0, 18.5, 0.8, 8.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Sprouts.jpg/640px-Sprouts.jpg"),
    ("Mixed Green Salad", "Salads", 35, 2.5, 6.5, 0.5, 3.0, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Mixed_salad_greens.jpg/640px-Mixed_salad_greens.jpg"),
    ("Cucumber Tomato Salad", "Salads", 28, 1.5, 5.5, 0.3, 1.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Cucumber_salad.jpg/640px-Cucumber_salad.jpg"),
    ("Fruit Salad (Phalphul)", "Salads", 60, 1.0, 15.0, 0.3, 2.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Fruit_salad.jpg/640px-Fruit_salad.jpg"),
    ("Chickpea Salad (Chana Chat)", "Salads", 155, 8.5, 25.5, 2.5, 7.5, "weight_loss",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Chickpeas_%28garbanzo_beans%29.jpg/640px-Chickpeas_%28garbanzo_beans%29.jpg"),
    ("Paleo Mix (Nuts & Dry Fruits)", "Snacks", 490, 12.0, 42.0, 32.5, 7.5, "muscle_gain",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Peanuts_in_shells.jpg/640px-Peanuts_in_shells.jpg"),
]

all_foods = FOODS + EXTRA_FOODS

print(f"Total food records: {len(all_foods)}")

# Write food_dataset.csv
with open("food_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["food_id","food_name","category","calories","protein","carbohydrates",
                     "fat","fiber","serving_size","recommended_goal","image_url"])
    for i, food in enumerate(all_foods, 1):
        name, cat, cal, prot, carbs, fat, fib, goal, img = food
        writer.writerow([i, name, cat, cal, prot, carbs, fat, fib, "100g", goal, img])

print("[OK] food_dataset.csv written")


# ============================================================
# DATASET 2: user_profile_dataset.csv
# ============================================================
ACTIVITY_LEVELS = ["sedentary","lightly_active","moderately_active","very_active"]
GOALS          = ["weight_loss","weight_gain","muscle_gain","maintenance"]
GENDERS        = ["male","female"]
GOAL_TO_CAT    = {
    "weight_loss":  "Low Calorie",
    "weight_gain":  "High Energy",
    "muscle_gain":  "High Protein",
    "maintenance":  "Balanced Diet",
}

def calc_bmi(weight, height_cm):
    return round(weight / ((height_cm/100)**2), 2)

def assign_category(gender, bmi, activity, goal):
    if goal == "weight_loss" or bmi >= 27.5:
        return "Low Calorie"
    if goal == "muscle_gain" or (activity in ["moderately_active","very_active"] and bmi < 25):
        return "High Protein"
    if goal == "weight_gain" or bmi < 18.5:
        return "High Energy"
    if bmi >= 25:
        return "Fiber Rich"
    return "Balanced Diet"

users = []
for uid in range(1, 2001):
    gender  = random.choice(GENDERS)
    age     = random.randint(15, 65)
    height  = round(random.uniform(148.0, 185.0), 1) if gender=="male" else round(random.uniform(145.0, 175.0), 1)
    weight  = round(random.uniform(45.0, 100.0), 1)
    bmi     = calc_bmi(weight, height)
    activity= random.choice(ACTIVITY_LEVELS)
    goal    = random.choice(GOALS)
    cat     = assign_category(gender, bmi, activity, goal)
    calorie_goal = 2000
    if goal == "weight_loss":  calorie_goal = random.randint(1400, 1800)
    elif goal == "weight_gain": calorie_goal = random.randint(2500, 3200)
    elif goal == "muscle_gain": calorie_goal = random.randint(2200, 2800)
    else:                       calorie_goal = random.randint(1800, 2200)

    users.append([uid, age, gender, height, weight, bmi, activity, goal, cat, calorie_goal])

with open("user_profile_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["user_id","age","gender","height_cm","weight_kg","bmi",
                     "activity_level","nutrition_goal","recommended_category","daily_calorie_goal"])
    writer.writerows(users)
print("[OK] user_profile_dataset.csv written (2000 users)")


# ============================================================
# DATASET 3: food_history_dataset.csv
# ============================================================
base_date = datetime(2024, 1, 1)
food_ids  = list(range(1, len(all_foods)+1))

history_rows = []
for _ in range(8000):
    uid  = random.randint(1, 2000)
    fid  = random.choice(food_ids)
    freq = random.randint(1, 20)
    days_offset = random.randint(0, 180)
    ts   = (base_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
    history_rows.append([uid, fid, freq, ts])

with open("food_history_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["user_id","food_id","frequency","timestamp"])
    writer.writerows(history_rows)
print("[OK] food_history_dataset.csv written (8000 records)")


# ============================================================
# DATASET 4: nutrition_intake_dataset.csv
# ============================================================
nutrition_rows = []
for uid in range(1, 2001):
    goal = users[uid-1][7]
    if goal == "weight_loss":
        base_cal  = random.uniform(1200, 1800)
        base_prot = random.uniform(60, 100)
    elif goal == "muscle_gain":
        base_cal  = random.uniform(2200, 3000)
        base_prot = random.uniform(120, 180)
    elif goal == "weight_gain":
        base_cal  = random.uniform(2500, 3500)
        base_prot = random.uniform(80, 130)
    else:
        base_cal  = random.uniform(1800, 2200)
        base_prot = random.uniform(70, 110)

    carbs = round(base_cal * 0.5 / 4, 1)
    fat   = round(base_cal * 0.3 / 9, 1)
    fiber = round(random.uniform(15, 35), 1)
    nutrition_rows.append([uid, round(base_cal,1), round(base_prot,1), carbs, fat, fiber])

with open("nutrition_intake_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["user_id","calories","protein","carbohydrates","fat","fiber"])
    writer.writerows(nutrition_rows)
print("[OK] nutrition_intake_dataset.csv written (2000 records)")


# ============================================================
# DATASET 5: meal_plan_dataset.csv
# ============================================================
BREAKFAST_FOODS = ["Oatmeal (Jaulo)","Chiura (Beaten Rice)","Sel Roti","Bara (Black Lentil Pancake)",
                   "Poha (Flattened Rice)","Boiled Egg","Milk Tea (Chiya)","Roti (Wheat Flatbread)",
                   "Idli","Cereal (Corn Flakes)","Muesli","Granola","Scrambled Eggs"]
LUNCH_FOODS     = ["Dal Bhat","Momo (Steamed Dumpling)","Chicken Curry","Aloo Tama (Potato Bamboo Curry)",
                   "Khichdi","Chapati with Sabzi","Thukpa (Noodle Soup)","Vegetable Biryani",
                   "Masoor Dal","Gundruk","Mixed Vegetable Curry","Paneer Curry"]
DINNER_FOODS    = ["Dal Bhat","Roti (Wheat Flatbread)","Grilled Chicken Breast","Mutton Curry",
                   "Fish Curry (Macha Ko Jhol)","Vegetable Soup","Chicken Soup","Buff Choila",
                   "Tofu Stir Fry","Brown Rice","Saag (Leafy Green Curry)","Curd Rice"]
SNACK_FOODS     = ["Peanuts (Badaam)","Fruit Salad (Phalphul)","Yogurt (Dahi)","Lapsi Candy (Hog Plum)",
                   "Roasted Corn (Bilaune Makai)","Chatpate","Sprouts Salad","Popcorn",
                   "Mixed Green Salad","Apple (Syau)","Banana (Kera)","Protein Bar"]

meal_plan_rows = []
for i in range(400):
    goal = random.choice(GOALS)
    meal_plan_rows.append([
        random.choice(BREAKFAST_FOODS),
        random.choice(LUNCH_FOODS),
        random.choice(DINNER_FOODS),
        random.choice(SNACK_FOODS),
        goal
    ])

with open("meal_plan_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["breakfast","lunch","dinner","snack","nutrition_goal"])
    writer.writerows(meal_plan_rows)
print("[OK] meal_plan_dataset.csv written (400 records)")


# ============================================================
# DATASET 6: bmi_recommendation_dataset.csv
# ============================================================
bmi_data = [
    ("< 16.0",    "Severe Thinness",    "High Energy"),
    ("16.0-16.9", "Moderate Thinness",  "High Energy"),
    ("17.0-18.4", "Mild Thinness",      "High Energy"),
    ("18.5-24.9", "Normal Weight",      "Balanced Diet"),
    ("25.0-27.4", "Pre-Obese",          "Low Calorie"),
    ("27.5-29.9", "Overweight",         "Low Calorie"),
    ("30.0-34.9", "Obese Class I",      "Low Calorie"),
    ("35.0-39.9", "Obese Class II",     "Low Calorie"),
    (">= 40.0",   "Obese Class III",    "Low Calorie"),
]

with open("bmi_recommendation_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["bmi_range","bmi_category","recommendation_type"])
    writer.writerows(bmi_data)
print("[OK] bmi_recommendation_dataset.csv written")

print("\nAll datasets generated successfully.")
