        if any(word in prompt.lower() for word in ["تخيل", "صورة", "image", "draw", "imagine"]):
            try:
                with st.spinner("Visualizing the Matrix..."):
                    # استعمال الموديل المخصص للصور
                    image_model = genai.GenerativeModel('gemini-1.5-flash')
                    # طلب توليد الصورة (خاص يكون الـ API كيدعم Imagen)
                    response = image_model.generate_content(
                        f"Generate a high-quality Matrix-style image: {prompt}",
                        # هاد السطر هو اللي كيطلب توليد مخرجات بصرية
                        generation_config={"response_mime_type": "image/png"} 
                    )
                    # عرض الصورة إيلا رجعات
                    if response.candidates[0].content.parts[0].inline_data:
                        st.image(response.candidates[0].content.parts[0].inline_data.data)
                    else:
                        st.info("The Matrix is only showing me code for now. Here is the description: " + response.text)
            except Exception as e:
                st.error("The simulation failed to render the image.")
