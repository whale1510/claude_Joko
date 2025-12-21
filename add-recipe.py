#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Recipe Adder for Joko's Jang-Namul-Bap
Usage: python add-recipe.py
"""

import os
import re
import shutil
from datetime import datetime

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def get_input(prompt, default=None):
    """Get user input with optional default"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def get_multiselect(prompt, options):
    """Get multiple selections from user"""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print("Enter numbers separated by commas (e.g., 1,3,5) or press Enter to skip:")

    selections = input("> ").strip()
    if not selections:
        return []

    selected_indices = [int(x.strip()) - 1 for x in selections.split(',') if x.strip().isdigit()]
    return [options[i] for i in selected_indices if 0 <= i < len(options)]

def backup_file(filepath):
    """Create backup of a file"""
    if not os.path.exists(filepath):
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.backup_{timestamp}"
    shutil.copy2(filepath, backup_path)
    return backup_path

def create_recipe_page(recipe_info):
    """Generate recipe detail page HTML"""
    template = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{recipe_info['name']} | Joko's Jang-Namul-Bap</title>
    <link rel="stylesheet" href="../../assets/css/style.css" />
    <script src="../../assets/js/includes.js" defer></script>
  </head>
  <body data-root-path="../..">
    <div data-include="../../partials/header.html" data-root-path="../.."></div>
    <main id="main-content">
      <article class="recipe-detail" aria-labelledby="{recipe_info['slug']}-heading">
        <div class="recipe-detail-grid">
          <header class="recipe-overview">
            <span class="category-tag">{recipe_info['category_display']}</span>
            <h1 class="section-title" id="{recipe_info['slug']}-heading">{recipe_info['name']}</h1>
            <img
              src="../../assets/img/recipes/{recipe_info['image']}"
              alt="{recipe_info['name']}"
              class="recipe-hero-image"
            />
            <div class="recipe-metadata">
              <span>⏱ {recipe_info['time']}</span>
              <span>🥄 Serves {recipe_info['servings']}</span>
            </div>
            <p>{recipe_info['description']}</p>
          </header>
          <aside class="recipe-visual" aria-label="{recipe_info['name']} tips">
            <span class="recipe-visual__label">Cooking Tips</span>
            <p>Tips for making delicious {recipe_info['name']}.</p>
            <ul>
              <li>Use fresh ingredients for the best flavor.</li>
              <li>Adjust seasoning to your taste preference.</li>
              <li>Serve immediately for optimal taste and texture.</li>
            </ul>
          </aside>
        </div>

        <section class="recipe-content-grid section" aria-labelledby="{recipe_info['slug']}-ingredients">
          <section class="recipe-section">
            <h2 id="{recipe_info['slug']}-ingredients">Ingredients</h2>
            <ul>
              <li>Add your ingredients here</li>
            </ul>
          </section>
          <aside class="aside-panel" aria-labelledby="{recipe_info['slug']}-substitution">
            <h2 id="{recipe_info['slug']}-substitution">Substitution Tips</h2>
            <ul>
              <li>Check the Vegan & Halal Guide for ingredient substitutions.</li>
            </ul>
          </aside>
        </section>

        <section class="recipe-steps section" aria-labelledby="{recipe_info['slug']}-steps">
          <h2 id="{recipe_info['slug']}-steps">Instructions</h2>
          <ol>
            <li>Add your cooking steps here.</li>
          </ol>
        </section>
      </article>
    </main>
    <div data-include="../../partials/footer.html" data-root-path="../.."></div>
  </body>
</html>
"""
    return template

def create_recipe_card(recipe_info, for_index=False):
    """Generate recipe card HTML"""
    img_path = f"assets/img/recipes/{recipe_info['image']}" if for_index else f"../assets/img/recipes/{recipe_info['image']}"
    link_path = f"recipes/{recipe_info['category']}/{recipe_info['slug']}.html" if for_index else f"{recipe_info['category']}/{recipe_info['slug']}.html"

    card = f"""          <article class="card recipe-card"
                   data-category="{recipe_info['category']}"
                   data-ingredients="{recipe_info['ingredients']}"
                   data-dietary="{recipe_info['dietary']}">
            <img src="{img_path}" alt="{recipe_info['name']}" class="recipe-card-image" />
            <div class="recipe-card-content">
              <span class="category-tag">{recipe_info['category_display']}</span>
              <h3><a href="{link_path}">{recipe_info['name']}</a></h3>
              <p>{recipe_info['description']}</p>
              <div class="recipe-metadata">
                <span>⏱ {recipe_info['total_time']}</span>
                <span>🥄 Serves {recipe_info['servings']}</span>
              </div>
            </div>
          </article>
"""
    return card

def insert_card_to_file(filepath, card_html, section_id):
    """Insert recipe card into HTML file"""
    try:
        # Backup first
        backup_path = backup_file(filepath)
        if backup_path:
            print(f"  📦 Backup created: {backup_path}")

        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find insertion point
        # Look for the recipe-card-grid div within the section
        section_pattern = rf'<section[^>]*id="{section_id}"[^>]*>(.*?)</section>'
        section_match = re.search(section_pattern, content, re.DOTALL)

        if not section_match:
            print(f"  ❌ Could not find section #{section_id}")
            return False

        section_content = section_match.group(1)

        # Find the last </article> before </div> in recipe-card-grid
        grid_pattern = r'<div class="recipe-card-grid">(.*?)</div>'
        grid_match = re.search(grid_pattern, section_content, re.DOTALL)

        if not grid_match:
            print(f"  ❌ Could not find recipe-card-grid in section #{section_id}")
            return False

        grid_content = grid_match.group(1)

        # Find the last </article> in the grid
        last_article_pos = grid_content.rfind('</article>')

        if last_article_pos == -1:
            # No articles yet, insert at the beginning
            insertion_point = content.find('<div class="recipe-card-grid">', section_match.start()) + len('<div class="recipe-card-grid">')
            new_content = content[:insertion_point] + '\n' + card_html + content[insertion_point:]
        else:
            # Insert after the last </article>
            absolute_pos = content.find(grid_content, section_match.start()) + last_article_pos + len('</article>')
            new_content = content[:absolute_pos] + '\n' + card_html + content[absolute_pos:]

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        # Restore from backup if exists
        if backup_path and os.path.exists(backup_path):
            shutil.copy2(backup_path, filepath)
            print(f"  🔄 Restored from backup")
        return False

def main():
    print("=" * 60)
    print("  🍜 Quick Recipe Adder for Joko's Jang-Namul-Bap")
    print("=" * 60)
    print()

    # Get recipe basic info
    name = get_input("Recipe name (e.g., 'Kimchi Jjigae')")
    if not name:
        print("❌ Recipe name is required!")
        return

    slug = slugify(name)

    # Category
    print("\nSelect category:")
    print("  1. Main Dish")
    print("  2. Side Dish")
    print("  3. Rice")
    category_choice = get_input("Enter number", "1")

    category_map = {
        "1": ("main-dish", "Main Dish"),
        "2": ("side-dish", "Side Dish"),
        "3": ("rice", "Rice")
    }
    category, category_display = category_map.get(category_choice, ("main-dish", "Main Dish"))

    # Description
    description = get_input("Short description", f"Delicious Korean {name}")

    # Time
    prep_time = get_input("Prep time (minutes)", "10")
    cook_time = get_input("Cook time (minutes)", "20")
    total_minutes = int(prep_time) + int(cook_time)
    time = f"Prep {prep_time} min + Cook {cook_time} min"
    total_time = f"{total_minutes} min"

    # Servings
    servings = get_input("Servings", "2")

    # Image
    image = get_input("Image filename (in assets/img/recipes/)", f"{slug}.jpg")

    # Ingredients
    print("\nEnter main ingredients (comma-separated, e.g., 'kimchi,pork,tofu')")
    ingredients = get_input("Ingredients", "kimchi,tofu,garlic").lower()

    # Dietary options
    dietary_options = [
        "vegan",
        "halal",
        "gluten-free",
        "nut-free",
        "dairy-free",
        "shellfish-free"
    ]
    selected_dietary = get_multiselect("Select dietary types (if applicable):", dietary_options)
    dietary = ",".join(selected_dietary) if selected_dietary else "gluten-free,dairy-free,shellfish-free"

    # Compile recipe info
    recipe_info = {
        "name": name,
        "slug": slug,
        "category": category,
        "category_display": category_display,
        "description": description,
        "time": time,
        "total_time": total_time,
        "servings": servings,
        "image": image,
        "ingredients": ingredients,
        "dietary": dietary
    }

    print("\n" + "=" * 60)
    print("📝 Recipe Summary:")
    print("=" * 60)
    for key, value in recipe_info.items():
        print(f"  {key:20s}: {value}")
    print("=" * 60)

    confirm = get_input("\nCreate this recipe? (y/n)", "y")
    if confirm.lower() != 'y':
        print("❌ Cancelled.")
        return

    print("\n" + "=" * 60)
    print("🚀 Creating recipe...")
    print("=" * 60)

    # Create recipe detail page
    recipe_page = create_recipe_page(recipe_info)
    recipe_path = f"recipes/{category}/{slug}.html"

    os.makedirs(os.path.dirname(recipe_path), exist_ok=True)
    with open(recipe_path, 'w', encoding='utf-8') as f:
        f.write(recipe_page)
    print(f"\n✅ Created recipe page: {recipe_path}")

    # Generate recipe cards
    card_for_index = create_recipe_card(recipe_info, for_index=True)
    card_for_recipes = create_recipe_card(recipe_info, for_index=False)

    # Auto-insert into index.html
    print("\n📝 Adding to index.html...")
    if insert_card_to_file("index.html", card_for_index, "featured-recipes-section"):
        print("  ✅ Successfully added to index.html")
    else:
        print("  ❌ Failed to add to index.html (manual insertion needed)")
        print("\n  Copy this code to index.html (#featured-recipes-section):")
        print("  " + "-" * 56)
        print(card_for_index)

    # Auto-insert into recipes/index.html
    section_id_map = {
        "main-dish": "main-dish-recipes",
        "side-dish": "side-dish-recipes",
        "rice": "rice-recipes"
    }
    section_id = section_id_map[category]

    print("\n📝 Adding to recipes/index.html...")
    if insert_card_to_file("recipes/index.html", card_for_recipes, section_id):
        print(f"  ✅ Successfully added to recipes/index.html (#{section_id})")
    else:
        print(f"  ❌ Failed to add to recipes/index.html (manual insertion needed)")
        print(f"\n  Copy this code to recipes/index.html (#{section_id}):")
        print("  " + "-" * 56)
        print(card_for_recipes)

    print("\n" + "=" * 60)
    print("📋 NEXT STEPS:")
    print("=" * 60)
    print(f"\n1. ✅ Recipe page created: {recipe_path}")
    print(f"\n2. 📝 Edit recipe details in: {recipe_path}")
    print(f"   - Add detailed ingredients list")
    print(f"   - Add cooking instructions")
    print(f"   - Update cooking tips")
    print(f"\n3. 🖼️  Make sure image exists: assets/img/recipes/{image}")
    print(f"\n4. 🧪 Test with: python -m http.server 8000")
    print(f"   - Visit: http://localhost:8000")
    print(f"   - Check: http://localhost:8000/recipes/{category}/{slug}.html")

    print("\n✨ Done! Your recipe has been added to the site.")
    print("\n💡 Tip: Backup files are saved with .backup_TIMESTAMP extension")
    print("   You can safely delete them after confirming everything works.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
