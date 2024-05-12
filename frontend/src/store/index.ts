import { createStore } from 'vuex';

// 定义 state 的类型
interface State {
  isLoggedIn: boolean;
}

export default createStore<State>({
  state: {
    isLoggedIn: false
  },
  mutations: {
    setLoggedIn(state: State, status: boolean) {
      state.isLoggedIn = status;
    }
  },
  actions: {
    login({ commit }) {
      commit('setLoggedIn', true);
    },
    logout({ commit }) {
      commit('setLoggedIn', false);
    }
  }
});
