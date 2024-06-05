<template>
    <transition name="slide-up">
        <div v-if="show" class="overlay" @click.self="closeCard">
            <div class="card">
                <button class="close-btn" @click="closeCard">×</button>
                <h2>Upload New Video</h2>
                <input type="file" @change="onFileChange" />
                <div v-if="previewUrl" class="preview">
                    <img :src="previewUrl" alt="Image Preview" />
                </div>
                <button class="upload-btn" @click="uploadImage" :disabled="!selectedFile || loading">
                    <span v-if="!loading">↑</span>
                    <span v-else class="loader"></span>
                </button>
                <div v-if="error" class="error">{{ error }}</div>
                <ul v-if="errorDetails.length" class="error-details">
                    <li v-for="(detail, index) in errorDetails" :key="index">{{ detail }}</li>
                </ul>
            </div>
        </div>
    </transition>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
    name: 'UploadCard',
    props: {
        show: {
            type: Boolean,
            default: false,
        },
    },
    emits: ['onClose'],
    setup(props, { emit }) {
        const selectedFile = ref(null);
        const previewUrl = ref(null);
        const loading = ref(false);
        const error = ref('');
        const errorDetails = ref([]);
        const generationId = ref('');

        const onFileChange = (event) => {
            const file = event.target.files[0];
            if (file) {
                selectedFile.value = file;
                const reader = new FileReader();
                reader.onload = (e) => {
                    previewUrl.value = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        };

        const resizeImage = (file, width, height, callback) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (event) => {
                const img = new Image();
                img.src = event.target.result;
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    canvas.width = width;
                    canvas.height = height;
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    canvas.toBlob(callback, 'image/jpeg', 1);
                };
            };
        };

        const getBestFitDimensions = (originalWidth, originalHeight) => {
            const aspectRatio = originalWidth / originalHeight;
            if (aspectRatio > 1) {
                if (originalWidth > 1024) {
                    return [1024, 576];
                } else if (originalWidth > 768) {
                    return [768, 768];
                } else {
                    return [576, 1024];
                }
            } else {
                if (originalHeight > 1024) {
                    return [576, 1024];
                } else if (originalHeight > 768) {
                    return [768, 768];
                } else {
                    return [1024, 576];
                }
            }
        };

        const uploadImage = async () => {
            if (!selectedFile.value) return;

            loading.value = true;
            error.value = '';
            errorDetails.value = [];
            generationId.value = '';

            const img = new Image();
            const reader = new FileReader();
            reader.readAsDataURL(selectedFile.value);
            reader.onload = (event) => {
                img.src = event.target.result;
                img.onload = async () => {
                    const [width, height] = getBestFitDimensions(img.width, img.height);
                    resizeImage(selectedFile.value, width, height, async (blob) => {
                        const reader = new FileReader();
                        reader.readAsDataURL(blob);
                        reader.onload = async () => {
                            try {
                                const base64Image = reader.result.split(',')[1];
                                const payload = {
                                    image: base64Image,
                                    seed: 0,
                                    cfg_scale: 1.8,
                                    motion_bucket_id: 127,
                                };

                                const response = await axios.post('http://localhost:8000/api/image-to-video/upload_image/', payload, {
                                    headers: {
                                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                                    },
                                });

                                generationId.value = response.data.generation_id;
                            } catch (err) {
                                if (err.response) {
                                    if (err.response.status === 400) {
                                        error.value = 'Bad request. Please check your input.';
                                        if (err.response.data.details && Array.isArray(err.response.data.details)) {
                                            errorDetails.value = err.response.data.details;
                                        }
                                    } else if (err.response.status === 401) {
                                        error.value = 'Unauthorized. Please provide a valid JWT token.';
                                    } else if (err.response.status === 403) {
                                        error.value = 'Your request was flagged by our content moderation system.';
                                    } else if (err.response.status === 413) {
                                        error.value = 'Your request was larger than 10MiB.';
                                    } else if (err.response.status === 422) {
                                        error.value = 'You made a request with an unsupported language.';
                                    } else if (err.response.status === 429) {
                                        error.value = 'You have made more than 150 requests in 10 seconds.';
                                    } else if (err.response.status === 500) {
                                        error.value = 'An internal error occurred. If the problem persists contact support.';
                                    } else {
                                        error.value = 'Failed to generate video. Please try again.';
                                    }
                                } else {
                                    error.value = 'Failed to generate video. Please try again.';
                                }
                            } finally {
                                loading.value = false;
                                selectedFile.value = null;
                                previewUrl.value = null;
                                closeCard();
                            }
                        };
                    });
                };
            };
        };

        const closeCard = () => {
            emit('onClose');
        };

        return {
            selectedFile,
            previewUrl,
            loading,
            error,
            errorDetails,
            generationId,
            onFileChange,
            uploadImage,
            closeCard,
        };
    },
};
</script>

<style>
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    display: flex;
    justify-content: center;
    align-items: flex-end;
    z-index: 1000;
}

.card {
    width: 80%;
    max-width: 400px;
    height: 60%;
    background: white;
    border-radius: 15px 15px 0 0;
    padding: 20px;
    box-shadow: 0 -5px 15px rgba(0, 0, 0, 0.3);
    position: relative;
    transition: transform 0.3s ease-out;
}

.close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 30px;
    height: 30px;
    background: red;
    color: white;
    border: none;
    border-radius: 50%;
    font-size: 20px;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
}

.close-btn:hover {
    transform: scale(1.1);
}

.upload-btn {
    width: 60px;
    height: 60px;
    background: yellow;
    color: black;
    font-size: 24px;
    font-weight: bold;
    border: none;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    cursor: pointer;
}

.upload-btn .loader {
    border: 4px solid #f3f3f3;
    border-radius: 50%;
    border-top: 4px solid black;
    width: 20px;
    height: 20px;
    animation: spin 2s linear infinite;
}

.preview img {
    width: 100%;
    max-height: 200px;
    object-fit: cover;
    margin-top: 20px;
}

.error {
    color: red;
}

.error-details {
    color: darkred;
    font-size: 0.9em;
    list-style: none;
    padding: 0;
    margin: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
    transition: transform 0.5s ease;
}

.slide-up-enter,
.slide-up-leave-to {
    transform: translateY(100%);
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>
