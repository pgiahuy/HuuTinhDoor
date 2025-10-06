document.addEventListener('DOMContentLoaded', () => {

    // ----------------- Tab sidebar -----------------
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active-tab'));
            tab.classList.add('active-tab');
            const target = tab.dataset.tab;
            contents.forEach(c => c.classList.remove('active'));
            document.getElementById(`tab-${target}`).classList.add('active');
        });
    });

    // Mặc định mở tab Thêm
    document.querySelector('.tab-btn[data-tab="add"]').click();

    // ----------------- Lọc subcategory -----------------
    const categorySelect = document.getElementById('categorySelect');
    const subcategorySelect = document.getElementById('subcategorySelect');

    function filterSubcategories() {
        const selectedCategory = categorySelect.value;
        let firstVisible = null;

        Array.from(subcategorySelect.options).forEach(option => {
            if (option.dataset.category === selectedCategory) {
                option.style.display = 'block';
                if (!firstVisible) firstVisible = option;
            } else {
                option.style.display = 'none';
            }
        });

        subcategorySelect.value = firstVisible ? firstVisible.value : "";
    }

    if (categorySelect && subcategorySelect) {
        filterSubcategories();
        categorySelect.addEventListener('change', filterSubcategories);
    }

    // Lọc cate cho tìm kiếm
    const categoryProductSearch = document.getElementById('categoryProductSearch');
    const subcategoryProductSearch = document.getElementById('subcategoryProductSearch');

    function filterSubcategoriesSearch() {
        const selectedCategory = categoryProductSearch.value;
        let firstVisible = null;

        Array.from(subcategoryProductSearch.options).forEach(option => {
            if (option.dataset.category === selectedCategory|| option.dataset.category === 'all') {
                option.style.display = 'block';
                if (!firstVisible) firstVisible = option;
            } else {
                option.style.display = 'none';
            }
        });

        subcategoryProductSearch.value = firstVisible ? firstVisible.value : "";
    }

    if (categoryProductSearch && subcategoryProductSearch) {
        filterSubcategoriesSearch();
        categoryProductSearch.addEventListener('change', filterSubcategoriesSearch);
    }
    //



    // ----------------- Toggle Form Sản phẩm & Công trình -----------------
    const addProductForm = document.getElementById('addProductForm');
    const addProjectForm = document.getElementById('addProjectForm');

    const toggleFormProductBtn = document.getElementById('toggleFormProductBtn');
    const closeProductFormBtn = document.getElementById('CloseProductFormBtn');

    const toggleFormProjectBtn = document.getElementById('toggleFormProjectBtn');
    const closeProjectFormBtn = document.getElementById('closeProjectFormBtn');

    if (toggleFormProductBtn && addProductForm) {
        toggleFormProductBtn.addEventListener('click', () => {
            addProjectForm.style.display = 'none';
            addProductForm.style.display = addProductForm.style.display === 'block' ? 'none' : 'block';
        });
    }

    if (closeProductFormBtn) {
        closeProductFormBtn.addEventListener('click', () => {
            addProductForm.style.display = 'none';
        });
    }

    if (toggleFormProjectBtn && addProjectForm) {
        toggleFormProjectBtn.addEventListener('click', () => {
            addProductForm.style.display = 'none';
            addProjectForm.style.display = addProjectForm.style.display === 'block' ? 'none' : 'block';
        });
    }

    if (closeProjectFormBtn) {
        closeProjectFormBtn.addEventListener('click', () => {
            addProjectForm.style.display = 'none';
        });
    }

    // ----------------- Preview Ảnh Sản phẩm -----------------
    const productInput = document.getElementById('imagesProductInput');
    const productPreview = document.getElementById('previewProductContainer');
    const productMainIndex = document.getElementById('main_image_product_index');

    if (productInput && productPreview) {
            // Preview ảnh sản phẩm
        productInput.addEventListener('change', () => {
            productPreview.innerHTML = '';
            const files = productInput.files;
            for (let i = 0; i < files.length; i++) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const div = document.createElement('div');
                    div.classList.add('preview-item');

                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.classList.add('preview-img');

                    const radio = document.createElement('input');
                    radio.type = 'radio';
                    radio.name = 'main_image_product';
                    radio.value = i;
                    radio.classList.add('radio-main');
                    if (i === 0) radio.checked = true;
                    radio.addEventListener('change', () => { productMainIndex.value = i; });

                    // Khi click vào ảnh, radio cũng được chọn
                    img.addEventListener('click', () => {
                        radio.checked = true;
                        productMainIndex.value = i;
                    });

                    div.appendChild(img);
                    div.appendChild(radio);
                    productPreview.appendChild(div);

                    productMainIndex.value = 0;
                };
                reader.readAsDataURL(files[i]);
            }
        });

    }

    // ----------------- Preview Ảnh Công trình -----------------
    const projectInput = document.getElementById('imagesProjectInput');
    const projectPreview = document.getElementById('previewProjectContainer');
    const projectMainIndex = document.getElementById('main_image_project_index');

    if (projectInput && projectPreview) {
        projectInput.addEventListener('change', () => {
            projectPreview.innerHTML = '';
            const files = projectInput.files;
            for (let i = 0; i < files.length; i++) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const div = document.createElement('div');
                    div.classList.add('preview-item');

                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.classList.add('preview-img');
                    div.appendChild(img);

                    const radio = document.createElement('input');
                    radio.type = 'radio';
                    radio.name = 'main_image_project';
                    radio.value = i;
                    radio.classList.add('radio-main');
                    if (i === 0) radio.checked = true;
                    radio.addEventListener('change', () => { projectMainIndex.value = i; });

                    // Thêm: click vào ảnh cũng chọn radio
                    img.addEventListener('click', () => {
                        radio.checked = true;
                        projectMainIndex.value = i;
                    });

                    div.appendChild(radio);
                    projectPreview.appendChild(div);
                    projectMainIndex.value = 0;
                };
                reader.readAsDataURL(files[i]);
            }
        });

    }



    //================
    //=================
    //=============
    const productList = document.getElementById("product-list");
    const projectsList = document.getElementById("project-list");

    // Filter elements
    const categoryFilter = document.getElementById('categoryProductSearch');
    const subcategoryFilter = document.getElementById('subcategoryProductSearch');
    const searchProductByName = document.getElementById("searchProductByName");

    // Store fetched data
    let allProducts = [];
    let allProjects = [];

    // --- Fetch Products ---
    fetch("/api/products")
        .then(res => res.json())
        .then(data => {
            allProducts = data.products;
            renderProducts(allProducts);
        })
        .catch(err => console.error(err));

    // --- Fetch Projects ---
    fetch("/api/projects")
        .then(res => res.json())
        .then(data => {
            allProjects = data.projects;
            renderProjects(allProjects);
        })
        .catch(err => console.error(err));

    // --- Render Products ---
    function renderProducts(products) {
        productList.innerHTML = "";
        products.forEach(p => {
            const div = document.createElement("div");
            div.className = "product-card";
            div.dataset.category = p.category_id;
            div.dataset.subcategory = p.subcategory_id;

            let mainImg = "";
            if (p.images && p.images.length) {
                const main = p.images.find(img => img.is_main) || p.images[0];
                mainImg = `<img src="${main.url}" alt="${main.alt_text || p.name}">`;
            }

            div.innerHTML = `
                ${mainImg}
                <h3>${p.name}</h3>
                <p>Giá: $${p.price}</p>
                <p>Danh mục: ${p.category_name}</p>
                <p>Loại: ${p.subcategory_name}</p>
                <div>
                    <a href="/product/${p.id}" class="btn-detail">Xem</a>
                    <a href="/admin/edit_product/${p.id}" class="btn-edit">Sửa</a>
                    <a href="/admin/delete_product/${p.id}" class="btn-delete"
                       onclick="return confirm('Bạn có chắc chắn muốn xóa sản phẩm này?');">Xóa</a>
                </div>
            `;
            productList.appendChild(div);
        });
    }

    // --- Render Projects ---
    function renderProjects(projects) {
        projectsList.innerHTML = "";
        projects.forEach(pr => {
            const div = document.createElement("div");
            div.className = "project-card";

            let mainImg = "";
            if (pr.images && pr.images.length) {
                const main = pr.images.find(img => img.is_main) || pr.images[0];
                mainImg = `<div class="project-image"><img src="${main.url}" alt="${main.alt_text || pr.name}"></div>`;
            }

            div.innerHTML = `
                <h2>${pr.name}</h2>
                ${mainImg}
                <p>Giá: ${pr.price || "Liên hệ"}</p>
                <p>${pr.description || ""}</p>
                <a class="btn" href="/project/${pr.id}">Xem thêm</a>
            `;
            projectsList.appendChild(div);
        });
    }

    // --- Filter Products ---
    function filterProducts() {
        const txtSearch = searchProductByName.value.toLowerCase();
        const selectedCategory = categoryFilter.value;
        const selectedSubCategory = subcategoryFilter.value;

        const filtered = allProducts.filter(p => {
            const matchCategory = !selectedCategory || p.category_id.toString() === selectedCategory;
            const matchSubcategory = !selectedSubCategory || p.subcategory_id.toString() === selectedSubCategory;
            const matchName = p.name.toLowerCase().includes(txtSearch);
            return matchCategory && matchSubcategory && matchName;
        });

        renderProducts(filtered);
    }

    // Event listeners
    categoryFilter.addEventListener('change', filterProducts);
    subcategoryFilter.addEventListener('change', filterProducts);
    searchProductByName.addEventListener('input', filterProducts);


});
