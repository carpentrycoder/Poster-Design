// ==============================
// script.js
// Customer Order Form ka JavaScript
// ==============================


// ===== Price Tables (Backend se match karti hain) =====
const FONT_PRICES = {
    handwritten: 30,
    bold: 20,
    elegant: 40,
    modern: 25,
    classic: 35,
};

const SIZE_PRICES = {
    a4: 100,
    a3: 150,
    a2: 200,
    a1: 300,
    custom: 250,
};


// ==============================
// Price Update Function
// Jab bhi font ya size change ho, price update karo
// ==============================
function updatePrice() {
    const font = document.getElementById('font_style').value;
    const size = document.getElementById('poster_size').value;
    const priceAmount = document.getElementById('priceAmount');
    const priceBreakdown = document.getElementById('priceBreakdown');

    // Dono select kiye hain?
    if (font && size) {
        const fontPrice = FONT_PRICES[font] || 0;
        const sizePrice = SIZE_PRICES[size] || 0;
        const total = fontPrice + sizePrice;

        priceAmount.textContent = total;
        priceBreakdown.textContent = `Font (₹${fontPrice}) + Size (₹${sizePrice}) = ₹${total}`;
    } else if (font) {
        // Sirf font chuna
        const fontPrice = FONT_PRICES[font] || 0;
        priceAmount.textContent = '?';
        priceBreakdown.textContent = `Font (₹${fontPrice}) + Size chuniye`;
    } else if (size) {
        // Sirf size chuna
        const sizePrice = SIZE_PRICES[size] || 0;
        priceAmount.textContent = '?';
        priceBreakdown.textContent = `Font chuniye + Size (₹${sizePrice})`;
    } else {
        priceAmount.textContent = '---';
        priceBreakdown.textContent = 'Font aur Size chuniye price dekhne ke liye';
    }
}


// ==============================
// Image Preview Function
// Jab user image upload kare, preview dikhao
// ==============================
function previewImage(event) {
    const file = event.target.files[0];
    const previewDiv = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');

    if (file) {
        // FileReader se image read karo
        const reader = new FileReader();

        reader.onload = function(e) {
            previewImg.src = e.target.result;  // Image set karo
            previewDiv.classList.remove('d-none');  // Preview dikhao
        };

        reader.readAsDataURL(file);  // File read karo
    }
}


// ==============================
// Form Submit Handler
// Order submit karo API ko
// ==============================
document.getElementById('orderForm').addEventListener('submit', async function(e) {
    e.preventDefault();  // Default form submit rokna (page reload rokna)

    const submitBtn = document.getElementById('submitBtn');
    const alertBox = document.getElementById('alertBox');

    // Loading state dikhao
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
    submitBtn.disabled = true;

    // FormData banao (file upload ke saath kaam karta hai)
    const formData = new FormData(this);

    try {
        // API call karo
        const response = await fetch('/orders/', {
            method: 'POST',
            body: formData,  // FormData directly bhejo (Content-Type auto set hoga)
        });

        const data = await response.json();

        if (response.ok) {
            // ===== SUCCESS =====
            showAlert(
                'success',
                `✅ <strong>Order Successfully Submit Ho Gaya!</strong><br>
                Order ID: <strong>#${data.order_id}</strong> |
                Total Price: <strong>₹${data.total_price}</strong><br>
                ${data.message}`
            );

            // Form reset karo
            this.reset();
            document.getElementById('imagePreview').classList.add('d-none');
            document.getElementById('priceAmount').textContent = '---';
            document.getElementById('priceBreakdown').textContent = 'Font aur Size chuniye price dekhne ke liye';

            // Button normal karo
            submitBtn.innerHTML = '<i class="bi bi-send-fill me-2"></i>Order Submit Karo!';
            submitBtn.disabled = false;

            // Page ke upar scroll karo
            window.scrollTo({ top: 0, behavior: 'smooth' });

        } else {
            // ===== ERROR =====
            let errorMsg = data.detail || 'Kuch problem hui. Dobara try karo.';

            // Agar validation error hai (array format)
            if (Array.isArray(data.detail)) {
                errorMsg = data.detail.map(e => e.msg).join(', ');
            }

            showAlert('danger', '❌ Error: ' + errorMsg);

            // Button normal karo
            submitBtn.innerHTML = '<i class="bi bi-send-fill me-2"></i>Order Submit Karo!';
            submitBtn.disabled = false;
        }

    } catch (error) {
        // Network error ya kuch aur
        console.error('Error:', error);
        showAlert('danger', '❌ Server se connect nahi ho pa raha. Internet check karo ya baad mein try karo.');

        submitBtn.innerHTML = '<i class="bi bi-send-fill me-2"></i>Order Submit Karo!';
        submitBtn.disabled = false;
    }
});


// ==============================
// Alert Show Karne Ka Function
// type = 'success', 'danger', 'warning', 'info'
// ==============================
function showAlert(type, message) {
    const alertBox = document.getElementById('alertBox');
    alertBox.className = `alert alert-${type}`;
    alertBox.innerHTML = message;
    alertBox.classList.remove('d-none');

    // Alert auto-hide (success ke liye 8 sec baad)
    if (type === 'success') {
        setTimeout(() => {
            alertBox.classList.add('d-none');
        }, 8000);
    }
}