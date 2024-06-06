<template>
    <div class="all-nodes">
      <h2>全部节点</h2>
      <ul class="node-list">
        <li v-for="(node, index) in nodes" :key="index" class="node-item">{{ node }}</li>
      </ul>
    </div>
  
    <!-- 导航栏组件 -->
    <Navbar />
  </template>
  
  <script setup>
  import Navbar from './Navbar.vue'; // 导入导航栏组件
  
  const nodes = [
    "others39", "node19", "wc9", "supermarket23", "supermarket22", "supermarket29", "node27", "node58", "others36",
    "supermarket3", "node32", "node56", "supermarket17", "node39", "node31", "restaurant14", "wc7", "others7",
    "supermarket13", "wc12", "others6", "supermarket33", "restaurant15", "restaurant21", "others35", "node7", 
    "others31", "supermarket10", "others12", "others4", "node57", "node52", "others18", "supermarket32", 
    "supermarket14", "restaurant40", "node44", "others33", "node6", "restaurant4", "supermarket15", "node15", 
    "restaurant18", "supermarket7", "others40", "supermarket25", "others14", "restaurant8", "restaurant6", 
    "node55", "restaurant7", "others13", "node29", "supermarket35", "wc2", "supermarket9", "restaurant38", 
    "wc3", "restaurant28", "node16", "node20", "others26", "wc13", "node23", "supermarket36", "node49", 
    "node60", "node53", "supermarket18", "others25", "node59", "node54", "wc10", "others32", "restaurant20", 
    "supermarket40", "others10", "others37", "restaurant9", "restaurant32", "supermarket2", "others5", 
    "restaurant10", "others3", "others2", "node50", "restaurant3", "node47", "restaurant5", "wc16", "node8", 
    "wc11", "node28", "node14", "node24", "wc5", "node35", "restaurant16", "supermarket8", "node38", 
    "supermarket5", "restaurant35", "node41", "node33", "wc6", "supermarket34", "wc15", "node34", 
    "restaurant17", "node10", "node5", "wc20", "others24", "node26", "others21", "supermarket20", 
    "supermarket21", "wc14", "restaurant31", "node9", "node3", "restaurant36", "others8", "supermarket24", 
    "node17", "restaurant37", "restaurant39", "wc18", "node45", "node25", "others17", "others9", 
    "restaurant12", "restaurant11", "node1", "supermarket37", "node30", "supermarket16", "supermarket39", 
    "supermarket27", "supermarket28", "others1", "supermarket6", "restaurant22", "others15", "others22", 
    "others28", "others34", "others20", "node48", "others29", "wc17", "supermarket19", "node46", 
    "node11", "wc8", "node37", "supermarket11", "wc4", "others27", "restaurant27", "node43", "wc1", 
    "node18", "node21", "supermarket4", "restaurant33", "supermarket38", "restaurant30", "supermarket26", 
    "others19", "restaurant13", "node42", "others23", "supermarket1", "supermarket12", "restaurant2", 
    "node13", "restaurant25", "node4", "others11", "restaurant29", "node2", "restaurant23", "node12", 
    "supermarket30", "node40", "supermarket31", "supermarket32", "restaurant24", "restaurant34", 
    "node36", "others30", "restaurant1"
  ];
  </script>
  
  <style scoped>
  .all-nodes {
    width: 800px;
    margin: auto;
    text-align: center;
    color: #333;
  }
  
  h2 {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  .node-list {
    list-style-type: none;
    padding: 0;
  }
  
  .node-item {
    margin-bottom: 5px;
    padding: 8px 20px;
    background-color: #4CAF50;
    border-radius: 20px;
    display: inline-block;
    font-size: 16px;
    font-weight: bold;
    color: #fff;
  }
  </style>
  