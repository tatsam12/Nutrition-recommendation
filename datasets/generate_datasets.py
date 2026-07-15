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
     "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=600&q=80"),
    ("Masoor Dal", "Legumes", 116, 9.0, 20.0, 0.4, 3.9, "weight_loss",
     "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80"),
    ("Chana Dal", "Legumes", 164, 8.9, 27.4, 2.6, 7.6, "weight_loss",
     "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=600&q=80"),
    ("Mung Dal", "Legumes", 105, 7.0, 19.2, 0.4, 7.6, "weight_loss",
     "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?auto=format&fit=crop&w=600&q=80"),
    ("Toor Dal", "Legumes", 118, 6.8, 20.6, 0.4, 5.0, "maintenance",
     "https://images.unsplash.com/photo-1585821937315-f1a029756611?auto=format&fit=crop&w=600&q=80"),
    ("Black Dal (Kali Dal)", "Legumes", 127, 9.0, 21.6, 0.8, 5.3, "muscle_gain",
     "https://images.unsplash.com/photo-1608219990948-21934c77b8cb?auto=format&fit=crop&w=600&q=80"),
    ("Kidney Beans (Rajma)", "Legumes", 127, 8.7, 22.8, 0.5, 6.4, "muscle_gain",
     "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=600&q=80"),
    ("Soybean", "Legumes", 173, 16.6, 9.0, 9.0, 6.0, "muscle_gain",
     "https://images.unsplash.com/photo-1599599810769-bcde5a160d32?auto=format&fit=crop&w=600&q=80"),
    ("Chickpeas (Chana)", "Legumes", 164, 8.9, 27.4, 2.6, 7.6, "weight_loss",
     "https://images.unsplash.com/photo-1585821937315-f1a029756611?auto=format&fit=crop&w=600&q=80"),

    # Rice & Grains
    ("Steamed Rice", "Rice & Grains", 204, 4.2, 44.5, 0.4, 0.6, "maintenance",
     "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=600&q=80"),
    ("Brown Rice", "Rice & Grains", 216, 5.0, 44.8, 1.8, 3.5, "weight_loss",
     "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80"),
    ("Chiura (Beaten Rice)", "Rice & Grains", 346, 6.9, 76.9, 1.4, 1.7, "maintenance",
     "https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=600&q=80"),
    ("Dhido (Buckwheat Porridge)", "Traditional", 161, 5.7, 33.5, 1.0, 2.7, "weight_loss",
     "https://images.unsplash.com/photo-1541832676-9b763b0239ab?auto=format&fit=crop&w=600&q=80"),
    ("Roti (Wheat Flatbread)", "Bread & Roti", 297, 9.7, 57.5, 3.5, 5.5, "maintenance",
     "https://images.unsplash.com/photo-1613564834644-a170dc930e40?auto=format&fit=crop&w=600&q=80"),
    ("Makai Roti (Corn Flatbread)", "Bread & Roti", 218, 5.1, 45.5, 2.1, 3.8, "weight_loss",
     "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80"),
    ("Puri", "Bread & Roti", 349, 7.0, 48.0, 16.0, 2.0, "weight_gain",
     "https://images.unsplash.com/photo-1626132647523-66f5bf380027?auto=format&fit=crop&w=600&q=80"),
    ("Sel Roti", "Traditional", 325, 5.0, 55.0, 10.5, 1.2, "maintenance",
     "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=600&q=80"),
    ("Oatmeal (Jaulo)", "Rice & Grains", 158, 5.6, 27.4, 3.2, 4.0, "weight_loss",
     "https://images.unsplash.com/photo-1517849058932-d9065dc93e93?auto=format&fit=crop&w=600&q=80"),
    ("Millet (Kodo)", "Rice & Grains", 378, 11.0, 72.8, 4.2, 8.5, "weight_loss",
     "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?auto=format&fit=crop&w=600&q=80"),
    ("Corn (Makai)", "Rice & Grains", 96, 3.4, 21.0, 1.5, 2.4, "maintenance",
     "https://images.unsplash.com/photo-1551754625-40137410b915?auto=format&fit=crop&w=600&q=80"),

    # Vegetables
    ("Gundruk", "Fermented Foods", 30, 2.5, 5.5, 0.5, 3.0, "weight_loss",
     "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80"),
    ("Spinach (Palungo)", "Vegetables", 23, 2.9, 3.6, 0.4, 2.2, "weight_loss",
     "https://images.unsplash.com/photo-1576045057995-568f588f82fb?auto=format&fit=crop&w=600&q=80"),
    ("Cauliflower (Kauli)", "Vegetables", 25, 1.9, 5.0, 0.3, 2.0, "weight_loss",
     "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?auto=format&fit=crop&w=600&q=80"),
    ("Cabbage (Bandakopi)", "Vegetables", 25, 1.3, 5.8, 0.1, 2.5, "weight_loss",
     "https://images.unsplash.com/photo-1606787366850-de6330128bfc?auto=format&fit=crop&w=600&q=80"),
    ("Potato (Aloo)", "Vegetables", 77, 2.0, 17.5, 0.1, 2.2, "maintenance",
     "https://images.unsplash.com/photo-1518977676601-b53f02db1d2d?auto=format&fit=crop&w=600&q=80"),
    ("Tomato", "Vegetables", 18, 0.9, 3.9, 0.2, 1.2, "weight_loss",
     "https://images.unsplash.com/photo-1595855759920-86582396756a?auto=format&fit=crop&w=600&q=80"),
    ("Cucumber (Kakro)", "Vegetables", 16, 0.7, 3.6, 0.1, 0.5, "weight_loss",
     "https://images.unsplash.com/photo-1604974244131-030ec60cf880?auto=format&fit=crop&w=600&q=80"),
    ("Onion (Pyaj)", "Vegetables", 40, 1.1, 9.3, 0.1, 1.7, "weight_loss",
     "https://images.unsplash.com/photo-1508747703725-719777637510?auto=format&fit=crop&w=600&q=80"),
    ("Garlic (Lasun)", "Vegetables", 149, 6.4, 33.1, 0.5, 2.1, "maintenance",
     "https://images.unsplash.com/photo-1540148426945-6cf22a6b2383?auto=format&fit=crop&w=600&q=80"),
    ("Ginger (Adrak)", "Vegetables", 80, 1.8, 17.8, 0.8, 2.0, "maintenance",
     "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?auto=format&fit=crop&w=600&q=80"),
    ("Radish (Mula)", "Vegetables", 16, 0.7, 3.4, 0.1, 1.6, "weight_loss",
     "https://images.unsplash.com/photo-1592394533824-9440e5d68514?auto=format&fit=crop&w=600&q=80"),
    ("Carrot (Gajar)", "Vegetables", 41, 0.9, 9.6, 0.2, 2.8, "weight_loss",
     "https://images.unsplash.com/photo-1598170845058-32b996a6885e?auto=format&fit=crop&w=600&q=80"),
    ("Broccoli", "Vegetables", 34, 2.8, 6.6, 0.4, 2.6, "weight_loss",
     "https://images.unsplash.com/photo-1453133451515-5ff7c1d0d63c?auto=format&fit=crop&w=600&q=80"),
    ("Bitter Gourd (Karela)", "Vegetables", 17, 1.0, 3.7, 0.2, 2.8, "weight_loss",
     "https://images.unsplash.com/photo-1587486913049-53fc88980cfc?auto=format&fit=crop&w=600&q=80"),
    ("Pumpkin (Farsi)", "Vegetables", 26, 1.0, 6.5, 0.1, 0.5, "weight_loss",
     "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80"),
    ("Bamboo Shoot (Tama)", "Vegetables", 27, 2.6, 5.2, 0.3, 2.2, "weight_loss",
     "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80"),
    ("Mustard Greens (Rayo Saag)", "Vegetables", 27, 2.7, 4.7, 0.4, 3.2, "weight_loss",
     "https://images.unsplash.com/photo-1576045057995-568f588f82fb?auto=format&fit=crop&w=600&q=80"),
    ("Fenugreek Leaves (Methi)", "Vegetables", 49, 4.4, 6.0, 0.9, 2.7, "weight_loss",
     "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80"),
    ("Green Peas (Kerau)", "Vegetables", 81, 5.4, 14.5, 0.4, 5.1, "maintenance",
     "https://images.unsplash.com/photo-1587486913049-53fc88980cfc?auto=format&fit=crop&w=600&q=80"),
    ("Sweet Potato (Sakhar Kanda)", "Vegetables", 86, 1.6, 20.1, 0.1, 3.0, "maintenance",
     "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?auto=format&fit=crop&w=600&q=80"),

    # Meat & Poultry
    ("Buffalo Meat (Buff)", "Meat", 131, 26.0, 0.0, 2.8, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80"),
    ("Chicken Curry", "Meat", 215, 23.0, 5.2, 11.5, 0.5, "muscle_gain",
     "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=600&q=80"),
    ("Mutton Curry", "Meat", 258, 24.5, 4.0, 16.2, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=600&q=80"),
    ("Sukuti (Dried Meat)", "Meat", 234, 40.0, 2.0, 6.5, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1608219990948-21934c77b8cb?auto=format&fit=crop&w=600&q=80"),
    ("Pork (Sungur)", "Meat", 242, 27.3, 0.0, 14.4, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1602489107164-b841194975db?auto=format&fit=crop&w=600&q=80"),
    ("Duck (Hans)", "Meat", 337, 19.0, 0.0, 28.4, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80"),

    # Seafood & Fish
    ("Rohu Fish (Rohu Macha)", "Fish & Seafood", 97, 16.7, 0.0, 3.0, 0.0, "weight_loss",
     "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80"),
    ("Catfish", "Fish & Seafood", 116, 18.0, 0.0, 4.3, 0.0, "weight_loss",
     "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80"),
    ("Dried Fish (Sidra)", "Fish & Seafood", 290, 55.0, 0.0, 6.5, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1608219990948-21934c77b8cb?auto=format&fit=crop&w=600&q=80"),
    ("Crab Curry", "Fish & Seafood", 119, 16.5, 3.5, 4.8, 0.0, "weight_loss",
     "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80"),

    # Eggs & Dairy
    ("Boiled Egg", "Eggs & Dairy", 155, 13.0, 1.1, 11.0, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1516685018646-549198525c1b?auto=format&fit=crop&w=600&q=80"),
    ("Egg Curry", "Eggs & Dairy", 185, 11.8, 6.2, 12.5, 0.8, "muscle_gain",
     "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=600&q=80"),
    ("Scrambled Eggs", "Eggs & Dairy", 149, 10.1, 1.6, 11.2, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1516685018646-549198525c1b?auto=format&fit=crop&w=600&q=80"),
    ("Milk (Dudh)", "Eggs & Dairy", 42, 3.4, 4.8, 1.0, 0.0, "maintenance",
     "https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=600&q=80"),
    ("Buffalo Milk", "Eggs & Dairy", 97, 3.8, 5.0, 6.9, 0.0, "weight_gain",
     "https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=600&q=80"),
    ("Yogurt (Dahi)", "Eggs & Dairy", 61, 3.5, 4.7, 3.3, 0.0, "maintenance",
     "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=600&q=80"),
    ("Paneer (Chhurpi Fresh)", "Eggs & Dairy", 265, 18.3, 3.4, 20.8, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=600&q=80"),
    ("Hard Chhurpi", "Eggs & Dairy", 380, 35.0, 4.2, 25.0, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=600&q=80"),
    ("Butter (Nauni)", "Eggs & Dairy", 717, 0.9, 0.1, 81.1, 0.0, "weight_gain",
     "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&w=600&q=80"),
    ("Ghee", "Eggs & Dairy", 900, 0.0, 0.0, 100.0, 0.0, "weight_gain",
     "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&w=600&q=80"),

    # Snacks & Street Food
    ("Momo (Steamed Dumpling)", "Street Food", 245, 12.5, 28.0, 9.0, 1.5, "maintenance",
     "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=600&q=80"),
    ("Fried Momo", "Street Food", 320, 12.0, 28.5, 16.5, 1.2, "maintenance",
     "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=600&q=80"),
    ("Chowmein (Stir-fried Noodles)", "Street Food", 310, 9.5, 52.0, 8.5, 2.5, "maintenance",
     "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80"),
    ("Thukpa (Noodle Soup)", "Street Food", 220, 11.0, 35.0, 5.0, 3.0, "weight_loss",
     "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80"),
    ("Samosa", "Street Food", 262, 5.2, 32.8, 13.2, 2.8, "maintenance",
     "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?auto=format&fit=crop&w=600&q=80"),
    ("Chatpate", "Street Food", 180, 5.5, 32.0, 4.5, 4.0, "weight_loss",
     "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=600&q=80"),
    ("Aloo Tama (Potato Bamboo Curry)", "Traditional", 145, 4.5, 25.5, 3.5, 3.5, "maintenance",
     "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80"),
    ("Kheer (Rice Pudding)", "Sweets", 178, 4.5, 32.0, 5.0, 0.3, "weight_gain",
     "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=600&q=80"),
    ("Halwa", "Sweets", 284, 4.2, 52.0, 8.5, 1.5, "weight_gain",
     "https://images.unsplash.com/photo-1587314168485-3236d6710814?auto=format&fit=crop&w=600&q=80"),
    ("Jeri (Jalebi)", "Sweets", 337, 2.3, 67.5, 7.7, 0.3, "weight_gain",
     "https://images.unsplash.com/photo-1587314168485-3236d6710814?auto=format&fit=crop&w=600&q=80"),
    ("Yomari", "Traditional", 285, 5.5, 52.0, 7.5, 2.0, "maintenance",
     "https://images.unsplash.com/photo-1587314168485-3236d6710814?auto=format&fit=crop&w=600&q=80"),
    ("Bara (Black Lentil Pancake)", "Traditional", 198, 9.5, 28.5, 5.5, 3.5, "maintenance",
     "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=600&q=80"),
    ("Woh", "Traditional", 192, 9.0, 27.5, 5.8, 3.0, "maintenance",
     "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=600&q=80"),
    ("Kwati (Mixed Bean Soup)", "Traditional", 148, 9.0, 24.5, 1.5, 7.5, "weight_loss",
     "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80"),
    ("Aloo Achaar (Potato Pickle)", "Pickles", 95, 2.5, 18.5, 2.5, 2.0, "maintenance",
     "https://images.unsplash.com/photo-1518977676601-b53f02db1d2d?auto=format&fit=crop&w=600&q=80"),

    # Fruits
    ("Mango (Aap)", "Fruits", 60, 0.8, 15.0, 0.4, 1.6, "maintenance",
     "https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=600&q=80"),
    ("Banana (Kera)", "Fruits", 89, 1.1, 22.8, 0.3, 2.6, "weight_gain",
     "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=600&q=80"),
    ("Apple (Syau)", "Fruits", 52, 0.3, 13.8, 0.2, 2.4, "weight_loss",
     "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=600&q=80"),
    ("Orange (Suntala)", "Fruits", 47, 0.9, 11.8, 0.1, 2.4, "weight_loss",
     "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?auto=format&fit=crop&w=600&q=80"),
    ("Papaya (Mewa)", "Fruits", 43, 0.5, 11.0, 0.3, 1.7, "weight_loss",
     "https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=600&q=80"),
    ("Guava (Amba)", "Fruits", 68, 2.6, 14.3, 1.0, 5.4, "weight_loss",
     "https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=600&q=80"),
    ("Watermelon (Tarbuja)", "Fruits", 30, 0.6, 7.6, 0.2, 0.4, "weight_loss",
     "https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=600&q=80"),
    ("Pineapple (Bhuin Katahar)", "Fruits", 50, 0.5, 13.1, 0.1, 1.4, "weight_loss",
     "https://images.unsplash.com/photo-1550258114-28ab25db93cd?auto=format&fit=crop&w=600&q=80"),
    ("Litchi (Lichi)", "Fruits", 66, 0.8, 16.5, 0.4, 1.3, "maintenance",
     "https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=600&q=80"),
    ("Plum (Aarukhada)", "Fruits", 46, 0.7, 11.4, 0.3, 1.4, "weight_loss",
     "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?auto=format&fit=crop&w=600&q=80"),
    ("Pomegranate (Anar)", "Fruits", 83, 1.7, 18.7, 1.2, 4.0, "weight_loss",
     "https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=600&q=80"),
    ("Jackfruit (Katahar)", "Fruits", 95, 1.7, 23.2, 0.6, 1.5, "weight_gain",
     "https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=600&q=80"),
    ("Avocado", "Fruits", 160, 2.0, 9.0, 14.7, 6.7, "muscle_gain",
     "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?auto=format&fit=crop&w=600&q=80"),

    # Beverages
    ("Milk Tea (Chiya)", "Beverages", 74, 2.2, 9.8, 3.1, 0.0, "maintenance",
     "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80"),
    ("Black Tea", "Beverages", 1, 0.0, 0.2, 0.0, 0.0, "weight_loss",
     "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=600&q=80"),
    ("Lassi (Yogurt Drink)", "Beverages", 97, 4.1, 11.5, 4.2, 0.0, "maintenance",
     "https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=600&q=80"),
    ("Tongba (Millet Beer)", "Beverages", 85, 1.5, 15.5, 0.5, 0.5, "maintenance",
     "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=600&q=80"),
    ("Butter Tea (Churpi Chiya)", "Beverages", 105, 2.5, 4.5, 8.5, 0.0, "weight_gain",
     "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80"),

    # Nuts & Seeds
    ("Peanuts (Badaam)", "Nuts & Seeds", 567, 25.8, 16.1, 49.2, 8.5, "muscle_gain",
     "https://images.unsplash.com/photo-1568254183919-78a4f43a2877?auto=format&fit=crop&w=600&q=80"),
    ("Sesame Seeds (Til)", "Nuts & Seeds", 573, 17.7, 23.4, 49.7, 11.8, "muscle_gain",
     "https://images.unsplash.com/photo-1508061253366-f7da158b6cd9?auto=format&fit=crop&w=600&q=80"),
    ("Walnuts (Okhar)", "Nuts & Seeds", 654, 15.2, 13.7, 65.2, 6.7, "muscle_gain",
     "https://images.unsplash.com/photo-1508061253366-f7da158b6cd9?auto=format&fit=crop&w=600&q=80"),
    ("Almonds", "Nuts & Seeds", 579, 21.2, 21.7, 49.9, 12.5, "muscle_gain",
     "https://images.unsplash.com/photo-1508061253366-f7da158b6cd9?auto=format&fit=crop&w=600&q=80"),
    ("Flaxseeds (Alsi)", "Nuts & Seeds", 534, 18.3, 28.9, 42.2, 27.3, "weight_loss",
     "https://images.unsplash.com/photo-1508061253366-f7da158b6cd9?auto=format&fit=crop&w=600&q=80"),

    # Oils & Condiments
    ("Mustard Oil", "Oils", 884, 0.0, 0.0, 100.0, 0.0, "maintenance",
     "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=600&q=80"),
    ("Coconut Oil", "Oils", 862, 0.0, 0.0, 100.0, 0.0, "maintenance",
     "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=600&q=80"),
    ("Soybean Oil", "Oils", 884, 0.0, 0.0, 100.0, 0.0, "maintenance",
     "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=600&q=80"),

    # Additional Traditional/Popular
    ("Aloo Paratha", "Bread & Roti", 300, 7.0, 42.0, 12.5, 3.0, "maintenance",
     "https://images.unsplash.com/photo-1613564834644-a170dc930e40?auto=format&fit=crop&w=600&q=80"),
    ("Saag (Leafy Green Curry)", "Vegetables", 65, 4.5, 7.5, 2.5, 4.5, "weight_loss",
     "https://images.unsplash.com/photo-1576045057995-568f588f82fb?auto=format&fit=crop&w=600&q=80"),
    ("Biryani (Pulao)", "Rice & Grains", 290, 9.5, 45.5, 9.5, 2.0, "maintenance",
     "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=600&q=80"),
    ("Fried Rice (Bhuteko Bhat)", "Rice & Grains", 238, 7.0, 38.5, 7.5, 1.5, "maintenance",
     "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=600&q=80"),
    ("Noodle Soup (Wai Wai)", "Street Food", 330, 7.5, 47.0, 13.5, 1.5, "maintenance",
     "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80"),
    ("Fish Curry (Macha Ko Jhol)", "Fish & Seafood", 165, 18.5, 5.5, 7.5, 1.0, "weight_loss",
     "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80"),
    ("Lemon (Kagati)", "Fruits", 29, 1.1, 9.3, 0.3, 2.8, "weight_loss",
     "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?auto=format&fit=crop&w=600&q=80"),
    ("Brinjal/Eggplant (Bhanta)", "Vegetables", 25, 1.0, 5.9, 0.2, 3.0, "weight_loss",
     "https://images.unsplash.com/photo-1606787366850-de6330128bfc?auto=format&fit=crop&w=600&q=80"),
    ("Ketchup (Tomato Sauce)", "Condiments", 112, 1.4, 26.6, 0.2, 0.3, "maintenance",
     "https://images.unsplash.com/photo-1595855759920-86582396756a?auto=format&fit=crop&w=600&q=80"),
    ("Pickle (Achaar)", "Pickles", 70, 1.5, 12.5, 2.5, 2.5, "maintenance",
     "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=600&q=80"),
    ("Honey (Maaha)", "Sweets", 304, 0.3, 82.4, 0.0, 0.2, "maintenance",
     "https://images.unsplash.com/photo-1587314168485-3236d6710814?auto=format&fit=crop&w=600&q=80"),
    ("Jaggery (Gud)", "Sweets", 383, 0.4, 98.0, 0.1, 0.0, "weight_gain",
     "https://images.unsplash.com/photo-1587314168485-3236d6710814?auto=format&fit=crop&w=600&q=80"),
    ("Lapsi Candy (Hog Plum)", "Snacks", 44, 0.5, 10.9, 0.1, 1.8, "weight_loss",
     "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=600&q=80"),
    ("Popcorn", "Snacks", 375, 11.0, 74.3, 4.5, 14.5, "weight_loss",
     "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?auto=format&fit=crop&w=600&q=80"),
    ("Roasted Corn (Bilaune Makai)", "Snacks", 352, 8.0, 73.5, 4.0, 7.0, "maintenance",
     "https://images.unsplash.com/photo-1551754625-40137410b915?auto=format&fit=crop&w=600&q=80"),
    ("Saatu (Roasted Flour)", "Snacks", 388, 14.2, 70.5, 6.5, 4.5, "weight_gain",
     "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80"),
    ("Nimki (Crackers)", "Snacks", 465, 8.5, 58.5, 22.5, 2.5, "maintenance",
     "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=600&q=80"),
    ("Papad", "Snacks", 371, 19.5, 64.5, 4.5, 2.0, "maintenance",
     "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=600&q=80"),
    ("Aloo Chips", "Snacks", 536, 7.0, 53.0, 34.5, 4.5, "maintenance",
     "https://images.unsplash.com/photo-1518977676601-b53f02db1d2d?auto=format&fit=crop&w=600&q=80"),
    ("Dhakane (Sprouted Gram)", "Snacks", 133, 9.0, 22.5, 0.8, 8.5, "weight_loss",
     "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80"),
]

# Add more foods to reach 300+
EXTRA_FOODS = [
    ("Lentil Soup (Dal Jhol)", "Dal & Rice", 98, 6.5, 15.5, 1.2, 4.0, "weight_loss",
     "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80"),
    ("Mixed Vegetable Curry", "Vegetables", 85, 3.0, 12.5, 3.0, 3.5, "weight_loss",
     "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80"),
    ("Paneer Curry", "Eggs & Dairy", 290, 14.5, 7.5, 22.5, 1.0, "muscle_gain",
     "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=600&q=80"),
    ("Tofu Stir Fry", "Protein Foods", 144, 10.5, 8.5, 8.0, 2.0, "muscle_gain",
     "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80"),
    ("Black Bean Curry", "Legumes", 155, 9.5, 24.5, 3.0, 8.5, "muscle_gain",
     "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=600&q=80"),
    ("Corn Soup", "Soups", 75, 2.5, 15.5, 1.0, 1.5, "weight_loss",
     "https://images.unsplash.com/photo-1551754625-40137410b915?auto=format&fit=crop&w=600&q=80"),
    ("Tomato Soup", "Soups", 55, 1.5, 11.5, 0.8, 1.5, "weight_loss",
     "https://images.unsplash.com/photo-1595855759920-86582396756a?auto=format&fit=crop&w=600&q=80"),
    ("Vegetable Soup", "Soups", 65, 3.0, 12.5, 1.0, 3.0, "weight_loss",
     "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80"),
    ("Chicken Soup", "Soups", 75, 8.5, 5.0, 2.5, 0.5, "muscle_gain",
     "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=600&q=80"),
    ("Fried Chicken", "Meat", 265, 23.5, 8.5, 15.5, 0.5, "muscle_gain",
     "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80"),
    ("Grilled Chicken Breast", "Meat", 165, 31.0, 0.0, 3.6, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=600&q=80"),
    ("Tuna (Canned)", "Fish & Seafood", 116, 26.0, 0.0, 1.0, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80"),
    ("Salmon Fillet", "Fish & Seafood", 208, 20.0, 0.0, 13.4, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80"),
    ("Greek Yogurt", "Eggs & Dairy", 59, 10.0, 3.6, 0.4, 0.0, "muscle_gain",
     "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=600&q=80"),
    ("Low Fat Milk", "Eggs & Dairy", 35, 3.4, 4.8, 0.2, 0.0, "weight_loss",
     "https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=600&q=80"),
    ("Whole Wheat Bread", "Bread & Roti", 247, 13.0, 41.0, 3.4, 7.0, "weight_loss",
     "https://images.unsplash.com/photo-1613564834644-a170dc930e40?auto=format&fit=crop&w=600&q=80"),
    ("White Bread", "Bread & Roti", 265, 9.0, 49.0, 3.2, 2.7, "maintenance",
     "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80"),
    ("Pasta (Macaroni)", "Rice & Grains", 371, 13.0, 74.7, 1.5, 3.2, "maintenance",
     "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80"),
    ("Pizza (Slice)", "Street Food", 266, 11.0, 33.0, 10.4, 2.3, "maintenance",
     "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80"),
    ("Burger", "Street Food", 295, 17.0, 24.0, 14.0, 1.5, "maintenance",
     "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80"),
    ("French Fries", "Street Food", 312, 3.4, 41.4, 15.0, 3.8, "maintenance",
     "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=600&q=80"),
    ("Sandwich", "Street Food", 250, 10.5, 33.5, 8.5, 3.0, "maintenance",
     "https://images.unsplash.com/photo-1613564834644-a170dc930e40?auto=format&fit=crop&w=600&q=80"),
    ("Idli", "Traditional", 58, 2.7, 11.8, 0.4, 0.5, "weight_loss",
     "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=600&q=80"),
    ("Dosa", "Traditional", 165, 4.5, 30.0, 3.5, 1.2, "maintenance",
     "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=600&q=80"),
    ("Upma", "Traditional", 150, 4.0, 28.0, 3.5, 2.0, "weight_loss",
     "https://images.unsplash.com/photo-1541832676-9b763b0239ab?auto=format&fit=crop&w=600&q=80"),
    ("Poha (Flattened Rice)", "Traditional", 250, 4.0, 47.5, 6.0, 1.5, "maintenance",
     "https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=600&q=80"),
    ("Cereal (Corn Flakes)", "Breakfast Foods", 357, 7.5, 84.0, 0.9, 1.2, "maintenance",
     "https://images.unsplash.com/photo-1551754625-40137410b915?auto=format&fit=crop&w=600&q=80"),
    ("Muesli", "Breakfast Foods", 370, 11.5, 65.0, 8.5, 7.5, "weight_loss",
     "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?auto=format&fit=crop&w=600&q=80"),
    ("Granola", "Breakfast Foods", 471, 10.0, 64.0, 20.0, 6.5, "weight_gain",
     "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?auto=format&fit=crop&w=600&q=80"),
    ("Protein Bar", "Supplements", 370, 25.0, 48.0, 8.5, 5.0, "muscle_gain",
     "https://images.unsplash.com/photo-1508061253366-f7da158b6cd9?auto=format&fit=crop&w=600&q=80"),
    ("Protein Shake", "Supplements", 200, 30.0, 10.0, 3.5, 1.5, "muscle_gain",
     "https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=600&q=80"),
    ("Energy Drink", "Beverages", 112, 1.0, 28.0, 0.0, 0.0, "maintenance",
     "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=600&q=80"),
    ("Orange Juice", "Beverages", 45, 0.7, 10.4, 0.2, 0.2, "weight_loss",
     "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?auto=format&fit=crop&w=600&q=80"),
    ("Coconut Water", "Beverages", 19, 0.7, 3.7, 0.2, 1.1, "weight_loss",
     "https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=600&q=80"),
    ("Sugarcane Juice (Ukhoo Ras)", "Beverages", 78, 0.3, 19.5, 0.1, 0.0, "maintenance",
     "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=600&q=80"),
    ("Coffee (Black)", "Beverages", 1, 0.3, 0.0, 0.0, 0.0, "weight_loss",
     "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=600&q=80"),
    ("Lemon Water", "Beverages", 11, 0.1, 3.5, 0.0, 0.1, "weight_loss",
     "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?auto=format&fit=crop&w=600&q=80"),
    ("Strawberry", "Fruits", 32, 0.7, 7.7, 0.3, 2.0, "weight_loss",
     "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=600&q=80"),
    ("Grapes (Angur)", "Fruits", 67, 0.6, 17.2, 0.4, 0.9, "maintenance",
     "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?auto=format&fit=crop&w=600&q=80"),
    ("Kiwi", "Fruits", 61, 1.1, 14.7, 0.5, 3.0, "weight_loss",
     "https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=600&q=80"),
    ("Pear (Naspati)", "Fruits", 57, 0.4, 15.2, 0.1, 3.1, "weight_loss",
     "https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=600&q=80"),
    ("Fig (Anjir)", "Fruits", 74, 0.75, 19.2, 0.3, 2.9, "maintenance",
     "https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=600&q=80"),
    ("Dates (Khurmah)", "Fruits", 277, 1.8, 74.97, 0.2, 6.7, "weight_gain",
     "https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=600&q=80"),
    ("Raisins (Kismis)", "Fruits", 299, 3.1, 79.2, 0.5, 3.7, "weight_gain",
     "https://images.unsplash.com/photo-1508061253366-f7da158b6cd9?auto=format&fit=crop&w=600&q=80"),
    ("Asparagus", "Vegetables", 20, 2.2, 3.7, 0.1, 2.1, "weight_loss",
     "https://images.unsplash.com/photo-1453133451515-5ff7c1d0d63c?auto=format&fit=crop&w=600&q=80"),
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
