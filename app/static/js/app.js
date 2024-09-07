// Функция для получения списка продуктов через API
async function fetchProducts() {
    const response = await fetch('/api/products');
    const products = await response.json();
    displayProducts(products);
}

// Функция для отображения продуктов на странице
function displayProducts(products) {
    const productList = document.getElementById('product-list');
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <p><strong>Цена: ${product.price} руб.</strong></p>
        `;
        productList.appendChild(productCard);
    });
}

// Вызываем функцию для загрузки продуктов при загрузке страницы
window.onload = fetchProducts;
