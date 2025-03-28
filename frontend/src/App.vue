<template>
  <div id="app" class="flex flex-col min-h-screen font-sans antialiased overflow-x-hidden" :class="isDarkMode ? 'bg-gray-900 text-gray-100' : 'bg-gradient-to-br from-gray-50 to-gray-200 text-gray-900'">
    <!-- Notification -->
    <transition name="fade">
      <div v-if="notification" class="fixed top-4 right-4 z-50 p-4 rounded-xl shadow-xl text-white font-medium flex items-center space-x-3" :class="notification.type === 'success' ? 'bg-gradient-to-r from-green-500 to-teal-500' : 'bg-gradient-to-r from-red-500 to-pink-500'">
        <span>{{ notification.message }}</span>
        <button @click="clearNotification" class="text-white hover:text-gray-200">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </transition>

    <!-- Loading Screen -->
    <transition name="fade">
      <div v-if="isLoading" class="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600">
        <div class="text-center relative">
          <div class="w-24 h-24 border-6 border-t-6 border-white border-opacity-30 rounded-full animate-spin mb-6"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <svg class="w-16 h-16 text-white animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <p class="text-3xl font-extrabold text-white animate-pulse tracking-wider">TechHub</p>
          <p class="text-base text-white opacity-80 mt-2">Загружаем будущее...</p>
          <div class="w-56 h-1.5 bg-white bg-opacity-20 rounded-full mt-4 overflow-hidden">
            <div class="h-full bg-gradient-to-r from-indigo-400 to-purple-400 animate-progress" :style="{ width: `${loadingProgress}%` }"></div>
          </div>
          <div class="absolute inset-0 pointer-events-none overflow-hidden">
            <div v-for="i in 20" :key="i" class="particle" :style="particleStyle()"></div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Header -->
    <header class="fixed w-full top-0 z-40 shadow-lg" :class="isDarkMode ? 'bg-gray-800 border-b border-gray-700' : 'bg-white border-b border-gray-200'">
      <div class="container mx-auto flex justify-between items-center py-3 px-4 sm:px-6">
        <div class="flex items-center space-x-3 cursor-pointer" @click="$router.push('/')">
          <svg class="w-10 h-10 text-indigo-600 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
          <h1 class="text-2xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">TechHub</h1>
        </div>
        <div class="flex items-center space-x-4 sm:space-x-6">
          <div class="relative w-64 sm:w-80 hidden sm:block">
            <input
              v-model="searchQuery"
              @input="debouncedSearch"
              type="text"
              class="w-full p-2.5 pl-10 border rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all duration-300 shadow-sm"
              :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100 placeholder-gray-400' : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'"
              placeholder="Поиск товаров..."
            >
            <svg class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <ul v-if="searchSuggestions.length" class="absolute w-full border rounded-xl shadow-lg mt-1 max-h-56 overflow-y-auto z-50" :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'">
              <li v-for="suggestion in searchSuggestions" :key="suggestion.id" @click="selectSuggestion(suggestion)" class="p-2.5 hover:bg-gradient-to-r hover:from-indigo-600 hover:to-purple-600 hover:text-white cursor-pointer transition-all duration-200" :class="isDarkMode ? 'text-gray-100' : 'text-gray-700'">
                {{ suggestion.name }}
              </li>
            </ul>
          </div>
          <button @click="toggleSidebar" class="hover:text-indigo-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
            <svg class="w-6 h-6 sm:w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="showSidebar ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16m-7 6h7'"></path>
            </svg>
          </button>
          <button @click="toggleCompare" class="relative hover:text-indigo-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
            <svg class="w-6 h-6 sm:w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h18M3 12h18M3 20h18"></path>
            </svg>
            <span v-if="compareList.length" class="absolute -top-1 -right-1 bg-gradient-to-r from-indigo-500 to-purple-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center shadow-sm">{{ compareList.length }}</span>
          </button>
          <button @click="toggleCart" ref="cartButton" class="relative hover:text-indigo-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
            <svg class="w-6 h-6 sm:w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <span v-if="cartCount > 0" class="absolute -top-1 -right-1 bg-gradient-to-r from-indigo-500 to-purple-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center shadow-sm">{{ cartCount }}</span>
          </button>
          <button @click="toggleOrderHistory" class="hover:text-indigo-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
            <svg class="w-6 h-6 sm:w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </button>
          <button @click="toggleFavorites" class="hover:text-red-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
            <svg class="w-6 h-6 sm:w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
            </svg>
            <span v-if="favorites.length" class="absolute -top-1 -right-1 bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center shadow-sm">{{ favorites.length }}</span>
          </button>
          <button @click="toggleDarkMode" class="hover:text-indigo-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
            <svg class="w-6 h-6 sm:w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="isDarkMode ? 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z' : 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z'"></path>
            </svg>
          </button>
        </div>
      </div>
      <!-- Mobile Search Bar -->
      <div class="block sm:hidden px-4 pb-3">
        <div class="relative w-full">
          <input
            v-model="searchQuery"
            @input="debouncedSearch"
            type="text"
            class="w-full p-2.5 pl-10 border rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all duration-300 shadow-sm"
            :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100 placeholder-gray-400' : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'"
            placeholder="Поиск товаров..."
          >
          <svg class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <ul v-if="searchSuggestions.length" class="absolute w-full border rounded-xl shadow-lg mt-1 max-h-56 overflow-y-auto z-50" :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'">
            <li v-for="suggestion in searchSuggestions" :key="suggestion.id" @click="selectSuggestion(suggestion)" class="p-2.5 hover:bg-gradient-to-r hover:from-indigo-600 hover:to-purple-600 hover:text-white cursor-pointer transition-all duration-200" :class="isDarkMode ? 'text-gray-100' : 'text-gray-700'">
              {{ suggestion.name }}
            </li>
          </ul>
        </div>
      </div>
    </header>

    <!-- Main Layout -->
    <div class="flex flex-grow pt-16 sm:pt-20">
      <!-- Sidebar (Filters & Categories) -->
      <transition name="slide">
        <aside v-if="showSidebar" class="w-72 sm:w-80 fixed h-full z-40 p-6 sm:p-8 top-16 sm:top-20 transform transition-transform duration-500 shadow-lg rounded-r-2xl" :class="isDarkMode ? 'bg-gray-800 border-r border-gray-700' : 'bg-white border-r border-gray-200'">
          <div class="flex justify-between items-center mb-8">
            <h2 class="text-xl sm:text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">Фильтры</h2>
            <button @click="toggleSidebar" class="hover:text-indigo-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div class="space-y-8">
            <!-- Categories -->
            <div>
              <h3 class="text-lg font-semibold mb-3" :class="isDarkMode ? 'text-gray-200' : 'text-gray-700'">Категории</h3>
              <ul class="space-y-2">
                <li>
                  <button
                    @click="selectCategory(null)"
                    class="w-full text-left py-2.5 px-4 rounded-lg hover:bg-gradient-to-r hover:from-indigo-600 hover:to-purple-600 hover:text-white transition-all duration-300 flex items-center shadow-sm"
                    :class="isDarkMode ? (!selectedCategory ? 'bg-gradient-to-r from-indigo-700 to-purple-700 text-white' : 'bg-gray-700 text-gray-200') : (!selectedCategory ? 'bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700' : 'bg-white text-gray-700')"
                  >
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                    </svg>
                    Все товары
                  </button>
                </li>
                <li v-for="category in categories" :key="category.id">
                  <button
                    @click="selectCategory(category.id)"
                    class="w-full text-left py-2.5 px-4 rounded-lg hover:bg-gradient-to-r hover:from-indigo-600 hover:to-purple-600 hover:text-white transition-all duration-300 flex items-center shadow-sm"
                    :class="isDarkMode ? (selectedCategory === category.id ? 'bg-gradient-to-r from-indigo-700 to-purple-700 text-white' : 'bg-gray-700 text-gray-200') : (selectedCategory === category.id ? 'bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700' : 'bg-white text-gray-700')"
                  >
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                    </svg>
                    {{ category.name }}
                  </button>
                </li>
              </ul>
            </div>
            <!-- Brands -->
            <div>
              <h3 class="text-lg font-semibold mb-3" :class="isDarkMode ? 'text-gray-200' : 'text-gray-700'">Бренды</h3>
              <ul class="space-y-2">
                <li v-for="brand in brands" :key="brand">
                  <label class="flex items-center space-x-2">
                    <input type="checkbox" v-model="selectedBrands" :value="brand" class="w-4 h-4 accent-indigo-600 rounded">
                    <span class="text-sm font-medium" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">{{ brand }}</span>
                  </label>
                </li>
              </ul>
            </div>
            <!-- Filters -->
            <div>
              <h3 class="text-lg font-semibold mb-3" :class="isDarkMode ? 'text-gray-200' : 'text-gray-700'">Параметры</h3>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Цена</label>
                  <input type="range" v-model="priceFilter" min="0" max="5000" step="50" class="w-full h-1.5 rounded-full accent-indigo-600 cursor-pointer shadow-inner" :class="isDarkMode ? 'bg-gray-600' : 'bg-gray-200'">
                  <span class="text-sm mt-1 block" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">До ${{ priceFilter }}</span>
                </div>
                <div>
                  <label class="flex items-center space-x-2">
                    <input type="checkbox" v-model="inStockOnly" class="w-4 h-4 accent-indigo-600 rounded">
                    <span class="text-sm font-medium" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Только в наличии</span>
                  </label>
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Сортировка</label>
                  <select v-model="sortOption" class="w-full p-2.5 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all duration-300 shadow-sm" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-700'">
                    <option value="price-asc">Цена: по возрастанию</option>
                    <option value="price-desc">Цена: по убыванию</option>
                    <option value="name">По названию</option>
                    <option value="newest">Новинки</option>
                    <option value="rating">По рейтингу</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </transition>

      <!-- Main Content -->
      <main class="flex-grow container mx-auto py-10 px-4 sm:px-6 transition-all duration-500" :class="{ 'md:ml-80': showSidebar }">
        <h2 class="text-4xl sm:text-5xl font-extrabold mb-10 text-center tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">TechHub: Ваш выбор технологий</h2>
        <ProductList
          :cart="cart"
          :compare-list="compareList"
          :favorites="favorites"
          @add-to-cart="addToCart"
          @toggle-compare="toggleCompareItem"
          @toggle-favorite="toggleFavorite"
          :selected-category="selectedCategory"
          :selected-brands="selectedBrands"
          :price-filter="priceFilter"
          :in-stock-only="inStockOnly"
          :sort-option="sortOption"
          :search-query="searchQuery"
          :current-page="currentPage"
          @update-page="updatePage"
          :is-dark-mode="isDarkMode"
        />
        <!-- Pagination -->
        <div class="flex justify-center mt-10 space-x-4">
          <button @click="prevPage" :disabled="currentPage === 1" class="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 disabled:bg-gray-400 shadow-sm">Назад</button>
          <span class="text-base sm:text-lg font-medium" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Страница {{ currentPage }} из {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages" class="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 disabled:bg-gray-400 shadow-sm">Вперёд</button>
        </div>
      </main>
    </div>

    <!-- Cart Modal -->
    <transition name="fade">
      <div v-if="showCart" class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50" @click.self="toggleCart">
        <div class="rounded-2xl p-6 w-full max-w-md sm:max-w-lg shadow-2xl" :class="isDarkMode ? 'bg-gray-800' : 'bg-white'">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-xl sm:text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">Корзина</h3>
            <button @click="toggleCart" class="hover:text-indigo-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div v-if="cart.length === 0" class="text-center py-6" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Корзина пуста</div>
          <div v-else>
            <ul class="space-y-3 max-h-64 overflow-y-auto mb-6">
              <li v-for="item in cart.filter(item => item && item.id)" :key="item.id" class="flex justify-between items-center p-3 rounded-lg shadow-sm transition-all duration-300 hover:shadow-md" :class="isDarkMode ? 'bg-gray-700' : 'bg-gray-50'">
                <div class="flex items-center space-x-3">
                  <img :src="getImageUrl(item.image)" alt="Product" class="w-12 h-12 object-cover rounded-md" @error="handleImageError">
                  <div>
                    <span class="text-sm font-semibold" :class="isDarkMode ? 'text-gray-100' : 'text-gray-800'">{{ item.name }}</span>
                    <div class="flex items-center space-x-1 mt-1">
                      <button @click="decreaseQuantity(item)" class="px-1.5 py-0.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded hover:from-indigo-700 hover:to-purple-700">-</button>
                      <span class="text-xs" :class="isDarkMode ? 'text-gray-300' : 'text-gray-500'">{{ item.quantity || 1 }}</span>
                      <button @click="increaseQuantity(item)" class="px-1.5 py-0.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded hover:from-indigo-700 hover:to-purple-700">+</button>
                    </div>
                  </div>
                </div>
                <div class="flex items-center space-x-3">
                  <span class="text-indigo-600 font-bold text-sm">${{ (item.price * (item.quantity || 1)).toFixed(2) }}</span>
                  <button @click="removeFromCart(item.id)" class="text-red-500 hover:text-red-700 transition-colors duration-300 text-sm">Удалить</button>
                </div>
              </li>
            </ul>
            <div class="flex justify-between items-center mb-6">
              <p class="text-lg font-semibold" :class="isDarkMode ? 'text-gray-100' : 'text-gray-800'">Итого: ${{ cartTotal }}</p>
              <button @click="clearCart" class="text-sm text-red-500 hover:text-red-700 transition-colors duration-300 font-medium">Очистить корзину</button>
            </div>
            <div class="space-y-3">
              <input v-model="order.name" type="text" class="w-full p-2.5 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all duration-300 shadow-sm" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-700'" placeholder="Ваше имя">
              <input v-model="order.address" type="text" class="w-full p-2.5 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all duration-300 shadow-sm" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-700'" placeholder="Адрес доставки">
              <select v-model="order.delivery" class="w-full p-2.5 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all duration-300 shadow-sm" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-700'">
                <option value="standard">Стандарт ($5)</option>
                <option value="express">Экспресс ($15)</option>
                <option value="pickup">Самовывоз</option>
              </select>
              <textarea v-model="order.comment" class="w-full p-2.5 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all duration-300 shadow-sm" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-700'" placeholder="Комментарий к заказу" rows="2"></textarea>
              <button @click="submitOrder" class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-2.5 rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 font-semibold shadow-sm">Оформить заказ</button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Compare Modal -->
    <transition name="fade">
      <div v-if="showCompare" class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50" @click.self="toggleCompare">
        <div class="rounded-2xl p-6 w-full max-w-5xl shadow-2xl" :class="isDarkMode ? 'bg-gray-800' : 'bg-white'">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-xl sm:text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">Сравнение товаров</h3>
            <button @click="toggleCompare" class="hover:text-indigo-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div v-if="compareList.length === 0" class="text-center py-6" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Нет товаров для сравнения</div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <div v-for="item in compareList.filter(item => item && item.id)" :key="item.id" class="border p-4 rounded-lg shadow-sm transition-all duration-300 hover:shadow-md" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'">
              <img :src="getImageUrl(item.image)" alt="Product" class="w-full h-40 object-cover rounded-md mb-3" @error="handleImageError">
              <h4 class="text-sm font-semibold mb-2" :class="isDarkMode ? 'text-gray-100' : 'text-gray-800'">{{ item.name }}</h4>
              <p class="text-indigo-600 font-bold mb-2 text-sm">${{ item.price }}</p>
              <p class="text-xs line-clamp-3 mb-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">{{ item.description }}</p>
              <button @click="toggleCompareItem(item)" class="text-red-500 hover:text-red-700 transition-colors duration-300 text-xs font-medium">Убрать</button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Favorites Modal -->
    <transition name="fade">
      <div v-if="showFavorites" class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50" @click.self="toggleFavorites">
        <div class="rounded-2xl p-6 w-full max-w-5xl shadow-2xl" :class="isDarkMode ? 'bg-gray-800' : 'bg-white'">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-xl sm:text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-pink-500">Избранное</h3>
            <button @click="toggleFavorites" class="hover:text-red-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div v-if="favorites.length === 0" class="text-center py-6" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Избранное пусто</div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <div v-for="item in favorites.filter(item => item && item.id)" :key="item.id" class="border p-4 rounded-lg shadow-sm transition-all duration-300 hover:shadow-md" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'">
              <img :src="getImageUrl(item.image)" alt="Product" class="w-full h-40 object-cover rounded-md mb-3" @error="handleImageError">
              <h4 class="text-sm font-semibold mb-2" :class="isDarkMode ? 'text-gray-100' : 'text-gray-800'">{{ item.name }}</h4>
              <p class="text-indigo-600 font-bold mb-2 text-sm">${{ item.price }}</p>
              <p class="text-xs line-clamp-3 mb-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">{{ item.description }}</p>
              <button @click="toggleFavorite(item)" class="text-red-500 hover:text-red-700 transition-colors duration-300 text-xs font-medium">Убрать</button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Order History Modal -->
    <transition name="fade">
      <div v-if="showOrderHistory" class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50" @click.self="toggleOrderHistory">
        <div class="rounded-2xl p-6 w-full max-w-3xl shadow-2xl" :class="isDarkMode ? 'bg-gray-800' : 'bg-white'">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-xl sm:text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">История заказов</h3>
            <button @click="toggleOrderHistory" class="hover:text-indigo-500 transition-colors duration-300" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div v-if="orderHistory.length === 0" class="text-center py-6" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">История заказов пуста</div>
          <div v-else class="space-y-4 max-h-80 overflow-y-auto">
            <div v-for="order in orderHistory.filter(order => order && order.id)" :key="order.id" class="p-4 rounded-lg shadow-sm" :class="isDarkMode ? 'bg-gray-700' : 'bg-gray-50'">
              <p class="text-sm font-semibold" :class="isDarkMode ? 'text-gray-100' : 'text-gray-800'">Заказ #{{ order.id }} от {{ formatDate(order.created_at) }}</p>
              <p class="text-xs" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Клиент: {{ order.customer_name }}</p>
              <p class="text-xs" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Адрес: {{ order.address }}</p>
              <p class="text-xs" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Доставка: {{ order.delivery }}</p>
              <p class="text-xs" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Статус: {{ order.status === 'Pending' ? 'Ожидает обработки' : order.status === 'Shipped' ? 'Отправлен' : 'Доставлен' }}</p>
              <p class="text-xs" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Итого: ${{ order.total }}</p>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Footer -->
    <footer class="py-8 border-t" :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'">
      <div class="container mx-auto text-center">
        <div class="flex items-center justify-center space-x-3 mb-4">
          <svg class="w-10 h-10 animate-pulse" :class="isDarkMode ? 'text-indigo-400' : 'text-indigo-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
          <p class="text-base font-semibold" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">© 2025 TechHub. Все права защищены.</p>
        </div>
        <div class="flex justify-center space-x-6 sm:space-x-8">
          <a href="#" class="text-base font-semibold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition-all duration-300">О нас</a>
          <a href="#" class="text-base font-semibold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition-all duration-300">Контакты</a>
          <a href="#" class="text-base font-semibold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition-all duration-300">Политика</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import ProductList from './components/ProductList.vue';
import axios from 'axios';
import debounce from 'lodash/debounce';

export default {
  name: 'App',
  components: {
    ProductList,
  },
  data() {
    return {
      isLoading: true,
      loadingProgress: 0,
      showCart: false,
      showSidebar: false,
      showCompare: false,
      showOrderHistory: false,
      showFavorites: false,
      categories: [],
      brands: ['Apple', 'Samsung', 'Sony', 'Xiaomi', 'Asus'],
      selectedCategory: null,
      selectedBrands: [],
      cart: [],
      compareList: [],
      favorites: [],
      order: {
        name: '',
        address: '',
        delivery: 'standard',
        comment: '',
      },
      orderHistory: [],
      priceFilter: 5000,
      inStockOnly: false,
      sortOption: 'price-asc',
      searchQuery: '',
      searchSuggestions: [],
      notification: null,
      currentPage: 1,
      totalPages: 1,
      itemsPerPage: 12,
      isDarkMode: false,
    };
  },
  computed: {
    cartCount() {
      return this.cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
    },
    cartTotal() {
      let total = this.cart.reduce((sum, item) => sum + parseFloat(item.price) * (item.quantity || 1), 0);
      if (this.order.delivery === 'standard') total += 5;
      if (this.order.delivery === 'express') total += 15;
      return total.toFixed(2);
    },
  },
  mounted() {
    this.fetchCategories();
    this.loadCartFromStorage();
    this.loadFavoritesFromStorage();
    this.fetchOrderHistory();
    this.loadDarkModePreference();
    window.addEventListener('resize', this.handleResize);
    this.simulateLoading();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    simulateLoading() {
      const interval = setInterval(() => {
        if (this.loadingProgress < 100) {
          this.loadingProgress += 10;
        } else {
          clearInterval(interval);
          setTimeout(() => {
            this.isLoading = false;
          }, 500);
        }
      }, 200);
    },
    async fetchCategories() {
      try {
        const response = await axios.get('http://localhost:8000/api/categories/');
        this.categories = Array.isArray(response.data) ? response.data : [];
      } catch (error) {
        console.error('Error fetching categories:', error);
        this.categories = [];
      }
    },
    async fetchOrderHistory() {
      try {
        const response = await axios.get('http://localhost:8000/api/orders/');
        console.log('Order history response:', response.data);
        this.orderHistory = Array.isArray(response.data) 
          ? response.data.filter(order => order && order.id) 
          : response.data && response.data.results && Array.isArray(response.data.results) 
            ? response.data.results.filter(order => order && order.id) 
            : [];
      } catch (error) {
        console.error('Error fetching order history:', error);
        this.orderHistory = [];
      }
    },
    async fetchSuggestions(query) {
      if (!query) {
        this.searchSuggestions = [];
        return;
      }
      try {
        const response = await axios.get(`http://localhost:8000/api/products/?search=${query}`);
        this.searchSuggestions = Array.isArray(response.data) ? response.data.slice(0, 5) : [];
      } catch (error) {
        console.error('Error fetching suggestions:', error);
        this.searchSuggestions = [];
      }
    },
    debouncedSearch: debounce(function () {
      this.fetchSuggestions(this.searchQuery);
    }, 300),
    selectSuggestion(suggestion) {
      this.searchQuery = suggestion.name;
      this.searchSuggestions = [];
    },
    toggleCart() {
      this.showCart = !this.showCart;
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },
    toggleCompare() {
      this.showCompare = !this.showCompare;
    },
    toggleOrderHistory() {
      this.showOrderHistory = !this.showOrderHistory;
    },
    toggleFavorites() {
      this.showFavorites = !this.showFavorites;
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('darkMode', this.isDarkMode);
    },
    loadDarkModePreference() {
      const darkMode = localStorage.getItem('darkMode');
      this.isDarkMode = darkMode === 'true';
    },
    selectCategory(categoryId) {
      this.selectedCategory = categoryId;
      this.currentPage = 1;
    },
    addToCart(product, event) {
      const cartButton = this.$refs.cartButton;
      const productImage = event.target.closest('.product-card')?.querySelector('img');
      if (productImage && cartButton) {
        const clone = productImage.cloneNode(true);
        const rect = productImage.getBoundingClientRect();
        const cartRect = cartButton.getBoundingClientRect();

        clone.style.position = 'fixed';
        clone.style.zIndex = '1000';
        clone.style.width = `${rect.width}px`;
        clone.style.height = `${rect.height}px`;
        clone.style.top = `${rect.top}px`;
        clone.style.left = `${rect.left}px`;
        clone.style.transition = 'all 0.7s ease-in-out';
        document.body.appendChild(clone);

        requestAnimationFrame(() => {
          clone.style.width = '40px';
          clone.style.height = '40px';
          clone.style.top = `${cartRect.top + 8}px`;
          clone.style.left = `${cartRect.left + 8}px`;
          clone.style.opacity = '0';
        });

        setTimeout(() => {
          document.body.removeChild(clone);
        }, 700);
      }

      const existingItem = this.cart.find(item => item.id === product.id);
      if (existingItem) {
        existingItem.quantity = (existingItem.quantity || 1) + (product.quantity || 1);
      } else {
        this.cart.push({ ...product, quantity: product.quantity || 1 });
      }
      this.saveCartToStorage();
      this.showNotification('success', `${product.name} добавлен в корзину!`);
    },
    removeFromCart(productId) {
      this.cart = this.cart.filter(item => item.id !== productId);
      this.saveCartToStorage();
      this.showNotification('success', 'Товар удалён из корзины.');
    },
    clearCart() {
      this.cart = [];
      this.saveCartToStorage();
      this.showNotification('success', 'Корзина очищена.');
    },
    increaseQuantity(item) {
      item.quantity = (item.quantity || 1) + 1;
      this.saveCartToStorage();
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        item.quantity -= 1;
        this.saveCartToStorage();
      } else {
        this.removeFromCart(item.id);
      }
    },
    toggleCompareItem(product) {
      const index = this.compareList.findIndex(item => item.id === product.id);
      if (index === -1) {
        if (this.compareList.length < 3) {
          this.compareList.push(product);
          this.showNotification('success', `${product.name} добавлен в сравнение.`);
        } else {
          this.showNotification('error', 'Можно сравнить не более 3 товаров.');
        }
      } else {
        this.compareList.splice(index, 1);
        this.showNotification('success', `${product.name} удалён из сравнения.`);
      }
    },
    toggleFavorite(product) {
      const index = this.favorites.findIndex(item => item.id === product.id);
      if (index === -1) {
        this.favorites.push(product);
        this.showNotification('success', `${product.name} добавлен в избранное.`);
      } else {
        this.favorites.splice(index, 1);
        this.showNotification('success', `${product.name} удалён из избранного.`);
      }
      this.saveFavoritesToStorage();
    },
    loadCartFromStorage() {
      const savedCart = localStorage.getItem('techHubCart');
      if (savedCart) this.cart = JSON.parse(savedCart).filter(item => item && item.id);
    },
    saveCartToStorage() {
      localStorage.setItem('techHubCart', JSON.stringify(this.cart));
    },
    loadFavoritesFromStorage() {
      const savedFavorites = localStorage.getItem('techHubFavorites');
      if (savedFavorites) this.favorites = JSON.parse(savedFavorites).filter(item => item && item.id);
    },
    saveFavoritesToStorage() {
      localStorage.setItem('techHubFavorites', JSON.stringify(this.favorites));
    },
    showNotification(type, message) {
      this.notification = { type, message };
      setTimeout(() => this.clearNotification(), 3000);
    },
    clearNotification() {
      this.notification = null;
    },
    getImageUrl(image) {
      if (!image) return 'https://via.placeholder.com/300x200?text=No+Image';
      return image.startsWith('http') ? image : `http://localhost:8000${image}`;
    },
    handleImageError(event) {
      event.target.src = 'https://via.placeholder.com/300x200?text=Image+Not+Found';
    },
    async submitOrder() {
      if (!this.order.name || !this.order.address) {
        this.showNotification('error', 'Пожалуйста, заполните имя и адрес доставки.');
        return;
      }
      const orderData = {
        items: this.cart.map(item => ({
          id: item.id,
          name: item.name,
          price: item.price,
          image: item.image,
          quantity: item.quantity || 1,
          components: item.components || {},
        })),
        total: this.cartTotal,
        customer_name: this.order.name,
        address: this.order.address,
        delivery: this.order.delivery,
        comment: this.order.comment,
        status: 'Pending',
      };
      try {
        await axios.post('http://localhost:8000/api/orders/', orderData);
        this.showNotification('success', 'Заказ успешно оформлен!');
        this.cart = [];
        this.saveCartToStorage();
        this.order = { name: '', address: '', delivery: 'standard', comment: '' };
        this.showCart = false;
        this.fetchOrderHistory();
      } catch (error) {
        console.error('Error submitting order:', error);
        this.showNotification('error', 'Ошибка при оформлении заказа.');
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('ru-RU', { day: '2-digit', month: 'long', year: 'numeric' });
    },
    updatePage(pageCount) {
      this.totalPages = pageCount;
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    handleResize() {},
    particleStyle() {
      const size = Math.random() * 10 + 5;
      const duration = Math.random() * 4 + 2;
      const delay = Math.random() * 2;
      const x = Math.random() * 100 - 50;
      const y = Math.random() * 100 - 50;
      return {
        width: `${size}px`,
        height: `${size}px`,
        background: 'rgba(255, 255, 255, 0.3)',
        borderRadius: '50%',
        position: 'absolute',
        top: `${y}%`,
        left: `${x}%`,
        animation: `float ${duration}s infinite ease-in-out ${delay}s`,
      };
    },
  },
};
</script>

<style scoped>
#app {
  background: linear-gradient(to bottom right, #f3f4f6, #e5e7eb);
}
.bg-gray-900 {
  background: linear-gradient(to bottom right, #111827, #1f2937);
}
button {
  transition: all 0.3s ease;
}
button:hover:not(:disabled) {
  transform: scale(1.03);
}
button:active:not(:disabled) {
  transform: scale(0.97);
}
.shadow-lg {
  box-shadow: 0 10px 20px rgba(0, 0,0, 0.1);
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0.98);
}
.slide-enter-active, .slide-leave-active {
  transition: transform 0.5s ease;
}
.slide-enter-from, .slide-leave-to {
  transform: translateX(-100%);
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.animate-spin {
  animation: spin 1s linear infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
.animate-pulse {
  animation: pulse 1.5s infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.animate-bounce {
  animation: bounce 1s infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}
.particle {
  position: absolute;
}
@keyframes progress {
  0% { width: 0%; }
  100% { width: 100%; }
}
.animate-progress {
  animation: progress 2s ease-in-out forwards;
}

/* Адаптивность */
@media (max-width: 640px) {
  .container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  .pt-16 {
    padding-top: 4.5rem; /* Учитываем высоту хедера на мобильных */
  }
  .w-72 {
    width: 80%;
  }
  .text-4xl {
    font-size: 2rem;
  }
  .max-w-5xl {
    max-width: 90%;
  }
  .max-w-3xl {
    max-width: 90%;
  }
  .max-w-md {
    max-width: 90%;
  }
  .grid-cols-3 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
  .grid-cols-2 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
  .space-x-8 > :not([hidden]) ~ :not([hidden]) {
    --tw-space-x-reverse: 0;
    margin-right: calc(1.5rem * var(--tw-space-x-reverse));
    margin-left: calc(1.5rem * (1 - var(--tw-space-x-reverse)));
  }
}
</style>