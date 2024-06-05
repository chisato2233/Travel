<template>
    <div class="sidebar">
        <router-link to="/create-diary" class="sidebar-btn">✎</router-link>
        <router-link to="/all-diaries" class="sidebar-btn">☰</router-link>
    </div>
</template>

<script>
export default {
    name: 'Sidebar'
};
</script>

<style scoped>
.sidebar {
    position: fixed;
    top: 50%;
    left: 10px;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.sidebar-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50px;
    height: 50px;
    background-color: #008000;
    color: white;
    border-radius: 50%;
    font-size: 24px;
    font-weight: bold;
    text-decoration: none;
    transition: background-color 0.3s, transform 0.3s;
}

.sidebar-btn:hover {
    background-color: #005200;
    transform: scale(1.1);
}
</style>
