const signupBt = document.querySelector('.signupBt');
        const signupSB = document.querySelector('#signupSB')
        const fileInput = document.querySelector('.signup_input_profile_image');
        const label = document.querySelector('.signup_label_profile_image');
        const preview = document.querySelector('.signup_profile_image_preview');

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
        signupBt.addEventListener('click', () => {
            signupSB.click();
        })