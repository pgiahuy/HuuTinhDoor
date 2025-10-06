async function loadData() {
    const res = await fetch('/api/index');
    const data = await res.json();

    const productGrid = document.getElementById('product-grid');
    data.products.forEach(product => {
        const card = document.createElement('div');
        card.classList.add('product-card');
        card.innerHTML = `
            <h2>${product.name}</h2>
            <p>Giá: ${product.price}đ</p>
            <p>${product.description}</p>
            <a class="btn" href="/product/${product.id}">Xem thêm</a>
        `;
        productGrid.appendChild(card);
    });

    const projectGrid = document.getElementById('project-grid');
    data.projects.forEach(project => {
        const card = document.createElement('div');
        card.classList.add('project-card');
        card.innerHTML = `
            <h2>${project.name}</h2>
            <p>Giá: ${project.price}đ</p>
            <p>${project.description}</p>
            <a class="btn" href="/project/${project.id}">Xem thêm</a>
        `;
        projectGrid.appendChild(card);
    });
}

window.addEventListener('DOMContentLoaded', loadData);
