import { createStore } from 'vuex'

const store = createStore({
  state () {
    return {
      password: "",
      score: -1,
      buffs: [],
      previous: [],
      advice: []
    }
  },
  mutations: {
    changePassword (state, newPassword) {
      state.password = newPassword
    },
    changeScore (state, newScore) {
      state.score = newScore
    },
    changeBuffs (state, newBuffs) {
      state.buffs = newBuffs
    },
    pushPrevious (state) {
      state.previous.push(state.password)
    },
    popPrevious (state) {
      state.previous.pop()
    },
    changeAdvice (state, newAdvice) {
      state.advice = newAdvice
    }
  }
})

export default store