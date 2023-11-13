document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file_upload");
    const imagePreview = document.getElementById("image-preview");

    // Check for saved image data in localStorage
    const imageData = localStorage.getItem("imageData");
    if (imageData) {
        imagePreview.src = imageData;
    }

    fileInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.addEventListener("load", function () {
                imagePreview.src = reader.result;
                localStorage.setItem("imageData", reader.result);
            });

            reader.readAsDataURL(file);
        }
    });

    const form = document.getElementById("image-form");
    form.addEventListener("submit", function () {
        // Clear the image data from localStorage
        localStorage.removeItem("imageData");
    });
});
