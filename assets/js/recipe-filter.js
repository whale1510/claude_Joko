/**
 * Recipe Filter System
 * Filters recipes by category, ingredients, and dietary preferences
 */

(function() {
  'use strict';

  // State
  let allRecipes = [];
  let activeFilters = {
    category: new Set(),
    dietary: new Set()
  };

  // DOM Elements
  let filterForm;
  let filteredResultsSection;
  let filteredResultsGrid;
  let resultCountSpan;
  let resetButton;
  let activeFiltersCountSpan;
  let originalRecipeSections;

  /**
   * Initialize the filter system
   */
  function init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', setup);
    } else {
      setup();
    }
  }

  /**
   * Set up the filter system
   */
  function setup() {
    // Get DOM elements
    filterForm = document.getElementById('recipe-filter-form');
    filteredResultsSection = document.getElementById('filtered-results-section');
    filteredResultsGrid = document.getElementById('filtered-results-grid');
    resultCountSpan = document.getElementById('result-count');
    resetButton = document.getElementById('reset-filters');
    activeFiltersCountSpan = document.getElementById('active-filters-count');

    // Store original recipe sections for hiding/showing
    originalRecipeSections = document.querySelectorAll('#main-dish-recipes, #side-dish-recipes, #rice-recipes, #featured-recipes-section');

    // Collect recipe data
    collectRecipeData();

    // Set up event listeners
    setupEventListeners();

    // Initial state
    updateActiveFiltersCount();
  }

  /**
   * Collect all recipe data from the page
   */
  function collectRecipeData() {
    const recipeCards = document.querySelectorAll('.recipe-card[data-category]');

    allRecipes = Array.from(recipeCards).map(card => {
      return {
        element: card.cloneNode(true), // Clone the entire card
        category: card.dataset.category || '',
        ingredients: (card.dataset.ingredients || '').split(',').filter(i => i.trim()),
        dietary: (card.dataset.dietary || '').split(',').filter(d => d.trim())
      };
    });

    console.log(`Collected ${allRecipes.length} recipes`);
  }


  /**
   * Set up event listeners
   */
  function setupEventListeners() {
    // Listen for filter changes
    if (filterForm) {
      filterForm.addEventListener('change', handleFilterChange);
    }

    // Reset button
    if (resetButton) {
      resetButton.addEventListener('click', resetFilters);
    }
  }

  /**
   * Handle filter checkbox changes
   */
  function handleFilterChange(event) {
    const input = event.target;

    if (input.type !== 'checkbox') return;

    const filterType = input.name; // 'category' or 'dietary'
    const value = input.value;

    if (input.checked) {
      activeFilters[filterType].add(value);
    } else {
      activeFilters[filterType].delete(value);
    }

    applyFilters();
    updateActiveFiltersCount();
  }

  /**
   * Apply active filters and display results
   */
  function applyFilters() {
    // Check if any filters are active
    const hasActiveFilters =
      activeFilters.category.size > 0 ||
      activeFilters.dietary.size > 0;

    if (!hasActiveFilters) {
      // No filters active - hide filtered results, show original sections
      hideFilteredResults();
      return;
    }

    // Filter recipes
    const filteredRecipes = allRecipes.filter(recipe => {
      // Category filter (OR logic - match any selected category)
      const categoryMatch = activeFilters.category.size === 0 ||
        activeFilters.category.has(recipe.category);

      // Dietary filter (AND logic - must match all selected dietary types)
      const dietaryMatch = activeFilters.dietary.size === 0 ||
        Array.from(activeFilters.dietary).every(dietary =>
          recipe.dietary.includes(dietary)
        );

      return categoryMatch && dietaryMatch;
    });

    displayFilteredResults(filteredRecipes);
  }

  /**
   * Display filtered results
   */
  function displayFilteredResults(filteredRecipes) {
    // Hide original recipe sections
    originalRecipeSections.forEach(section => {
      section.style.display = 'none';
    });

    // Clear previous results
    filteredResultsGrid.innerHTML = '';

    // Add filtered recipes
    filteredRecipes.forEach(recipe => {
      filteredResultsGrid.appendChild(recipe.element);
    });

    // Update count
    resultCountSpan.textContent = filteredRecipes.length;

    // Show filtered results section
    filteredResultsSection.style.display = 'block';

    // Scroll to results
    filteredResultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  /**
   * Hide filtered results and show original sections
   */
  function hideFilteredResults() {
    filteredResultsSection.style.display = 'none';

    // Show original recipe sections
    originalRecipeSections.forEach(section => {
      section.style.display = 'block';
    });
  }

  /**
   * Reset all filters
   */
  function resetFilters() {
    // Clear active filters
    activeFilters.category.clear();
    activeFilters.dietary.clear();

    // Uncheck all checkboxes
    const checkboxes = filterForm.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
      checkbox.checked = false;
    });

    // Hide filtered results
    hideFilteredResults();

    // Update count
    updateActiveFiltersCount();

    // Scroll to filter section
    const filterHeading = document.getElementById('filter-heading');
    if (filterHeading) {
      filterHeading.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  /**
   * Update active filters count display
   */
  function updateActiveFiltersCount() {
    const totalActive =
      activeFilters.category.size +
      activeFilters.dietary.size;

    if (activeFiltersCountSpan) {
      if (totalActive === 0) {
        activeFiltersCountSpan.textContent = '';
      } else {
        activeFiltersCountSpan.textContent = `${totalActive} filter(s) active`;
      }
    }
  }

  // Initialize on load
  init();

})();
