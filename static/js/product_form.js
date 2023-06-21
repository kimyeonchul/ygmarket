const submitBtn = document.querySelector('.create_product_confirm_btn');
  const fileInput = document.querySelector('.create_product_image_input');
  const label = document.querySelector('.create_product_image_label');
  const preview = document.querySelector('.create_product_preview');

  label.addEventListener('click', (e) => {
    if (e.target !== fileInput) {
      fileInput.click();
    }
  });

  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];

    if (file) {
      const reader = new FileReader();

      reader.onload = (e) => {
        preview.innerHTML = `<img src="${e.target.result}" alt="Preview" width="100px" height="100px" style="margin-left: 10px" />`;
      };

      reader.readAsDataURL(file);
    } else {
      preview.innerHTML = '';
    }
  });