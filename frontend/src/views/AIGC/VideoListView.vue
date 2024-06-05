<template>
    <div class="container">
        <h1>My Videos</h1>
        <UploadCard :show="showUploadCard" @onClose="closeUploadCard" />

        <div v-if="loading">Loading...</div>
        <div v-if="error" class="error">{{ error }}</div>

        <div v-if="videos.length === 0">
            <p>You have no videos. Click the button above to add a new video.</p>
        </div>

        <ul v-else class="video-list">
            <li v-for="video in videos" :key="video.generation_id" :class="getCardClass(video.status)"
                @click="toggleVideo(video)" @mouseover="hover = video.generation_id" @mouseleave="hover = null">
                <p>Video ID: {{ abbreviateId(video.generation_id) }}</p>
                <p>Status: {{ video.status }}</p>
                <div v-if="hover === video.generation_id && video.status === 'complete'" class="tooltip">
                    Click to view the video
                </div>
                <div v-if="video.status !== 'complete'" class="loading">
                    Loading video, this may take 2-3 minutes...
                </div>
                <div v-if="video.showVideo" class="video-container">
                    <video :src="`data:video/mp4;base64,${video.video_data}`" controls></video>
                    <button @click.stop="toggleVideo(video)" class="collapse-btn">Collapse</button>
                </div>
            </li>
        </ul>
        <Navbar />
        <button class="upload-btn" @click="showUploadCard = true">+</button>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import UploadCard from '../../components/AIGC/UploadCard.vue';
import Navbar from '@/components/Navbar.vue';

export default {
    name: 'VideoListView',
    components: {
        UploadCard,
        Navbar,
    },
    setup() {
        const videos = ref([]);
        const loading = ref(false);
        const error = ref('');
        const showUploadCard = ref(false);
        const hover = ref(null);

        const fetchVideos = async () => {
            loading.value = true;
            error.value = '';
            const token = localStorage.getItem('token');
            try {
                const response = await axios.get('http://localhost:8000/api/image-to-video/vedio_status/', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                videos.value = response.data.videos.map((video) => ({ ...video, showVideo: false }));
            } catch (err) {
                if (err.response && err.response.status === 401) {
                    error.value = 'Unauthorized. Please provide a valid JWT token.';
                } else {
                    error.value = 'Failed to fetch videos. Please try again.';
                }
            } finally {
                loading.value = false;
            }
        };

        const closeUploadCard = () => {
            showUploadCard.value = false;
            fetchVideos(); // Refresh the video list after closing the upload card
        };

        const getCardClass = (status) => {
            if (status === 'complete') return 'card complete';
            if (status === 'in-progress') return 'card in-progress';
            if (status === 'expired') return 'card expired';
            return 'card';
        };

        const toggleVideo = async (video) => {
            if (video.status !== 'complete') return;
            if (!video.showVideo) {
                const token = localStorage.getItem('token');
                try {
                    const response = await axios.get('http://localhost:8000/api/image-to-video/video_data/', {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                        params: {
                            generation_id: video.generation_id,
                        },
                    });
                    if (response.data.video_data) {
                        video.video_data = response.data.video_data;
                        video.showVideo = true;
                    } else {
                        error.value = 'Video not found';
                    }
                } catch (err) {
                    error.value = 'Failed to fetch video data. Please try again.';
                }
            } else {
                video.showVideo = false;
            }
        };

        const abbreviateId = (id) => {
            return id.length > 10 ? id.substring(0, 10) + '...' : id;
        };

        const getVideoStyle = (video) => {
            return {
                width: '100%',
                aspectRatio: '16/9',
            };
        };

        onMounted(fetchVideos);

        return {
            videos,
            loading,
            error,
            showUploadCard,
            closeUploadCard,
            getCardClass,
            toggleVideo,
            abbreviateId,
            getVideoStyle,
            hover,
        };
    },
};
</script>

<style>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.error {
    color: red;
}

.video-list {
    list-style-type: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.card {
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
    cursor: pointer;
    border: 2px solid transparent;
    transition: all 0.3s ease;
    width: 90%;
    max-width: 600px;
    position: relative;
}

.card:hover {
    transform: scale(1.05);
}

.card.complete {
    background-color: #d4edda;
    color: #155724;
    border-color: #c3e6cb;
}

.card.in-progress {
    background-color: #fff3cd;
    color: #856404;
    border-color: #ffeeba;
}

.card.expired {
    background-color: #f8d7da;
    color: #721c24;
    border-color: #f5c6cb;
}

.card video {
    margin-top: 10px;
    width: 100%;
    height: auto;
}

.card p {
    word-break: break-all;
}

.upload-btn {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #28a745;
    color: white;
    font-size: 24px;
    font-weight: bold;
    border: none;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.upload-btn:hover {
    background-color: #218838;
    transform: scale(1.1);
}

.tooltip {
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 5px;
    border-radius: 5px;
    font-size: 12px;
    white-space: nowrap;
}

.loading {
    margin-top: 10px;
    font-size: 14px;
    color: #856404;
}

.video-container {
    margin-top: 10px;
}

.collapse-btn {
    margin-top: 10px;
    padding: 5px 10px;
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.collapse-btn:hover {
    background-color: #c82333;
}
</style>
