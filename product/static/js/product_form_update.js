  const fileInput = document.querySelector('.create_product_image_input');
  const label = document.querySelector('.create_product_image_label');
  const preview = document.querySelector('.create_product_preview_image');

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
          preview.src = e.target.result;
        };

        reader.readAsDataURL(file);
      }
      //     } else {
      //         preview.src = {% static 'images/person.png' %};
      // }
    });
